import copy
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
from typing import List, Tuple, Iterable
import numpy as np

# Define an alias for a point for typing clarity
Point = Tuple[int, int]


class CleWin_color:
    def __init__(self, red: int, green: int, blue: int):
        """
        Interfaces the color format of CleWin
        """
        self.rgb = [red, green, blue]
        for color_channel in self.rgb:

            if not isinstance(color_channel, int):
                raise "Color channels must be integers"

            if not 0 <= color_channel <= 255:
                raise "Color channels must have value between 0 and 255"

        self.red = red
        self.green = green
        self.blue = blue

    def format_color_for_CleWin(self):
        return f"0f{format(self.blue, '02x')}{format(self.green, '02x')}{format(self.red, '02x')}"

    def format_color_hex_rgb(self):
        return f"#{format(self.red, '02x')}{format(self.green, '02x')}{format(self.blue, '02x')}"


class Mask_rectangle:
    def __init__(
        self, x_size_nm, y_size_nm, x_center_nm, y_center_nm, color: str = "blue"
    ):
        """
        A rectangle object mask.
        Rectangles are defined by a size in the x and y direction and a center position in the x and y direction.
        The center position is the center of the rectangle and the size is the size of the rectangle in nanometers.

        Args:
        -----
        x_size_nm: int
            The size of the rectangle in the x direction in nanometers
        
        y_size_nm: int
            The size of the rectangle in the y direction in nanometers

        x_center_nm: int
            The center position of the rectangle in the x direction in nanometers
        
        y_center_nm: int
            The center position of the rectangle in the y direction in nanometers
        
        color: str
            The color of the rectangle in plotting. Defaults to blue. Supports hex colors.
        """

        self.x_size_nm = x_size_nm
        self.y_size_nm = y_size_nm
        self.x_center_nm = x_center_nm
        self.y_center_nm = y_center_nm
        self.color = color

    def get_Mask_line(self):
        # is this even a line or is it a rectangle?
        return f"B {int(self.x_size_nm)} {int(self.y_size_nm)} {int(self.x_center_nm)} {int(self.y_center_nm)};\n"

    def shift(self, shift_x_nm, shift_y_nm):
        self.x_center_nm += shift_x_nm
        self.y_center_nm += shift_y_nm

    def deepcopy(self):
        return copy.deepcopy(self)

    def add_shape_to_ax(self, ax: plt.Axes, alpha=1):
        ax.add_patch(
            Rectangle(
                (
                    self.x_center_nm - self.x_size_nm / 2,
                    self.y_center_nm - self.y_size_nm / 2,
                ),
                self.x_size_nm,
                self.y_size_nm,
                facecolor=self.color,
                alpha=alpha,
            )
        )
        return None


class Mask_polygon:
    def __init__(self, points, color: str = "blue"):
        """
        A polygon object mask.
        Polygons are defined by a list of points. The points are the corners of the polygon and the polygon is closed by connecting the last point to the first point.
        The latter is assumed to be true by default (?) 

        Args:
        -----
        points: List[Point]
            A list of points that define the corners of the polygon. The points are connected linearly in the order they are given in the list and defines the border
            of the polygon.

        color: str
            The color of the polygon in plotting. Defaults to blue. Supports hex colors.
        """
        self.points = points
        self.color = color

    def get_Mask_line(self):
        string = "P"
        for point in self.points:
            x_coord = int(point[0])
            y_coord = int(point[1])
            string += f" {x_coord} {y_coord}"
        string += ";\n"

        return string

    def shift(self, shift_x_nm, shift_y_nm):
        for n in range(len(self.points)):
            self.points[n][0] += shift_x_nm
            self.points[n][1] += shift_y_nm

    def deepcopy(self):
        return copy.deepcopy(self)

    def add_shape_to_ax(self, ax: plt.Axes, alpha: float = 1):
        xy = np.array(self.points)
        ax.add_patch(Polygon(xy, closed=True, fill=True, color=self.color, alpha=alpha))
        return None


