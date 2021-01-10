import time
from abc import ABC, abstractmethod
from math import radians, cos, sin
from random import random
from typing import List, Callable, Union

import keyboard

from lighting import Color, Gradient, scale_map, key_codes, special_keys, Mask, KeyIndex


class ColorFunction(ABC):
    """
    A ColorFunction provides a single method, get, in order to get a color.
    """

    @abstractmethod
    def get(self, *args, **kwargs) -> Color:
        pass


class PeriodicFunction(ColorFunction, ABC):
    def __init__(self, period: float, current_time: float = 0):
        """
        A PeriodicFunction is used to get a Color that changes across a period of time and loops back to the start at the end.
        """
        self.period = period
        self.current_time = current_time
        self.start_time = time.time() - current_time

    def update_time(self):
        self.current_time = time.time() - self.start_time
        while self.current_time > self.period:
            self.start_time += self.period
            self.current_time -= self.period


class SolidColor(ColorFunction):
    def __init__(self, color: Color):
        """
        A SolidColor only ever returns one Color.
        """
        self.color = color

    def __str__(self):
        return "SolidColor[{}]".format(self.color)

    def get(self, *args, **kwargs):
        return self.color


class PeriodicColor(PeriodicFunction):
    def __init__(self, gradient: Gradient, period: float, current_time: float = 0):
        """
        A PeriodicColor returns a Color that moves along a Gradient in a linear, repeating fashion.
        """
        super().__init__(period, current_time)
        self.gradient = gradient

    def __str__(self):
        return "PeriodicColor[flame_base_gradient:{}, period:{}, current_time:{}]".format(self.gradient, self.period,
                                                                                          self.current_time)

    def get(self, *args, **kwargs):
        self.update_time()
        return self.gradient.get_color(scale_map(self.current_time, 0, self.period, 0, len(self.gradient)))


class StaticGradient(ColorFunction):
    def __init__(self, gradient: Gradient):
        """
        A StaticGradient can be used to get a Color at a random or desired point on a Gradient.

        See the documentation for this class's get method.
        """
        self.gradient = gradient

    def __str__(self):
        return "StaticGradient[{}]".format(self.gradient)

    def get(self, *args, **kwargs):
        """
        If kwargs doesn't have a value associated to 't', gets a random color on the flame_base_gradient.
        """
        if 't' in kwargs:
            return self.get_color_at_t(kwargs['t'])
        return self.get_color_at_t(random())

    def get_color_at_t(self, t: float) -> Color:
        return self.gradient.get_color(t)


class ReactiveFunction(ColorFunction):
    def __init__(self, lower_function: Union[ColorFunction, Callable], key: str, decay: float = 0.25):
        """
        A Reactive Function is special for a ReactiveScheme.
        """
        if isinstance(lower_function, ColorFunction):
            def callable_function(*args, **kwargs) -> Color:
                return lower_function.get(*args, **kwargs)

            lower_function = callable_function
        self.lower_function = lower_function
        self.on = False
        self.decay = decay
        self.start_time = 0
        self.key = key

        self.on_press = self._callback_on_press
        self.on_release = self._callback_on_release

    def _callback_on_press(self, event: keyboard.KeyboardEvent):
        """
        Turns on the lighting.
        """
        if int(key_codes[self.key]) == int(event.scan_code):
            if self.key in special_keys["Right"]:
                if event.name.startswith("right") and not event.is_keypad:
                    self.on = True
                return
            if self.key in special_keys["Numpad"]:
                if event.is_keypad:
                    self.on = True
                return
            if not (event.is_keypad or event.name.startswith("right")):
                self.on = True

    def _callback_on_release(self, event: keyboard.KeyboardEvent):
        """
        Starts the decay of the lighting.
        """
        if int(key_codes[self.key]) == int(event.scan_code):
            if self.key in special_keys["Right"]:
                if event.name.startswith("right") and not event.is_keypad:
                    self.on = False
                    self.start_time = time.time()
                return
            if self.key in special_keys["Numpad"]:
                if event.is_keypad:
                    self.on = False
                    self.start_time = time.time()
                return
            if not (event.is_keypad or event.name.startswith("right")):
                self.on = False
                self.start_time = time.time()

    def reset(self):
        self.start_time = time.time()

    def get(self, *args, **kwargs) -> Color:
        cur_time = time.time()
        if self.on:
            scalar = 1
        elif cur_time - self.start_time <= self.decay:
            scalar = scale_map(cur_time - self.start_time, 0, self.decay, 1, 0)
        else:
            scalar = 0
        return self.lower_function(*args, **kwargs) * scalar

    def __str__(self):
        return "{} {}".format(self.key, self.lower_function)

    def __repr__(self):
        return str(self)


