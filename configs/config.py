from abc import ABC, abstractmethod
from typing import Callable, Any, List

from backend.utils import CombineType, Mask
from frontend.lighting.lightingschemes import LightingScheme, CombiningScheme


class Layer:
    def __init__(self, scheme_getter, combine_type: CombineType = CombineType.Overlay, mask: Mask = Mask.ALL):
        self.scheme_getter = scheme_getter
        self.combine_type = combine_type
        self.mask = mask


def layer(combine_type:CombineType = CombineType.Overlay, mask: Mask = Mask.ALL):
    def decorator(func):
        return Layer(func, combine_type, mask)

    return decorator


class ConfigMeta(type):
    def __new__(mcs, *args, **kwargs):
        layers = {}

        new_cls = super().__new__(mcs, *args, **kwargs)
        for base in reversed(new_cls.__mro__):
            for elem, value in base.__dict__.items():
                if elem in layers:
                    del layers[elem]

                is_static_method = isinstance(value, staticmethod)
                if is_static_method:
                    value = value.__func__
                if isinstance(value, Layer):
                    if is_static_method:
                        raise TypeError(f"Layer method {elem} cannot be a staticmethod")
                    layers[elem] = value

        new_cls.__layers__ = list(layers.values())

        return new_cls


class Config(metaclass=ConfigMeta):
    def get_scheme(self) -> CombiningScheme:
        scheme = CombiningScheme()

        for l in self.__layers__:
            scheme.add_scheme(l.scheme_getter(self), l.combine_type, l.mask)

        return scheme
