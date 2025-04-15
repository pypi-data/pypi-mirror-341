from functools import lru_cache
from typing import List, Tuple, Union

import numpy as np
import skimage.draw
from ase.data.colors import jmol_colors
from numpy.typing import NDArray
from rich.color import Color as RichColor
from rich.console import Console, ConsoleOptions, RenderableType, RenderResult
from rich.segment import Segment
from rich.style import Style
from scipy.spatial.transform import Rotation
from textual import events
from textual.reactive import reactive
from textual.widget import Widget

from timol.custom_typing import FloatType, IntType
from timol.reader import MoleculesReader

jmol_colors[0] = (0, 0, 0)


class HDRenderable:
    def __init__(
        self,
        matrix: NDArray,
        colors: NDArray,
        background_color: RichColor = RichColor.from_rgb(0, 0, 0),
    ):
        self.background_color = background_color
        self.matrix = matrix
        self.colors = colors
        self.n_indices = len(colors)

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        new_line = Segment.line()

        colors = self.colors

        @lru_cache(maxsize=1024)
        def get_style(i_top, i_bottom) -> Style:
            if i_top >= self.n_indices:
                # unnecessary default, just useful fornot crashing while debugging...
                top_color = RichColor.from_rgb(0, 255, 0)
            elif i_top < 0:
                top_color = self.background_color
            else:
                top_color = RichColor.from_rgb(*colors[i_top] * 255)

            if i_bottom >= self.n_indices:
                # unnecessary default, just useful fornot crashing while debugging...
                bottom_color = RichColor.from_rgb(0, 255, 0)
            elif i_bottom < 0:
                bottom_color = self.background_color
            else:
                bottom_color = RichColor.from_rgb(*colors[i_bottom] * 255)

            return Style(color=top_color, bgcolor=bottom_color)

        x, y = self.matrix.shape
        for i in range(0, x, 2):
            n_same_style = 0
            last_style, style = None, None
            for j in range(y):
                style = get_style(self.matrix[i, j], self.matrix[i + 1, j])
                if style is not last_style:
                    yield Segment("▀" * n_same_style, last_style)
                    n_same_style = 1
                else:
                    n_same_style += 1

                last_style = style

            if (n_same_style > 0) and (style is not None):
                yield Segment("▀" * n_same_style, style)
                style = None

            yield new_line


