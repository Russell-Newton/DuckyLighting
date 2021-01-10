from keyboards import PacketStream, Packet, RGBKeyboard, KeyColorManager, KeyData
from typing import List
from lighting import Color
import asyncio

DUCKY_ONE_2_VID = 0x04d9
DUCKY_ONE_2_PID = 0x0348
DUCKY_ONE_2_USAGE_PAGE = 0xff00
DUCKY_ONE_2_USAGE = 1


class DuckyOne2RGBColorManager(KeyColorManager):
    """
    This KeyColorManager is specialized for the Ducky One2 RGB, 108-key US layout.
    """
    def _setup_keys(self):
        self.keys["Escape"] = KeyData(Color(0, 0, 0), 0, 0x08)
        self.keys["SectionSign"] = KeyData(Color(0, 0, 0), 0, 0x0b)
        self.keys["Tab"] = KeyData(Color(0, 0, 0), 0, 0x0e)
        self.keys["CapsLock"] = KeyData(Color(0, 0, 0), 0, 0x11)
        self.keys["LeftShift"] = KeyData(Color(0, 0, 0), 0, 0x14)
        self.keys["LeftControl"] = KeyData(Color(0, 0, 0), 0, 0x17)
        # 0 0x1a
        self.keys["1"] = KeyData(Color(0, 0, 0), 0, 0x1d)
        self.keys["Q"] = KeyData(Color(0, 0, 0), 0, 0x20)
        self.keys["A"] = KeyData(Color(0, 0, 0), 0, 0x23)
        # 0 0x26
        self.keys["LeftWindows"] = KeyData(Color(0, 0, 0), 0, 0x29)
        self.keys["F1"] = KeyData(Color(0, 0, 0), 0, 0x2c)
        self.keys["2"] = KeyData(Color(0, 0, 0), 0, 0x2f)
        self.keys["W"] = KeyData(Color(0, 0, 0), 0, 0x32)
        self.keys["S"] = KeyData(Color(0, 0, 0), 0, 0x35)
        self.keys["Z"] = KeyData(Color(0, 0, 0), 0, 0x38)
        self.keys["LeftAlt"] = KeyData(Color(0, 0, 0), 0, 0x3b)

        # Packet 1
        self.keys["F2"] = KeyData(Color(0, 0, 0), 1, 0x08)
        self.keys["3"] = KeyData(Color(0, 0, 0), 1, 0x0b)
        self.keys["E"] = KeyData(Color(0, 0, 0), 1, 0x0e)
        self.keys["D"] = KeyData(Color(0, 0, 0), 1, 0x11)
        self.keys["X"] = KeyData(Color(0, 0, 0), 1, 0x14)
        # 1 0x17
        self.keys["F3"] = KeyData(Color(0, 0, 0), 1, 0x1a)
        self.keys["4"] = KeyData(Color(0, 0, 0), 1, 0x1d)
        self.keys["R"] = KeyData(Color(0, 0, 0), 1, 0x20)
        self.keys["F"] = KeyData(Color(0, 0, 0), 1, 0x23)
        self.keys["C"] = KeyData(Color(0, 0, 0), 1, 0x26)
        # 1 0x29
        self.keys["F4"] = KeyData(Color(0, 0, 0), 1, 0x2c)
        self.keys["5"] = KeyData(Color(0, 0, 0), 1, 0x2f)
        self.keys["T"] = KeyData(Color(0, 0, 0), 1, 0x32)
        self.keys["G"] = KeyData(Color(0, 0, 0), 1, 0x35)
        self.keys["V"] = KeyData(Color(0, 0, 0), 1, 0x38)
        # 1 0x3b

        # Packet 2
        # 2 0x08
        self.keys["6"] = KeyData(Color(0, 0, 0), 2, 0x0b)
        self.keys["Y"] = KeyData(Color(0, 0, 0), 2, 0x0e)
        self.keys["H"] = KeyData(Color(0, 0, 0), 2, 0x11)
        self.keys["B"] = KeyData(Color(0, 0, 0), 2, 0x14)
        self.keys["Space"] = KeyData(Color(0, 0, 0), 2, 0x17)
        self.keys["F5"] = KeyData(Color(0, 0, 0), 2, 0x1a)
        self.keys["7"] = KeyData(Color(0, 0, 0), 2, 0x1d)
        self.keys["U"] = KeyData(Color(0, 0, 0), 2, 0x20)
        self.keys["J"] = KeyData(Color(0, 0, 0), 2, 0x23)
        self.keys["N"] = KeyData(Color(0, 0, 0), 2, 0x26)
        # 2 0x29
        self.keys["F6"] = KeyData(Color(0, 0, 0), 2, 0x2c)
        self.keys["8"] = KeyData(Color(0, 0, 0), 2, 0x2f)
        self.keys["I"] = KeyData(Color(0, 0, 0), 2, 0x32)
        self.keys["K"] = KeyData(Color(0, 0, 0), 2, 0x35)
        self.keys["M"] = KeyData(Color(0, 0, 0), 2, 0x38)
        # 2 0x3b

        # Packet 3
        self.keys["F7"] = KeyData(Color(0, 0, 0), 3, 0x08)
        self.keys["9"] = KeyData(Color(0, 0, 0), 3, 0x0b)
        self.keys["O"] = KeyData(Color(0, 0, 0), 3, 0x0e)
        self.keys["L"] = KeyData(Color(0, 0, 0), 3, 0x11)
        self.keys[","] = KeyData(Color(0, 0, 0), 3, 0x14)
        # 3 0x17
        self.keys["F8"] = KeyData(Color(0, 0, 0), 3, 0x1a)
        self.keys["0"] = KeyData(Color(0, 0, 0), 3, 0x1d)
        self.keys["P"] = KeyData(Color(0, 0, 0), 3, 0x20)
        self.keys["Semicolon"] = KeyData(Color(0, 0, 0), 3, 0x23)
        self.keys["."] = KeyData(Color(0, 0, 0), 3, 0x26)
        self.keys["RightAlt"] = KeyData(Color(0, 0, 0), 3, 0x29)
        self.keys["F9"] = KeyData(Color(0, 0, 0), 3, 0x2c)
        self.keys["-"] = KeyData(Color(0, 0, 0), 3, 0x2f)
        self.keys["["] = KeyData(Color(0, 0, 0), 3, 0x32)
        self.keys["'"] = KeyData(Color(0, 0, 0), 3, 0x35)
        self.keys["FSlash"] = KeyData(Color(0, 0, 0), 3, 0x38)
        # 3 0x3b

        # Packet 4
        self.keys["F10"] = KeyData(Color(0, 0, 0), 4, 0x08)
        self.keys["="] = KeyData(Color(0, 0, 0), 4, 0x0b)
        self.keys["]"] = KeyData(Color(0, 0, 0), 4, 0x0e)
        # 4 0x11
        # 4 0x14
        self.keys["RightWindows"] = KeyData(Color(0, 0, 0), 4, 0x17)
        self.keys["F11"] = KeyData(Color(0, 0, 0), 4, 0x1a)
        # 4 0x1d
        # 4 0x20
        # 4 0x23
        self.keys["RightShift"] = KeyData(Color(0, 0, 0), 4, 0x26)
        self.keys["Function"] = KeyData(Color(0, 0, 0), 4, 0x29)
        self.keys["F12"] = KeyData(Color(0, 0, 0), 4, 0x2c)
        self.keys["Backspace"] = KeyData(Color(0, 0, 0), 4, 0x2f)
        self.keys["BSlash"] = KeyData(Color(0, 0, 0), 4, 0x32)
        self.keys["Enter"] = KeyData(Color(0, 0, 0), 4, 0x35)
        # 4 0x38
        self.keys["RightControl"] = KeyData(Color(0, 0, 0), 4, 0x3b)

        # Packet 5
        self.keys["PrintScreen"] = KeyData(Color(0, 0, 0), 5, 0x08)
        self.keys["Insert"] = KeyData(Color(0, 0, 0), 5, 0x0b)
        self.keys["Delete"] = KeyData(Color(0, 0, 0), 5, 0x0e)
        # 5 0x11
        # 5 0x14
        self.keys["LeftArrow"] = KeyData(Color(0, 0, 0), 5, 0x17)
        self.keys["ScrollLock"] = KeyData(Color(0, 0, 0), 5, 0x1a)
        self.keys["Home"] = KeyData(Color(0, 0, 0), 5, 0x1d)
        self.keys["End"] = KeyData(Color(0, 0, 0), 5, 0x20)
        # 5 0x23
        self.keys["UpArrow"] = KeyData(Color(0, 0, 0), 5, 0x26)
        self.keys["DownArrow"] = KeyData(Color(0, 0, 0), 5, 0x29)
        self.keys["Pause"] = KeyData(Color(0, 0, 0), 5, 0x2c)
        self.keys["PageUp"] = KeyData(Color(0, 0, 0), 5, 0x2f)
        self.keys["PageDown"] = KeyData(Color(0, 0, 0), 5, 0x32)
        # 5 0x35
        # 5 0x38
        self.keys["RightArrow"] = KeyData(Color(0, 0, 0), 5, 0x3b)

        # Packet 6
        self.keys["Calc"] = KeyData(Color(0, 0, 0), 6, 0x08)
        self.keys["NumLock"] = KeyData(Color(0, 0, 0), 6, 0x0b)
        self.keys["N7"] = KeyData(Color(0, 0, 0), 6, 0x0e)
        self.keys["N4"] = KeyData(Color(0, 0, 0), 6, 0x11)
        self.keys["N1"] = KeyData(Color(0, 0, 0), 6, 0x14)
        self.keys["N0"] = KeyData(Color(0, 0, 0), 6, 0x17)
        self.keys["Mute"] = KeyData(Color(0, 0, 0), 6, 0x1a)
        self.keys["Divide"] = KeyData(Color(0, 0, 0), 6, 0x1d)
        self.keys["N8"] = KeyData(Color(0, 0, 0), 6, 0x20)
        self.keys["N5"] = KeyData(Color(0, 0, 0), 6, 0x23)
        self.keys["N2"] = KeyData(Color(0, 0, 0), 6, 0x26)
        # 6 0x29
        self.keys["VolumeDown"] = KeyData(Color(0, 0, 0), 6, 0x2c)
        self.keys["Multiply"] = KeyData(Color(0, 0, 0), 6, 0x2f)
        self.keys["N9"] = KeyData(Color(0, 0, 0), 6, 0x32)
        self.keys["N6"] = KeyData(Color(0, 0, 0), 6, 0x35)
        self.keys["N3"] = KeyData(Color(0, 0, 0), 6, 0x38)
        self.keys["NDelete"] = KeyData(Color(0, 0, 0), 6, 0x3b)

        # Packet 7
        self.keys["VolumeUp"] = KeyData(Color(0, 0, 0), 7, 0x08)
        self.keys["Subtract"] = KeyData(Color(0, 0, 0), 7, 0x0b)
        self.keys["Add"] = KeyData(Color(0, 0, 0), 7, 0x0e)
        # 7 0x11
        # 7 0x14
        self.keys["RightEnter"] = KeyData(Color(0, 0, 0), 7, 0x17)

    def packets_to_send(self) -> PacketStream:
        data_arrays: List[bytearray] = []
        packets: List[Packet] = []


        # ------------------------------------------ Apply packet metadata ------------------------------------------- #
        for i in range(8):
            data = bytearray(64)
            data[0] = 0x56
            data[1] = 0x42
            data[4] = 0x02
            if i == 7:
                data[5] = 0x06
            else:
                data[5] = 0x12
            data[6] = 18 * i
            data_arrays.append(data)

        # ---------------------------------------------- Apply key data ---------------------------------------------- #
        for name, key in self.keys.items():
            offsets = [key.offset + x for x in range(3)]

            for offset, color_byte in zip(offsets, key.color):
                packet = key.packet_number
                if offset >= 64:
                    offset -= 60
                    packet += 1

                data_arrays[packet][offset] = color_byte

        # -------------------------------------------- Initialize packets -------------------------------------------- #
        for data in data_arrays:
            packets.append(Packet(True, data, 0x1))
            packets.append(Packet(False, bytearray([0] * 64), 0x1))   # Allow for waiting for response

        return PacketStream(packets=packets)


class DuckyOne2RGB(RGBKeyboard):
    def __init__(self):
        """
        A DuckyOne2RGB is designed to communicate with a Ducky One2 RGB. By default, it makes use of the
        :class:`DuckyOne2RGBColorManager`.
        """
        super().__init__(DUCKY_ONE_2_VID, DUCKY_ONE_2_PID, DUCKY_ONE_2_USAGE, DUCKY_ONE_2_USAGE_PAGE,
                         initialize="preparedtraffic/DuckyOne2_Traffic_Init.txt",
                         exit="preparedtraffic/DuckyOne2_Traffic_Exit.txt")
        self.color_manager = DuckyOne2RGBColorManager()

    async def _init_connection(self):
        await super()._init_connection()
        await self.execute_packet_stream(self._prepared_traffic["initialize"])
        await asyncio.sleep(2)  # Pause before sending colors

    async def _close_connection(self):
        await super()._close_connection()
        await self.execute_packet_stream(self._prepared_traffic["exit"])