class Mask_wire:
    def __init__(self, points: List[Point], width_nm: int, color: str = "blue"):
        """
        Create a wire object mask.
        Wires are defined by a list of points and a width. The points are the center of the wire and the width is the width of the wire in nanometers.
        Wires run linearly between the points in the list. Edges are rounded, meaning the wire will be as if drawn using a pen with a circular tip.

        Args:
        -----
        points: List[Point]
            A list of points that define the centerline positions of the wire. The points are connected linearly in the order they are given in the list.

        width_nm: int
            The width of the wire in nanometers

        color: str
            The color of the wire in plotting. Defaults to blue.
        """
        if not isinstance(width_nm, (int, float)):
            raise "Width must be a number"

        if not isinstance(points, Iterable):
            raise "Points must be an iterable"

        self.points = np.array(points).squeeze()  # remove extra (empty) dimensions
        self.width_nm = width_nm
        self.color = color

    def get_cif_content(self):
        """Create a Wire object in the cif file in the proper .CIF format"""
        cif_content = f"W{self.width_nm}"

        for point in self.points:
            cif_content += f" {point[0]} {point[1]}"

        cif_content += ";\n"

        return cif_content

    def shift(self, shift_x_nm, shift_y_nm):
        """Shift the wire by a certain amount in the x and y direction"""
        for n in range(len(self.points)):
            self.points[n][0] += shift_x_nm
            self.points[n][1] += shift_y_nm

    def __paint_rect_between_points(
        self,
        point1: Point,
        point2: Point,
        width_nm: int,
        color: str,
        ax: plt.Axes,
        alpha: float = 1,
    ):

        if not color:
            color = self.color

        rot = np.array([[0, -1], [1, 0]])
        vec = point2 - point1
        adjust = vec / np.linalg.norm(vec) * width_nm / 2
        rot_adjust = rot @ adjust

        angle = np.arctan2(vec[1], vec[0]) * 180 / np.pi  # angle in degrees...

        rect = Rectangle(
            point1 - rot_adjust,
            angle=angle,
            width=np.linalg.norm(vec),
            height=width_nm,
            facecolor=color,
            alpha=alpha,
        )

        startCircle = Circle(point1, radius=width_nm / 2, facecolor=color, alpha=alpha)
        endCircle = Circle(point2, radius=width_nm / 2, facecolor=color, alpha=alpha)

        ax.add_patch(rect)
        ax.add_patch(startCircle)
        ax.add_patch(endCircle)

        return None

    def preview_plotAndShow(self, window_size: int = 10_000_000):
        """
        Show a preview of the wire geometry as it will be printed on the wafer in a matplotlib window

        Args:
        -----
        color: str
            The color of the wire in the preview
        window_size: int
            The side-length of the total window in nm
        """
        fig, ax = plt.subplots()
        ax.set_xlim(-window_size / 2, window_size / 2)
        xy = np.array(self.points)
        for pt1, pt2 in zip(xy[:-1], xy[1:]):
            self.__paint_rect_between_points(pt1, pt2, self.width_nm, self.color, ax)
        fig.show()

    def add_shape_to_ax(self, ax: plt.Axes, alpha: float = 1):
        """
        Add the wire geometry to a matplotlib axes object

        Args:
        -----
        ax: plt.Axes
            The axes object to add the wire geometry to
        """
        xy = np.array(self.points)
        for pt1, pt2 in zip(xy[:-1], xy[1:]):
            self.__paint_rect_between_points(
                pt1, pt2, self.width_nm, self.color, ax, alpha=alpha
            )

        return None


