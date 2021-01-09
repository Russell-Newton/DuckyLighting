import colorsys
from enum import Enum
from itertools import chain
from typing import List, Tuple, Union

import numpy as np

# keyboard package key codes
key_codes = {
    "Escape": 0x01, "F1": 0x3b, "F2": 0x3c, "F3": 0x3d, "F4": 0x3e, "F5": 0x3f, "F6": 0x40, "F7": 0x41, "F8": 0x42,
    "F9": 0x43, "F10": 0x44, "F11": 0x57, "F12": 0x58, "PrintScreen": 0x37, "ScrollLock": 0x46, "Pause": 69,
    "Calc": -183, "Mute": -173, "VolumeDown": -174, "VolumeUp": -175,
    "SectionSign": 0x29, "1": 0x02, "2": 0x03, "3": 0x04, "4": 0x05, "5": 0x06, "6": 0x07, "7": 0x08, "8": 0x09,
    "9": 0x0a, "0": 0x0b, "-": 0x0c, "=": 0x0d, "Backspace": 0x0e, "Insert": 82, "Home": 71, "PageUp": 73,
    "NumLock": 69, "Divide": 0x35, "Multiply": 0x37, "Subtract": 74,
    "Tab": 0x0f, "Q": 0x10, "W": 0x11, "E": 0x12, "R": 0x13, "T": 0x14, "Y": 0x15, "U": 0x16, "I": 0x17, "O": 0x18,
    "P": 0x19, "[": 0x1a, "]": 0x1b, "BSlash": 0x2b, "Delete": 83, "End": 79, "PageDown": 81, "N7": 71, "N8": 72,
    "N9": 73, "Add": 78,
    "CapsLock": 0x3a, "A": 0x1e, "S": 0x1f, "D": 0x20, "F": 0x21, "G": 0x22, "H": 0x23, "J": 0x24, "K": 0x25, "L": 0x26,
    "Semicolon": 0x27, "'": 0x28, "Enter": 0x1c, "N4": 75, "N5": 76, "N6": 77,
    "LeftShift": 0x2a, "Z": 0x2c, "X": 0x2d, "C": 0x2e, "V": 0x2f, "B": 0x30, "N": 0x31, "M": 0x32, ",": 0x33,
    ".": 0x34, "FSlash": 0x35, "RightShift": 0x36, "UpArrow": 72, "N1": 79, "N2": 80, "N3": 81,
    "LeftControl": 0x1d, "LeftWindows": 91, "LeftAlt": 0x38, "Space": 0x39, "RightAlt": 0x38, "RightWindows": 92,
    "Function": 0x00, "RightControl": 29, "LeftArrow": 75, "DownArrow": 80, "RightArrow": 77, "N0": 82, "NDelete": 83,
    "RightEnter": 28
}

# keyboard package special keys
special_keys = {
    "Numpad": ["Divide", "Multiply", "NumLock", "N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8", "N9", "N0", "NDelete"],
    "Right": ["RightAlt", "RightControl", "RightEnter", "RightWindows", "RightArrow"]
}

key_count = len(key_codes) - 1

# Separated by rows, (0, 0) is top left
key_grid_by_row = [
    ["Escape", None, "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "PrintScreen",
     "ScrollLock", "Pause", "Calc", "Mute", "VolumeDown", "VolumeUp"],
    ["SectionSign", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Backspace", "Insert", "Home", "PageUp",
     "NumLock", "Divide", "Multiply", "Subtract"],
    ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "BSlash", "Delete", "End", "PageDown", "N7",
     "N8", "N9", "Add"],
    ["CapsLock", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Semicolon", "'", None, "Enter", None, None, None, "N4",
     "N5", "N6", None],
    ["LeftShift", None, "Z", "X", "C", "V", "B", "N", "M", ",", ".", "FSlash", None, "RightShift", None, "UpArrow",
     None,
     "N1", "N2", "N3", None],
    ["LeftControl", "LeftWindows", "LeftAlt", None, None, None, "Space", None, None, None, "RightAlt", "RightWindows",
     "Function", "RightControl", "LeftArrow", "DownArrow", "RightArrow", "N0", None, "NDelete", "RightEnter"]
]

# Separated by columns, (0, 0) is bottom left
key_grid_by_col: List[List[str]] = list(list(sub) for sub in np.rot90(key_grid_by_row, k=-1))


class CombineType(Enum):
    """
    Used to determine how LightingSchemes are combined in a CombiningScheme.
    ::
        Overlay: Completely overrides the existing Color with this one, unless this Color is 0.
        Add: Adds this Color onto the existing one.
        Subtract: Subtracts this Color from the existing one.
    """
    Overlay = 0
    Add = 1
    Subtract = 2


