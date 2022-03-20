#!/usr/bin/python3.8

import socket
import sys
from typing import List
import bitarray
from bitarray import util
from ftp.parser.message import Message, Util

from ftp.parser.packet import packet

from ftp.parser.message_type import MessageType, MethodType, RequestType
from ftp.tcp.client import TcpClient
client = TcpClient("127.0.0.1")

def on_send_put(inp : List[str], type: MethodType) -> bytes:
    message = Message(3, type)
    
    file_data = Util.str2bit(inp[1], message.data[1].size, with_count=True)
    file_size = "00000000000000000000000000000000"

    message.parse(
    file_data + file_size
    )

    return Util.serialize(message)


def on_send_get(inp : List[str], type: MethodType) -> bytes:
    message = Message(3, type)

    file_data = Util.str2bit(inp[1], message.data[1].size, with_count=True)
    
    message.parse(file_data)
    return Util.serialize(message)


def on_send_change(inp : List[str], type: MethodType) -> bytes:
    message = Message(3, type)
    file_data_old = Util.str2bit(inp[1], message.data[1].size, with_count=True)
    file_data_new = Util.str2bit(inp[2], message.data[3].size, with_count=True, size_count=8)
    message.parse(
    file_data_old + file_data_new
    )

    return Util.serialize(message)

def on_send_help(inp : List[str], type: MethodType) -> bytes:
    message = Message(3, type)

    message.parse("00000")

    return Util.serialize(message)

client.on_send(
    (RequestType.PUT, on_send_put),
    (RequestType.GET, on_send_get),
    (RequestType.CHANGE, on_send_change),
    (RequestType.HELP, on_send_help)
)

client.connect()




