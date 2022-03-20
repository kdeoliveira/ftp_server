#!/usr/bin/python3.8
from io import BytesIO
import locale
import os
from re import S
from socket import socket
from ftp.cmd import arguments
from ftp.parser.message_type import MessageType, RequestType, ResponseType
from ftp.parser.message import Message, Util
from ftp.tcp.server import TcpServer

cmd = arguments.ParserArgs(2, helper = "Error", version="new version 1.0")

cmd.get_args()

arr = cmd.parameters(["-v"])



BASE_DIR = os.getcwd() + os.sep + "dir" + os.sep + "server" + os.sep


tcp_server = TcpServer("127.0.0.1")

def response_ok() -> bytes:
    message = Message(3, ResponseType.OK_PUT_CHANGE)
    message.parse("00000")
    return Util.serialize(message)

def response_get(file_name : str) -> bytes:
    message = Message(3, ResponseType.OK_GET)
    file_data = Util.str2bit(file_name, message.data[1].size, with_count=True)
    file_size = "00000000000000000000000000000000"

    message.parse(
    file_data + file_size
    )
    return Util.serialize(message)

def response_error_not_found():
    message = Message(3, ResponseType.ERROR_NOT_FOUND)
    message.parse("00000")
    return Util.serialize(message)

def response_error_no_change():
    message = Message(3, ResponseType.ERROR_NO_CHANGE)
    message.parse("00000")
    return Util.serialize(message)

def response_ok_help():
    message = Message(3, ResponseType.HELP)
    val = Util.str2bit("get put change bye",ResponseType.HELP.get_format()[1])
    message.parse(val)
    return Util.serialize(message)



def on_receive_put(addr, data : Message) -> bytes:
    
    result = Util.bit2byte(data)

    print(
        result[1].decode("utf-8"), int.from_bytes(result[2], byteorder="big")
    )

    return response_ok()


def on_receive_get(addr, data : Message) -> bytes:

    result = Util.bit2byte(data)

    file_name = BASE_DIR + result[1].decode("utf-8")


    #Remove embedded null pointer coming from raw data
    file_name = file_name.replace(chr(0), "")

    

    try:
        with open(file_name, "r") as open_file:
            f = open_file.read()
            print(f)
            
    except Exception as e:
        return response_error_not_found()

    return response_get(result[1].decode("utf-8"))


def on_receive_change(addr, data : Message) -> bytes:
    result = Util.bit2byte(data)

    file_name_old = BASE_DIR + result[1].decode("utf-8").replace(chr(0), '')
    file_name_new = BASE_DIR + result[3].decode("utf-8").replace(chr(0), '')



    try:
        os.rename(file_name_old, file_name_new)
    except Exception as e:
        return response_error_no_change()


    return response_ok()

def on_receive_help(addr, data : Message) -> bytes:
    result = Util.bit2byte(data)
    print("Help received: ", result)
    
    return response_ok_help()


tcp_server.on_receive(
    (RequestType.PUT , on_receive_put),
    (RequestType.GET, on_receive_get),
    (RequestType.CHANGE, on_receive_change),
    (RequestType.HELP, on_receive_help),
)

tcp_server.listen()