class CleWin_layer(object):
    def __init__(
        self,
        layer_name: str,
        layer_alias: str,
        layer_index: int,
        fill_color: CleWin_color,
        border_color: CleWin_color,
    ):
        # needs documentation, what is this?
        self.layer_name = layer_name
        self.layer_alias = layer_alias
        self.layer_index = layer_index
        self.fill_color = fill_color
        self.border_color = border_color
        self.shapes: List[Mask_polygon] = []  # only squares for now

    def add_shape_to_layer(self, shape: Mask_rectangle | Mask_polygon | Mask_wire):
        self.shapes.append(shape)

    def get_cif_declaration(self):
        fill_color_str = self.fill_color.format_color_for_CleWin()
        border_color_str = self.border_color.format_color_for_CleWin()

        # CleWin added because of the way the cif file is parsed by CleWin??
        cif_declaration = f"L {self.layer_alias};\n(CleWin: {self.layer_index} {self.layer_name}/{fill_color_str} {border_color_str});\n"

        return cif_declaration

    def get_cif_content(self):
        """
        Prints the content of the layer in the proper .CIF (Caltech Intermediate Form) format
        """
        # Initiate the layer using "L {layer_alias}";
        cif_content = f"L {self.layer_alias};\n"

        for shape in self.shapes:
            cif_content += shape.get_Mask_line()

        return cif_content

    def deepcopy(self):
        return copy.deepcopy(self)

    def shift(self, shift_x_nm, shift_y_nm):
        for shape in self.shapes:
            shape.shift(shift_x_nm, shift_y_nm)

    def plot_content(self, window_size: int = 10_000_000, ax=None):
        """
        Plots the content of the layer in a matplotlib window

        Args:
        -----
        window_size: int
            The side-length of the total window in nm
        ax: plt.Axes
            The axes object to add the wire geometry to
        """
        show = False
        if ax is None:
            fig, ax = plt.subplots()
            show = True
        ax.set_xlim(-window_size / 2, window_size / 2)
        ax.set_ylim(-window_size / 2, window_size / 2)
        for shape in self.shapes:
            shape.add_shape_to_ax(ax=ax)
        if show:
            plt.show()
        return fig, ax


def write_to_cif(filename, layers: List[CleWin_layer]):
    # Needs documentation
    cif = "(Layer names:);\n"
    for layer in layers:
        cif += layer.get_cif_declaration()

    # add .cif comment lol
    cif += "(Top level:);\n"

    # Why is this aspect ratio chosen (1:10)? Erlend please explain
    cif += "DS1 1 10;\n"

    # wtf is this ??
    cif += "9 MainSymbol;\n"

    for layer in layers:
        cif += layer.get_cif_content()

    # mark cif function as done (Done Function, DF) and end file (End, E)
    cif += "DF;\n"
    cif += "C 1;\n"  # What is this??
    cif += "E"

    with open(file=f"{filename}.cif", mode="w") as file:
        file.write(cif)


def load_cif(filename):
    # Needs documentation
    with open(file=f"{filename}.cif", mode="r") as file:
        cif = file.read()

    # Upper and lower bound the string to find the relevant info
    cif_relevant = cif.split("DF;")[0]
    cif = cif_relevant.split("(Layer names:);\n")[1]
    layer_info = cif.split("(Top level:);\n")[0]
    shape_info = cif.split("(Top level:);\n")[1]

    layers = []
    # Exclude the first substring because it is not layer info
    for layer_info_string in layer_info.split("L ")[1:]:
        layer: CleWin_layer = layer_from_cif_string(layer_info_string)
        layers.append(layer)

    # Stuff that works, but I did not write
    for layer_shapes_string in shape_info.split("L ")[1:]:
        layer_alias = layer_shapes_string.split(";\n")[0]
        shape_strings = layer_shapes_string.split(";\n")[1:-1]
        shapes = shapes_from_string(shape_strings)
        for layer in layers:
            if layer_alias == layer.layer_alias:
                for shape in shapes:
                    layer.add_shape_to_layer(shape)

    return layers


