import unittest

import bitarray

from ftp.parser.packet import packet


class TestPacket(unittest.TestCase):
    def setUp(self) -> None:
        self.packet = packet(5)
        return super().setUp()
    def test_max_size(self):
        self.assertEqual(self.packet.size, 5)

    def test_call(self):
        with self.assertRaises(ValueError):
            self.packet("000000")

    def test_to_bytes(self):
        self.assertIsInstance(self.packet.to_bytes(),bytes)

    def test_packet_value(self):
        self.packet("01100")
        temp = bitarray.bitarray("01100")

        self.assertEqual(self.packet.value(), temp)

    def test_set_size(self):
        self.packet.set_size(3)
        self.assertLess(self.packet.size, 5)