from typing import List, Tuple, Dict, Optional

import logging

from keyboards.hid import Enumeration, HIDDevice, HIDException


class Packet:
    def __init__(self, outbound: bool, data: bytearray, report_id: int = 0):
        """
        A Packet contains all the information required for sending and receiving information to and from a HID.
        :param outbound: outbound = True, inbound = False
        :param data: the data contained in the Packet
        :param report_id: the report id of the Packet (important for sending and checking recieved packets)
        """
        self.outbound = outbound
        self.data = data
        self.report_id = report_id

    def __repr__(self) -> str:
        return f"Packet[\n" \
               f"       Outbound:{self.outbound},\n" \
               f"       Data:    {self.data.hex()}\n" \
               f"       Report ID:    {self.report_id}\n" \
               f"      ]"

    def __str__(self) -> str:
        predicate = "I"
        if self.outbound:
            predicate = "O"
        return f"{predicate} {self.data.hex()}"

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Packet):
            raise TypeError(f"{o.__class__.__name__} cannot be compared to a Packet!")

        return o.outbound == self.outbound \
               and o.data == self.data \
               and o.report_id == self.report_id

    @classmethod
    def build_packet(cls, direction: str, data_string: str):
        """
        Builds a packet from a direction ("I" or "O" and data string. The first byte of data is assumed to be the report id for the
        packet.
        """
        for_sending = (direction == "O")

        assert len(data_string) % 2 == 0

        data = bytearray.fromhex(data_string)
        report_id = data[0]
        return cls(for_sending, data[1:], report_id)


class PacketStream:
    def __init__(self, *, packets: List[Packet] = None, file_path: str = ''):
        """
        A PacketStream is a wrapper for a set of Packets. It can be initialized either with a list (default) or by a
        path to a file containing strings that can be deserialized into Packets (see preparedtraffic/Example.txt)
        """
        self.packets: List[Packet] = packets if packets is not None else (
            PacketStream._setup_packets_from_file(file_path) if file_path != '' else [])

    @staticmethod
    def _setup_packets_from_file(file_path: str) -> List[Packet]:
        packets = []

        with open(file_path, 'r') as file:
            for line in file:
                if line != "":
                    direction = line[0]
                    if direction in ("I", "O"):
                        data_string = line[2:-1]
                        packets.append(Packet.build_packet(direction, data_string))

        print(f"PacketStream {file_path} parsed correctly.")
        logging.info(f"PacketStream {file_path} parsed correctly.")

        return packets

    def __str__(self) -> str:
        out = ""
        for packet in self.packets:
            out += str(packet) + "\n"

        return out

    def __repr__(self) -> str:
        out = "PacketStream[\n"
        for packet in self.packets:
            out += repr(packet) + "\n"
        out += "]"

        return out

    def __iter__(self):
        return (packet for packet in self.packets)


class HIDHandler:
    def __init__(self, vendor_id: int, product_id: int, usage: int, usage_page: int):
        """
        A HIDHandler is the direct interface to a HID. To make the connection to the physical device, a handle
        is found and opened for the first device that matches the passed in vendor id, product id, usage, and usage
        page.

        Packets are sent to and received from the HID through instances of this class.
        """
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.usage = usage
        self.usage_page = usage_page
        self.device: Optional[HIDDevice] = None

        self._setup()

    def __del__(self):
        self.device.close()

    def _setup(self) -> None:
        self.device = \
            Enumeration(vid=self.vendor_id,
                        pid=self.product_id).find(usage_page=self.usage_page,
                                                  usage=self.usage)[0]
        self.device.open()
        self.device.set_nonblocking(True)
        # print(f"Device: vid/pid: {self.device.vendor_id}/{self.device.product_id}\n"
        #       f"  path:          {self.device.path}\n"
        #       f"  serial_number: {self.device.serial_number}\n"
        #       f"  usage_page:    {self.device.usage_page}\n"
        #       f"  usage:         {self.device.usage}\n"
        #       f"  Manufacturer:  {self.device.manufacturer_string}\n"
        #       f"  Product:       {self.device.product_string}")

    async def send(self, bytes_to_send: bytearray, report_id: int) -> int:
        """
        Sends data to the HID.

        :param bytes_to_send: a bytearray of the data to send
        :param report_id: the report id of the data to send
        :return: the number of bytes actually sent (including the report id)
        :raises HIDException: if there is an error sending the packet data
        """
        try:
            return self.device.write(bytes_to_send, report_id)
        except HIDException as e:
            logging.warning(f"Error sending packet: {bytes_to_send}")
            print(f"Error sending packet: {bytes_to_send}")
            raise e

    async def recv(self, length: int = 64) -> bytearray:
        """
        Waits for data to be sent from the HID.

        :param length: how much data to read, in bytes (defaults to 64)
        :return: the data read from the device, including the report_id, if used
        """
        return self.device.read(length)


class PacketSender:
    def __init__(self, handler: HIDHandler, **prepared_traffic_files: str):
        """
        A PacketSender manages the Packets sent to and received from a HIDHandler. Its purpose is to execute
        PacketStreams through the passed in HIDHandler. It also allows for prepared, constant PacketStreams to be sent
        through the HIDHandler.

        :param handler:
        :param prepared_traffic_files: a dictionary of file paths to parsable traffic files that get converted to
        PacketStreams
        """
        self.handler = handler
        self._prepared_traffic: Dict[str, PacketStream] = PacketSender._setup_prepared_traffic(
            prepared_traffic_files)

    @staticmethod
    def _setup_prepared_traffic(traffic_files: Dict[str, str]) -> Dict[str, PacketStream]:
        prepared_traffic: Dict[str, PacketStream] = {}
        for key, path in traffic_files.items():
            prepared_traffic[key] = PacketStream(file_path=path)

        return prepared_traffic

    async def execute_packet_stream(self, packet_stream: PacketStream) -> Tuple[int, int]:
        """
        Executes a PacketStream.
        :return: (number of successful packet executions, number of failed packet executions)
        """
        successes = 0
        failures = 0

        for packet in packet_stream:
            result = await self._handle_packet(packet)

            if result:
                successes += 1
            else:
                failures += 1

        return successes, failures

    async def execute_prepared_traffic(self, prepared_traffic: str) -> None:
        """
        Execute a prepared PacketStream by name.
        :param prepared_traffic: the name of the PacketStream (passed in as the key in **prepared_traffic_files)
        """
        await self.execute_packet_stream(self._prepared_traffic[prepared_traffic])

    async def _handle_packet(self, packet: Packet) -> bool:
        """
        Handles Packet execution.
        :return: True if the execution is determined to have been successful
        """
        if packet.outbound:
            return await self.handler.send(packet.data, packet.report_id) - 1 == len(packet.data)
        else:
            returned_data = await self.handler.recv()
            return packet == Packet(False, returned_data[1:], returned_data[0])
