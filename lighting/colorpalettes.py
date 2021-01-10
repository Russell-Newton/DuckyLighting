import time
from typing import Dict

import numpy as np

from lighting import ColorFunction, letters, Gradient, Color, KeyIndex


class NoisePalette:

    def __init__(self, color_palette: Gradient, speed: float = 0.1, scale: float = 120, smoothing: float = 0):
        """
        A NoisePalette compacts some noise creation data for a NoiseScheme.

        :param color_palette: should only have GradientKeyPoints with t on [0.0, 1.0]
        :param speed: a higher speed results in faster shifting colors
        :param scale: scale determines how "zoomed out" the noise is (lower scale means bigger blobs, high scale means
        smaller blobs)
        :param smoothing: smoothing can reduce artifacts at lower speeds (clamped on [0.0, 1.0])
        """
        self.color_palette = color_palette
        self.speed = speed
        self.scale = scale
        self.smoothing = min(max(smoothing, 0), 1)

    def get_color(self, proportion: float) -> Color:
        return self.color_palette.get_color(proportion)


class WordPalette:

    def __init__(self, color_functions: Dict[KeyIndex, ColorFunction], word: str, step_time: float = 0.1):
        """
        A WordPalette compacts some word representation data for a WordScheme.

        :param color_functions: underlying functions to light up
        :param word: a word or phrase to display by a WordScheme
        :param step_time: how often to slide the letters
        """
        self.functions = color_functions
        self.map = letters.from_string(word)
        self.step_time = step_time
        self.start_time = time.time()

    def get_rolled_map(self) -> np.ndarray:
        """
        Determines the position of the map after having moved for some time since starting.
        """
        current_time = time.time() - self.start_time
        steps = int((current_time / self.step_time) % self.map.shape[0])
        return np.roll(self.map, -steps, axis=0)
