from lighting import CombiningScheme, CombineType, Mask


class Layer:
    def __init__(self, scheme_getter, combine_type: CombineType = CombineType.Overlay,
                 mask: Mask = Mask.ALL):
        """
        A class used by a Config's get_scheme() method. You shouldn't have to instantiate this.
        """
        self.scheme_getter = scheme_getter
        self.combine_type = combine_type
        self.mask = mask


def layer(combine_type: CombineType = CombineType.Overlay, mask: Mask = Mask.ALL):
    """
    Converts a method into a Layer for a Config. The method must take in no parameters and return a LightingScheme.
    :param combine_type: How to apply this layer on top of the other layers
    :param mask: Which keys to apply this layer to
    """

    def decorator(func):
        return Layer(func, combine_type, mask)

    return decorator


class ConfigMeta(type):
    """
    This metaclass sets up how a Config uses decorated methods to build a dictionary of layers. Don't instantiate this
    directly.
    """

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
    """
    A Config uses methods decorated with the layer() decorator to define a CombiningScheme that can be retrieved with
    get_scheme(). Layer method setup should fit the following format:
    ::
        import configs.config as config
        @config.layer()
        def example_layer(self) -> LightingScheme:
            return SolidColorScheme(Color(0, 255, 0))

    The layering order is determined by the placement of the method in the Config's class declaration (i.e. an earlier
    defined method represents an earlier added layer).
    """

    def get_scheme(self) -> CombiningScheme:
        if not hasattr(self, "scheme"):
            self.scheme = CombiningScheme()

            for l in self.__layers__:
                self.scheme.add_scheme(l.scheme_getter(self), l.combine_type, l.mask)

        return self.scheme
