import asyncio
import traceback

from keyboards import HIDHandler, PacketSender, PacketStream
from abc import ABC, abstractmethod
from lighting import Color, Mask, LightingScheme, CombiningScheme, CombineType, HookingScheme
from configs import Config

from typing import Dict, List, Callable, Optional
import keyboard
import logging


class KeyData:
    def __init__(self, color: Color, packet_number: int, offset: int):
        """
        The KeyData class contains data that a KeyColorManager needs to create outbound packets to send to the
        RGBKeyboard.

        :param color: the current Color assigned to this key
        :param packet_number: the packet this key's data starts in
        :param offset: the offset in the packet this key's data starts in
        """
        self.color = color
        self.packet_number = packet_number
        self.offset = offset


class KeyColorManager(ABC):
    def __init__(self):
        """
        A KeyColorManager manages active key colors and determines how that information should be encoded into packets
        to send to the physical keyboard.

        An instance of a KeyColorManager is created by every RGBKeyboard.
        """
        self.keys: Dict[str, KeyData] = {}
        self._setup_keys()

    @abstractmethod
    def _setup_keys(self) -> None:
        """
        Used to initialize self.keys to be a Dict[str, KeyData]. Must be defined in a subclass.
        """
        raise NotImplementedError("Must initialize self.keys.")

    def set_key_color(self, key: str, color: Color) -> None:
        """
        Sets the color of a KeyData in self.keys.
        """
        self.keys[key].color = color

    def reset_colors(self) -> None:
        """
        Resets the color of every KeyData in self.keys to black (Color(0, 0, 0)).
        """
        for key, data in self.keys.items():
            data.color = Color(0, 0, 0)

    def apply_scheme(self, scheme: LightingScheme, mask: Mask = Mask.ALL, *args, **kwargs) -> None:
        """
        Applies a LightingScheme to every KeyData in self.keys.
        :param scheme: the LightingScheme to apply
        :param mask: the Mask to apply the scheme to (defaults to every key)
        :param args: any additional arguments to pass into LightingScheme::get_all_colors()
        :param kwargs: any additional keyword arguments to pass into LightingScheme::get_all_colors()
        """
        colors = scheme.get_all_colors(mask, *args, **kwargs)
        for key, color in colors.items():
            self.set_key_color(str(key), color)

    @abstractmethod
    def packets_to_send(self) -> PacketStream:
        """
        Constructs a PacketStream that contains all the KeyData information. This gets sent to the physical keyboard by
        the owning RGBKeyboard. Must be defined in a subclass.

        Determining the structure of the packets can be done by examining default communication behavior with a program
        like WireShark (https://www.wireshark.org) with USBPcap.
        """
        raise NotImplementedError("Must implement a way to turn self.keys into a PacketStream for sending.")


