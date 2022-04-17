



import unittest

from ftp.parser.message import Message, Util
from ftp.parser.message_type import MessageType, RequestType


class TestMessage(unittest.TestCase):
    def setUp(self) -> None:
        self.message = Message(3, RequestType.GET)
        self.bytes_to_be_parsed = b'\x00\x04\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
        return super().setUp()

    def test_header_size(self):
        expected_size = 3 +  sum(RequestType.GET.get_format())
        self.assertEqual(self.message.size,  expected_size )
    
    def test_has_payload(self):
        self.assertFalse(self.message.has_payload())

    def test_parse_message(self):
        temp_msg = Util.deserialize(self.bytes_to_be_parsed, MessageType.REQUEST)
        self.assertEqual(temp_msg.header.value().to01(), "001")

    def test_bit_conversion(self):
        temp_msg = Util.deserialize(self.bytes_to_be_parsed, MessageType.REQUEST)
        byte_list = Util.bit2byte(temp_msg)
        self.assertCountEqual(self.bytes_to_be_parsed[2:], byte_list[1])

    def test_01_conversion(self):
        filename_to_be_tested = "test_file_name.pdf"
        filename = Util.str2bit(filename_to_be_tested, 32*8, with_count=True)

        test_value = Message(3, RequestType.GET)
        test_value.parse(filename)

        val = Util.bit2byte(test_value)

        val_filename = val[1].decode("utf-8").replace(chr(0), "") # Remove null char

        self.assertEqual(val_filename, filename_to_be_tested)
        

        