class MolViewer(Widget):
    index: reactive[int] = reactive(0)
    centering: reactive[bool] = reactive(False)
    radii_scale: reactive[float] = reactive(1)
    bond_factor: reactive[float] = reactive(0.7)
    mode: reactive[str] = reactive("lines")

    coordinates: NDArray
    sizes: NDArray
    colors: NDArray
    current_rotation: Rotation
    scale: float = 10
    offset: NDArray = np.zeros(2)
    background_color: RichColor
    _matrix: NDArray
    _draw_buffer: List[
        Tuple[FloatType, IntType, Union[NDArray, List], Union[NDArray, List]]
    ]

    DEFAULT_CSS = """
    MolViewer{
        width: 1fr;
        height: 1fr;
        background: red;
    }
    """

    def __init__(
        self,
        mols_reader: MoleculesReader,
        background_color: NDArray = np.array((0, 0, 0)),
    ):
        self.set_background_color(background_color)
        self.mols_reader = mols_reader
        self.clear_rotation()
        self._draw_buffer = []
        super().__init__()

    def set_background_color(self, background_color: NDArray):
        self.background_color = RichColor.from_rgb(*background_color)

    def clear_rotation(self):
        self.current_rotation = Rotation.identity()

    def get_system_center(self):
        return self.mols_reader.get_center(self.index)

    def build_matrix(self) -> NDArray:
        h, w = self.size.height * 2, self.size.width
        self._matrix = -np.ones((h, w)).astype(int)

        if self.mode == "spheres":
            self.buffer_draw_spheres()

        elif self.mode == "lines":
            self.buffer_draw_lines()

        elif self.mode == "spheres&lines":
            self.buffer_draw_spheres()
            self.buffer_draw_lines()

        else:
            raise Exception(f"Mode {self.mode} not recognised in build_matrix")

        return self.apply_draw_buffer()

    def apply_draw_buffer(self):
        matrix = self._matrix

        # sort by distance
        buffer = sorted(self._draw_buffer, key=lambda x: float(x[0]))

        for _, idx, x_idxs, y_idxs in buffer:
            matrix[y_idxs, x_idxs] = idx

        self._draw_buffer.clear()

        return matrix

    def get_pixel_size(self):
        return self.scale

    def get_pixel_visibilities(
        self, x: NDArray[np.int64], y: NDArray[np.int64]
    ) -> NDArray[np.bool]:
        w, h = self.size.width, self.size.height * 2
        return (x >= 0) & (x <= w - 1) & (y >= 0) & (y <= h - 1)

    def is_pixel_visible(self, x: IntType, y: IntType) -> bool:
        w, h = self.size.width, self.size.height * 2
        return bool((x >= 0) & (x <= w - 1) & (y >= 0) & (y <= h - 1))

    def snap_to_grid(self, x: FloatType, y: FloatType) -> Tuple[IntType, IntType]:
        return self.snap_to_x_grid(x), self.snap_to_y_grid(y)

    def snap_to_x_grid(self, x: FloatType) -> IntType:
        return np.round(x).astype(int)

    def snap_to_y_grid(self, y: FloatType) -> IntType:
        return np.round(y).astype(int)

    def get_line(self, x1: IntType, y1: IntType, x2: IntType, y2: IntType) -> List:
        line = skimage.draw.line(x1, y1, x2, y2)
        return line

    def buffer_draw_spheres(self) -> None:
        R, sizes, distances = self.get_projection()

        sizes = sizes * self.radii_scale

        # everything gets converted to pixel space
        for idx, distance in enumerate(distances):
            x, y = R[idx]
            sphere_size = sizes[idx] * self.get_pixel_size()

            x_min = self.snap_to_x_grid(x - sphere_size)
            x_max = self.snap_to_x_grid(x + sphere_size)

            y_min = self.snap_to_y_grid(y - sphere_size)
            y_max = self.snap_to_y_grid(y + sphere_size)

            # dumb and slow way to do it, could at least cache the mask somehow
            # it's spherical after all...
            # or do a np.where or smth, idk
            # TODO
            x_idxs, y_idxs = [], []
            for xn in range(int(x_min), int(x_max)):
                for yn in range(int(y_min), int(y_max)):
                    if np.sqrt((xn + 0.5 - x) ** 2 + (yn + 0.5 - y) ** 2) > sphere_size:
                        continue

                    x_idxs.append(xn)
                    y_idxs.append(yn)

            self.draw_buffer(float(distance), idx, np.array(x_idxs), np.array(y_idxs))

    def buffer_draw_lines(self) -> None:
        R, sizes, distances = self.get_projection()
        nbs = self.get_bonds()

        xs, ys = self.snap_to_grid(R[:, 0], R[:, 1])

        assert isinstance(xs, np.ndarray)
        assert isinstance(ys, np.ndarray)

        for nb_idx in range(len(nbs)):
            idx1, idx2 = nbs[nb_idx]

            x1, x2 = xs[idx1], xs[idx2]
            y1, y2 = ys[idx1], ys[idx2]

            # get the connecting line
            xline, yline = self.get_line(x1, y1, x2, y2)
            # taking the average distance as the "height" for the line to reduce buffer calls
            # This could lead to some visual artefacts but it's cheaper
            distance = (distances[idx1] + distances[idx2]) / 2

            # separate the two colors
            # number of points in each color proportional to respective atom sizes
            n_points = len(xline)
            ratio = sizes[idx1] / (sizes[idx1] + sizes[idx2])
            n1 = int(n_points * ratio)
            self.draw_buffer(float(distance), idx1, xline[:n1], yline[:n1])
            self.draw_buffer(float(distance), idx2, xline[n1:], yline[n1:])

    def draw_buffer(
        self,
        distance: FloatType,
        index: int,
        x_idxs: NDArray,
        y_idxs: NDArray,
    ):
        visible_pixels = self.get_pixel_visibilities(x_idxs, y_idxs)
        x_idxs = x_idxs[visible_pixels]
        y_idxs = y_idxs[visible_pixels]
        if len(x_idxs) > 0:
            self._draw_buffer.append((distance, index, x_idxs, y_idxs))

    def rotate_camera(self, x: FloatType = 0, y: FloatType = 0, z: FloatType = 0):
        r = Rotation.from_euler("zyx", np.array([x, y, z]), degrees=True)
        self.current_rotation = r * self.current_rotation
        self.refresh()

    def shift_offset(self, x: FloatType = 0, y: FloatType = 0):
        self.offset[0] += x
        self.offset[1] += y
        self.refresh()

    def on_mouse_move(self, event: events.MouseMove) -> None:
        if event.button == 1:
            if event.shift or event.meta:
                self.shift_offset(-0.1 * event.delta_x, -0.1 * event.delta_y)

            else:
                self.rotate_camera(5 * event.delta_x, -5 * event.delta_y)

        elif event.button == 2:
            return

    def on_mouse_scroll_down(self, event: events.MouseScrollDown) -> None:
        self.zoom_by(-1)

    def _on_mouse_scroll_up(self, event: events.MouseScrollUp) -> None:
        self.zoom_by(1)

    def zoom_by(self, amount: int):
        if self.scale <= 1:
            self.scale = max(0.75, self.scale + 0.05 * amount)
        else:
            self.scale = np.floor(max(1, self.scale + amount))
        self.refresh()

    def get_bonds(self):
        return self.mols_reader.get_bonds(self.index, self.bond_factor)

    def get_projection(
        self, center: bool = True, scaled: bool = True
    ) -> tuple[NDArray, NDArray, NDArray]:
        """Very rudimentary orthographic projection along the x-axis for the sake
        of simplicity and efficiency.

        :return: Coordinates (N, 2), sizes (N), distances (N)
        :rtype: tuple[NDArray, NDArray, NDArray]
        """

        # note, I am defining "xyz" as referring to the image one sees:
        # x rotation: rotation around the horizontal axis
        # y rotation: rotation around the vertical axis
        # z rotation: rotation into/out of the screen
        # Those are not the same as the euler x/y/z definition
        rot = self.current_rotation
        R = self.mols_reader.get_positions(self.index)
        if self.centering:
            R -= self.get_system_center()
        R = rot.apply(R)

        if center != scaled:
            raise Exception("center and scaled most be the same for now")

        positions = R[:, 1:] - self.offset
        if center and scaled:
            positions *= self.scale
            h, w = self.size.height * 2, self.size.width
            x_center, y_center = w / 2, h / 2
            positions[:, 0] += x_center
            positions[:, 1] += y_center

        return positions, self.mols_reader.get_radii(self.index), R[:, 0]

    def build(self) -> list[str]:
        lines = []

        # lines = [f"[@{self.bg}] "*self.width] * self.get_height()
        matrix = self.build_matrix()
        for i in range(matrix.shape[0]):
            line = ""
            last_idx = -1
            for j in range(matrix.shape[1]):
                idx = matrix[i][j]
                if idx != last_idx:
                    line += f"{idx}"
                    last_idx = idx
                else:
                    line += " "
                # if idx > 0:
                #     line += f"{idx}"
                # else:
                #     line += f"[on #000000]{idx}[/on #000000]"
            lines.append(line)

        return lines

    def render(self) -> RenderableType:
        colors = jmol_colors[self.mols_reader.get_atomic_numbers(self.index)]
        return HDRenderable(
            self.build_matrix(), colors, background_color=self.background_color
        )