class RGBKeyboard(HIDHandler, PacketSender, ABC):
    def __init__(self, vid: int, pid: int, usage: int, usage_page: int, **prepared_traffic_files: str):
        """
        An RGBKeyboard declares methods and defines some default behaviors required to interface with a physical RGB
        keyboard, as long as its key colors can be set over a standard HID connection (USB, bluetooth untested).

        An RGBKeyboard, after initialized, can be used by calling the run() method, which starts an asyncio task (see
        method declaration for details). Prior to this, a Config can be set with set_config() and LightingScheme layers
        can be added and removed with add_layer(), remove_layer(), and reset_layers().

        If HookingSchemes are being used, any hooks are automatically added and removed as necessary.

        :param vid: the vendor id of the desired HID device
        :param pid: the product id of the desired HID device
        :param usage: the usage of the desired HID device
        :param usage_page: the usage page of the desired HID device
        :param prepared_traffic_files: file paths of prepared traffic, executed with
        """
        HIDHandler.__init__(self, vid, pid, usage, usage_page)
        PacketSender.__init__(self, self, **prepared_traffic_files)
        self.color_manager: Optional[KeyColorManager] = None
        self.initialized = False

        self._hooks_list: List[Callable[[keyboard.KeyboardEvent], None]] = []
        keyboard.hook(self._hook_callback)

        self.scheme: CombiningScheme = CombiningScheme()

    def __del__(self):
        keyboard.unhook_all()

    async def _main_loop(self) -> None:
        try:
            await self._init_connection()
            while True:
                await self.push()
        except (KeyboardInterrupt, Exception) as error:
            logging.error("Caught an error!", exc_info=(type(error), error, error.__traceback__))
            traceback.print_exception(type(error), error, error.__traceback__)
            await self._close_connection()

    def run(self) -> None:
        """
        Uses asyncio to run the main loop of the RGBKeyboard, which, by default resembles the following::

            call _init_connection()
            call push() until an Exception or KeyboardInterrupt is raised
            call _close_connection()

        Both _init_connection() and _close_connection() can be overridden to have unique behavior. By default, they
        allow push() to be used.

        This method should probably not be overridden, unless more precise control over the event loop is desired.
        """
        asyncio.run(self._main_loop())

    def add_layer(self, scheme: LightingScheme, combine_type: CombineType = CombineType.Overlay,
                  mask: Mask = Mask.ALL) -> None:
        """
        Adds a LightingScheme layer to the self.scheme.
        :param scheme: the LightingScheme to add
        :param combine_type: how this layer should be added on top of self.scheme
        :param mask: which keys this layer applies to
        """
        self.scheme.add_scheme(scheme, combine_type, mask)
        if isinstance(scheme, HookingScheme):
            self._add_hooks(scheme.hook)
        if isinstance(scheme, CombiningScheme) and len(scheme.hooks) != 0:
            self._add_hooks(*scheme.hooks)

    def remove_layer(self, scheme: LightingScheme) -> None:
        """
        Removes a LightingScheme layer from self.scheme.
        """
        self.scheme.remove_scheme(scheme)
        if isinstance(scheme, HookingScheme):
            self._remove_hooks(scheme.hook)
        if isinstance(scheme, CombiningScheme) and len(scheme.hooks) != 0:
            self._remove_hooks(*scheme.hooks)

    def reset_layers(self) -> None:
        """
        Removes all layers from self.scheme.
        """
        self.scheme.clear_schemes()
        self._hooks_list = []

    def set_config(self, config: Config) -> None:
        """
        Sets self.scheme to the CombiningScheme defined by the passed Config.
        """
        self.reset_layers()
        self.add_layer(config.get_scheme())

    async def push(self, mask: Mask = Mask.ALL, *args, **kwargs) -> None:
        """
        Sends the lighting information to the physical keyboard. Can only be called after _init_connection() is called.
        :param mask: which keys to recalculate the colors for
        :param args: any additional arguments to pass into LightingScheme::get_all_colors()
        :param kwargs: any additional keyword arguments to pass into LightingScheme::get_all_colors()
        :return:
        """
        if not self.initialized:
            raise NotImplementedError("RGBKeyboard connection not initialized!")

        self.color_manager.apply_scheme(self.scheme, mask, *args, **kwargs)
        packet_stream = self.color_manager.packets_to_send()
        await self.execute_packet_stream(packet_stream)

    async def _init_connection(self) -> None:
        if self.__class__ == RGBKeyboard:
            raise NotImplementedError("Must have something to initialize the HID connection.")
        self.initialized = True
        logging.info("Initializing connection")

    async def _close_connection(self) -> None:
        if self.__class__ == RGBKeyboard:
            raise NotImplementedError("Must have something to close the HID connection.")
        self.initialized = False
        logging.info("Closing connection")

    def _add_hooks(self, *hooks: Callable[[keyboard.KeyboardEvent], None]) -> None:
        self._hooks_list += hooks
        logging.info("Added hooks!")

    def _remove_hooks(self, *hooks: Callable[[keyboard.KeyboardEvent], None]) -> None:
        self._hooks_list -= hooks
        logging.info("Removed hooks!")

    def _hook_callback(self, event: keyboard.KeyboardEvent) -> None:
        """
        This method gets hooked to the keyboard, and calls any hooks supplied by HookingSchemes in self.scheme.
        """
        for hook in self._hooks_list:
            hook(event)