def single_color(n: int, color: Color) -> List[SolidColor]:
    """
    Generates a list of n SolidColors.
    """
    out = [SolidColor(color)]
    return out * n


def gen_solid_gradient(width: int, height: int, gradient: Gradient, gradient_length: int, gradient_angle: float = 0) -> \
        List[SolidColor]:
    """
    Generates a flattened list of SolidColors that can be displayed as a static gradient across a grid of keys.
    :param width: the width of the grid to cover with the gradient
    :param height: the height of the grid to cover with the gradient
    :param gradient: the Gradient to be used to set the colors on the grid
    :param gradient_length: the length of the gradient (how stretched should it be)
    :param gradient_angle: a rotation angle for the grid
    """
    rads = radians(-gradient_angle)
    out = []
    for x in range(0, width):
        for y in range(0, height):
            i = min(int(round(abs(x * cos(rads) - y * sin(rads)))), gradient_length - 1)
            i = scale_map(i, 0, gradient_length - 1, 0, 1)
            out.append(SolidColor(gradient.get_color(i)))
    return out


def column_gradient(width: int, height: int, gradient: Gradient) -> List[SolidColor]:
    """
    An special case of gen_solid_gradient that spreads the Gradient vertically.
    """
    return gen_solid_gradient(width, height, gradient, width, 0)


def row_gradient(width: int, height: int, gradient: Gradient) -> List[SolidColor]:
    """
    An special case of gen_solid_gradient that spreads the Gradient horizontally.
    """
    return gen_solid_gradient(width, height, gradient, height, 90)


def uniform_periodic(n: int, gradient: Gradient, period: float) -> List[PeriodicColor]:
    """
    Generates a list of n PeriodicColors.
    """
    out = [PeriodicColor(gradient, period)]
    return out * n


def periodic_gradient(width: int, height: int, gradient: Gradient, period: float, gradient_length: int,
                      gradient_angle: float = 0, reverse_direction: bool = False) -> List[PeriodicColor]:
    """
    Generates a flattened list of PeriodicColors that can be displayed as a moving gradient across a grid of keys.
    :param width: the width of the grid to cover with the gradient
    :param height: the height of the grid to cover with the gradient
    :param gradient: the Gradient to be used to set the colors on the grid
    :param period: the time it takes for the gradient to make one revolution
    :param gradient_length: the length of the gradient (how stretched should it be)
    :param gradient_angle: a rotation angle for the grid
    :param reverse_direction: reverses the direction the gradient seems to move in
    """
    rads = radians(-gradient_angle)
    out = []
    for x in range(0, width):
        for y in range(0, height):
            i = min(int(round(abs(x * cos(rads) - y * sin(rads)))), gradient_length - 1)
            i = scale_map(i, 0, gradient_length - 1, 0, period)
            if reverse_direction:
                i = period - i
            out.append(PeriodicColor(gradient, period, i))
    return out


def combine_keys_and_functions(functions: List[ColorFunction]):
    return dict(zip(list(KeyIndex(key, False) for key in Mask.ALL), functions))
