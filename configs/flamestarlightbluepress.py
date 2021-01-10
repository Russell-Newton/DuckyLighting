import configs.config as config
from backend.utils import key_grid_by_col, GradientKeyPoint, Color, Gradient, CombineType, Mask
from frontend.lighting.colorfunctions import combine_keys_and_functions, column_gradient
from frontend.lighting.colorpalettes import NoisePalette
from frontend.lighting.lightingschemes import FunctionScheme, NoiseScheme, ReactiveScheme, SolidColorScheme
import numpy as np


class FSBPConfig(config.Config):
    def __init__(self):
        super().__init__()
        self.shape = np.shape(key_grid_by_col)

    @config.layer()
    def flame_base(self):
        flame_base_colors = [
            GradientKeyPoint(Color(255, 175, 0), 1),
            GradientKeyPoint(Color(255, 0, 0), 0),
        ]
        flame_base_gradient = Gradient(flame_base_colors, True)
        flame_base_scheme = FunctionScheme(
            combine_keys_and_functions(column_gradient(self.shape[0], self.shape[1], flame_base_gradient)))

        return flame_base_scheme

    @config.layer(combine_type=CombineType.Subtract)
    def flame_flicker(self):
        flame_flicker_colors = [
            GradientKeyPoint(Color(0, 0, 0), 0),
            GradientKeyPoint(Color(127, 127, 127), 1)
        ]
        flame_flicker_palette = NoisePalette(Gradient(flame_flicker_colors), speed=0.1)
        flame_flicker_scheme = NoiseScheme(flame_flicker_palette)

        return flame_flicker_scheme

    @config.layer(combine_type=CombineType.Subtract)
    def flame_dampen(self):
        flame_dampen_colors = [
            GradientKeyPoint(Color(180, 180, 180), 0),
            GradientKeyPoint(Color(130, 130, 175), 0.1),
            GradientKeyPoint(Color(0, 0, 0), 1)
        ]
        flame_dampen_gradient = Gradient(flame_dampen_colors)
        flame_dampen_scheme = FunctionScheme(
            combine_keys_and_functions(column_gradient(self.shape[0], self.shape[1], flame_dampen_gradient)))

        return flame_dampen_scheme

    @config.layer(mask=Mask.FUNCTION + ['Space'])
    def starlight(self):
        starlight_chance = 0.125

        starlight_colors = [
            GradientKeyPoint(Color(0, 0, 0), 0),
            GradientKeyPoint(Color(0, 0, 0), 1 - starlight_chance),
            GradientKeyPoint(Color(100, 25, 127), 1 - starlight_chance),
            GradientKeyPoint(Color(200, 50, 255), 1)
        ]
        return NoiseScheme(NoisePalette(Gradient(starlight_colors), speed=0.05, scale=115))

    @config.layer()
    def reactive_blue(self):
        reactive_scheme = ReactiveScheme(SolidColorScheme(Color(80, 0, 255)), 0.4)
        return reactive_scheme