def shapes_from_string(shape_strings):
    # Needs documentation
    shapes = []

    for i, shape_string in enumerate(shape_strings):
        if shape_string[0] == "B":
            values = shape_string.split(" ")[1:]
            x_size = int(values[0])
            y_size = int(values[1])
            x_center = int(values[2])
            y_center = int(values[3])
            square = Mask_rectangle(
                x_size_nm=x_size,
                y_size_nm=y_size,
                x_center_nm=x_center,
                y_center_nm=y_center,
            )
            shapes.append(square)

        elif shape_string[0] == "P":
            value_strings = shape_string.split(" ")[1:]
            values = []
            for value_string in value_strings:
                value_string = value_string.strip("\n")
                values.append(int(value_string))

            points = []
            for x_coord, y_coord in zip(values[::2], values[1::2]):
                point = [x_coord, y_coord]
                points.append(point)

            polygon = Mask_polygon(points=points)
            shapes.append(polygon)

        elif shape_string[0] == "W":
            value_strings = shape_string.split(" ")[1:]
            values = []
            for value_string in value_strings:
                value_string = value_string.strip("\n")
                values.append(int(value_string))

            # I think the first value (width) is not separated from W by a space, as those are the only examples I have seen
            # Though this is not explicitly stated in the documentation, so be careful
            # Ie. W200 100 100 200 200 200 205; is a valid wire with width 200 nm
            width = values[0][1:]  # remove the W
            points = []
            for x_coord, y_coord in zip(values[1::2], values[2::2]):
                point = [x_coord, y_coord]
                points.append(point)

            wire = Mask_wire(points=points, width_nm=width)
            shapes.append(wire)

        else:
            raise ValueError(
                f"Unsupported shape encountered in shape number {i}:\n{shape_string}"
            )

    return shapes


def color_from_clewin_string(color_string):
    red = int(f"0x{color_string[2:4]}", base=0)
    green = int(f"0x{color_string[4:6]}", base=0)
    blue = int(f"0x{color_string[6:8]}", base=0)

    return CleWin_color(red, green, blue)


def layer_from_cif_string(layer_string):
    alias = layer_string.split(";")[0]

    layer_string = layer_string.split(";")[1]
    layer_string = layer_string.split("(")[1]
    layer_string = layer_string.split(")")[0]

    index = int(layer_string.split("/")[0].split(" ")[1])
    name = " ".join(layer_string.split("/")[0].split(" ")[2:])
    fill_color_string = layer_string.split("/")[1].split(" ")[0]
    border_color_string = layer_string.split("/")[1].split(" ")[1]
    fill_color = color_from_clewin_string(fill_color_string)
    border_color = color_from_clewin_string(border_color_string)

    layer = CleWin_layer(
        layer_name=name,
        layer_alias=alias,
        layer_index=index,
        fill_color=fill_color,
        border_color=border_color,
    )

    return layer


def plotLayers(layers: List[CleWin_layer], window_size: int = 10_000_000, alpha=0.5):
    """
    Shows a preview of the masks for the different layers in a matplotlib window.
    Note that the window size is in nm as with the rest of the library (for obvious reasons)

    Also note that the the resulting layer will be one with alpha = 1. A lower alpha is used for the preview to
    make it easier to see the different layers stacked. This has the unfortunate side effect of making wires look
    like they are spotted and ugly, but this is not the case when printed. This is due to the way matplotlib handles
    transparency and absolute sizing of shapes in the plot. A more thoughtful implementation of this function would
    probably fix this, but it is not a priority.

    Args:
    -----
    layers: List[CleWin_layer]
        The layers to plot
    window_size: int
        The side-length of the total window in nm
    alpha: float
        The alpha (transparency) value of the layers in the plot. Defaults to 0.5. The printed results will look like alpha = 1.

    Returns:
    --------
    fig: matplotlib.figure.Figure
        The figure object of the plot
    ax: matplotlib.axes.Axes
        The axes object of the plot
    """
    fig, ax = plt.subplots()
    ax.set_xlim(-window_size / 2, window_size / 2)
    ax.set_ylim(-window_size / 2, window_size / 2)

    ax.set_aspect("equal", "box")
    # May want to reconsider plotting in nm -> um
    ax.set_xlabel("x (nm)")
    ax.set_ylabel("y (nm)")
    for layer in layers:
        color = layer.fill_color.format_color_hex_rgb()
        for shape in layer.shapes:
            shape.color = color
            shape.add_shape_to_ax(ax=ax, alpha=alpha)
    plt.show()
    return fig, ax
