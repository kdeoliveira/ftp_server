#!/usr/bin/python3.8

import os
import socket
import sys
from typing import List
import bitarray
from bitarray import util
from ftp.parser.message import Message, Util

from ftp.parser.packet import packet

from ftp.parser.message_type import MessageType, MethodType, RequestType, ResponseType
from ftp.tcp.client import TcpClient

BASE_DIR = os.getcwd() + os.sep + "dir" + os.sep + "client" + os.sep


client = TcpClient("127.0.0.1")

def on_send_put(inp : List[str], type: MethodType) -> bytes:
    message = Message(3, type)

    try:
        with open(BASE_DIR + inp[1], "r") as f:
            payload = f.read()
            size = os.path.getsize(BASE_DIR + inp[1])
    except Exception as e:
        raise ValueError("cannot send file")

    
    file_data = Util.str2bit(inp[1], message.data[1].size, with_count=True)
    file_size = bitarray.util.int2ba(size, length=32, endian='big').to01()

    message.parse(
    file_data + file_size
    )

    message.add_payload(payload)


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
    (RequestType.HELP, on_send_help),
)


def on_response_put_change(message : Message) :
    return

def on_response_get(message: Message) :
    val = Util.bit2byte(message)

    file_name = val[1].decode("utf-8").replace(chr(0), "")

    with os.scandir(BASE_DIR) as dir:
        flag : bool = False
        for x in dir:
            if x.name == file_name:
                flag = True
        
        if flag:
            ch : str = ''
            while ch not in ["y", "n"]:
                ch = input(file_name + " already exists. Do you want to overwrite? (y/n) ")
    try:
        if ch == "y":
            with open(BASE_DIR + file_name, "w") as f:
                f.write(val[-1].decode("utf-8").replace(chr(0), ""))

    except Exception as e:
        print(e)

def on_response_help(message: Message):
    val = Util.bit2byte(message)
    print(val[1].decode("utf-8").replace(chr(0), ""))

def on_response_unknown(message: Message):
    print("unknown command")

def on_response_not_found(message: Message):
    print("file not found")

def on_response_no_change(mesage : Message):
    print("operation failed")


client.on_response(
    (ResponseType.OK_PUT_CHANGE, on_response_put_change),
    (ResponseType.OK_GET, on_response_get),
    (ResponseType.HELP, on_response_help),
    (ResponseType.ERROR_UNKNOWN, on_response_unknown),
    (ResponseType.ERROR_NOT_FOUND, on_response_not_found),
    (ResponseType.ERROR_NO_CHANGE, on_response_no_change),
)
client.connect()