def flatten(grid: List[List[str]]) -> List[str]:
    """
    Flattens a 2D array of strings, used by LightingScheme and Mask.ALL.
    """
    return list(chain.from_iterable(grid))


def interpolate_single(v0: float, v1: float, t: float) -> float:
    """
    Performs linear interpolation between v0 and v1 at a certain t.
    """
    return (1 - t) * v0 + t * v1


def scale_map(x: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
    """
    This scales a passed input from one frame of reference to another. This is the same as the map function for an
    Arduino.
    """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def str_key_to_tuple(key_name: str, row_major: bool = False) -> Tuple[int, int]:
    """
    Converts a str key name to the tuple corresponding to its position, determined by row_major.
    """
    if row_major:
        grid = key_grid_by_row
    else:
        grid = key_grid_by_col
    for sub, i in zip(grid, range(len(grid))):
        for known, j in zip(sub, range(len(sub))):
            if key_name == known:
                return i, j
    return -1, -1


def tuple_key_to_string(key_coordinate: Tuple[int, int], row_major: bool = False) -> str:
    """
    Converts a tuple position to the key name corresponding with that position, determined by row_major.
    """
    if key_coordinate is not None:
        if row_major:
            return key_grid_by_row[key_coordinate[0]][key_coordinate[1]]
        return key_grid_by_col[key_coordinate[0]][key_coordinate[1]]
    return ""


class Mask(Enum):
    """
    Masks are used to filter which keys are used for an operation. Adding Masks creates a Union of the two. Subtracting
    a Mask from a Mask removes the Intersection between the two from the first Mask. Lists of strings can also be added
    and subtracted from Masks.
    """
    ALL = list(filter(lambda x: x is not None, flatten(key_grid_by_row)))
    WASD = ["W", "A", "S", "D"]
    FUNCTION = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"]
    NUMPAD = ["N0", "N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8", "N9", "Divide", "Multiply", "NumLock", "NDelete",
              "Subtract", "Add", "RightEnter"]

    def __new__(cls, keys: List[str], *args, **kwargs):
        assert isinstance(keys, list)
        keys = list(filter(lambda x: x is not None, keys))
        if len(keys) > 0:
            assert isinstance(keys[0], str)
        obj = object.__new__(cls)
        obj._value = keys
        return obj

    def __add__(self, other):
        if not (isinstance(other, Mask) or isinstance(other, list)):
            return NotImplemented
        if isinstance(other, list):
            return self.value + other
        return self.value + other.value

    def __sub__(self, other):
        if not (isinstance(other, Mask) or isinstance(other, list)):
            return NotImplemented
        out: list = self.value
        if isinstance(other, Mask):
            other = other.value
        for key in other:
            if key in out:
                out.remove(key)
        return Mask(out)

    def __radd__(self, other):
        if not (isinstance(other, Mask) or isinstance(other, list)):
            return NotImplemented
        return self + Mask(other)

    def __rsub__(self, other):
        if not (isinstance(other, Mask) or isinstance(other, list)):
            return NotImplemented
        return Mask(other) - self

    def __iter__(self):
        return iter(self.value)

    def __getitem__(self, item):
        return self.value[item]

    def __len__(self):
        return len(self.value)


class Color:
    """
    A Color supports a few basic mathematical operations:
    ::
        Color + Color : by-part addition
        Color - Color : by-part subtraction
        Color +/- int : Color +/- Color(int, int, int)
        ~Color        : Color(255, 255, 255) - Color
        Color * float : by-part scaling
    Every operation clamps the output Color components on [0, 255].
    """

    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b
        self.clamp()

    def clamp(self) -> None:
        """
        Clamps the components of this Color on [0, 255].
        """
        self.r = min(max(self.r, 0), 255)
        self.g = min(max(self.g, 0), 255)
        self.b = min(max(self.b, 0), 255)

    def is_zero(self) -> bool:
        """
        :return: True if all of this Color's components are 0.
        """
        if self.r == 0 and self.g == 0 and self.b == 0:
            return True
        return False

    def zero_out(self) -> None:
        """
        Sets all three of this Color's components to 0.
        """
        self.set_color_values(0, 0, 0)

    def set_color(self, color) -> None:
        """
        Sets all three components of this Color to the corresponding components of another Color.
        """
        self.set_color_values(color.r, color.g, color.b)

    def set_color_values(self, r, g, b) -> None:
        """
        Sets the r, g, and b components of this Color individually.
        """
        self.r = r
        self.g = g
        self.b = b
        self.clamp()

    def scale(self, scale_value: float) -> None:
        """
        Scale the r, g, and b values of this Color object.
        """
        self.r = int(round(self.r * scale_value))
        self.g = int(round(self.g * scale_value))
        self.b = int(round(self.b * scale_value))
        self.clamp()

    @staticmethod
    def to_hsv(rgb) -> Tuple[float, float, float]:
        """
        Converts a Color to its corresponding tuple in HSV space.
        """
        return colorsys.rgb_to_hsv(rgb.r / 255, rgb.g / 255, rgb.b / 255)

    @staticmethod
    def from_hsv(hsv: Tuple[float, float, float]):
        """
        Converts a tuple in HSV space to its corresponding Color.
        """
        rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
        return Color(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

    @staticmethod
    def interpolate(start, end, t: float, on_hsv: bool = False):
        """
        Performs linear interpolation between two Colors through RGB space or through HSV space (depending on on_hsv).
        """

        if on_hsv:
            start = Color.to_hsv(start)
            end = Color.to_hsv(end)
            return Color.from_hsv((interpolate_single(start[0], end[0], t), interpolate_single(start[1], end[1], t),
                                   interpolate_single(start[2], end[2], t)))
        return Color(int(interpolate_single(start.r, end.r, t)), int(interpolate_single(start.g, end.g, t)),
                     int(interpolate_single(start.b, end.b, t)))

    def __str__(self) -> str:
        return "Color[0x{}{}{}]".format(str(hex(self.r))[-2:], str(hex(self.g))[-2:], str(hex(self.b))[-2:])

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if isinstance(other, Color):
            return Color(self.r + other.r, self.g + other.g, self.b + other.b)
        return Color(self.r + other, self.g + other, self.b + other)

    def __sub__(self, other):
        if isinstance(other, Color):
            return Color(self.r - other.r, self.g - other.g, self.b - other.b)
        return Color(self.r - other, self.g - other, self.b - other)

    def __mul__(self, other):
        if not (isinstance(other, int) or isinstance(other, float)):
            return NotImplemented
        return Color(int(self.r * other), int(self.g * other), int(self.b * other))

    def __rsub__(self, other):
        return Color(other - self.r, other - self.g, other - self.b)

    def __radd__(self, other):
        return self + other

    def __rmul__(self, other):
        return self * other

    def __neg__(self):
        return 255 - self

    def __eq__(self, other):
        if not isinstance(other, Color):
            return NotImplemented
        return self.r == other.r and self.g == other.g and self.b == other.b

    def __ne__(self, other):
        if not isinstance(other, Color):
            return NotImplemented
        return not self.__eq__(other)

    def __invert__(self):
        return self.__neg__()

    def __hex__(self):
        return hex(int(self.__str__(), 16))

    def __iter__(self):
        return iter((self.r, self.g, self.b))

    def __getitem__(self, item):
        return tuple(self)[item]


class GradientKeyPoint:
    def __init__(self, color: Color, t: float):
        """
        A GradientKeyPoint is used by a Gradient to set the key interpolation points.
        """
        self.color = color
        self.t = t


class Gradient:
    def __init__(self, key_points: List[GradientKeyPoint], on_hsv: bool = False):
        """
        A Gradient is made up of GradientKeyPoints and can be used to find the color at some point between these points.
        A Gradient must have more than one GradientKeyPoint. If on_hsv is True,  interpolation will be performed in HSV
        space instead of RGB space.
        """
        assert len(key_points) > 1
        self.key_points = sorted(key_points, key=lambda point: point.t)
        assert self.key_points[-1].t > self.key_points[0].t
        self.on_hsv = on_hsv

    def get_color(self, t: float) -> Color:
        """
        Gets the Color at some point t on this Gradient.
        """
        i = 1
        prev_point = self.key_points[0]
        next_point = self.key_points[1]
        while t <= self.key_points[-1].t:
            if prev_point.t <= t <= next_point.t:
                break
            i += 1
            prev_point = next_point
            next_point = self.key_points[i]

        interp_t = (t - prev_point.t) / (next_point.t - prev_point.t)
        return Color.interpolate(prev_point.color, next_point.color, interp_t, self.on_hsv)

    def size(self) -> float:
        """
        :return: The distance from the first to the last GradientKeyPoint.
        """
        return self.key_points[-1].t - self.key_points[0].t

    def __len__(self):
        return self.size()


class KeyIndex:
    def __init__(self, index: Union[str, Tuple[int, int]], row_major: bool):
        """
        A KeyIndex allows for easy passing between str and position definitions for keys.
        :param index: either the key name or its position
        :param row_major: if the position definition is in row_major space
        """
        self.index = index
        self.row_major = row_major

    def __str__(self):
        if isinstance(self.index, str):
            return self.index

        return tuple_key_to_string(self.index, self.row_major)

    def __iter__(self):
        if isinstance(self.index, tuple):
            return self.index

        return iter(str_key_to_tuple(self.index, self.row_major))

    def __getitem__(self, item):
        return tuple(self)[item]

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash((self.index, self.row_major))
