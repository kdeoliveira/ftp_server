#!/usr/bin/python3.8

##
# @file tcp_client.py
#
# @brief Main TCP client application which contains the implementation of the client-end of this FTP service. All protocols and file handling is defined in this file. 
#
#
# @section author_doxygen_example Author(s)
# - Created by Kevin de Oliveira on 04/01/2022.
# - Student ID: 40054907
#
# Copyright (c) 2022 Kevin de Oliveira.  All rights reserved.

import os
from ftp.cmd import arguments

from typing import List
import bitarray
from bitarray import util
from ftp.parser.message import Message, Util

from ftp.parser.packet import packet

from ftp.parser.message_type import MessageType, MethodType, RequestType, ResponseType
from ftp.tcp.client import TcpClient

client_dir = "client"

BASE_DIR = os.getcwd() + os.sep + "dir" + os.sep + client_dir + os.sep




def on_send_put(inp : List[str], type: MethodType) -> bytes:
    message = Message(3, type)

    try:
        with open(BASE_DIR + inp[1], "rb") as f:
            payload = f.read()
            size = os.path.getsize(BASE_DIR + inp[1])
    except IndexError:
        # @brief if exception occurs during parsing of input, return as if the command syntax as invalid
        raise ValueError("invalid command")
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
    try:
        message = Message(3, type)
        file_data = Util.str2bit(inp[1], message.data[1].size, with_count=True)
        message.parse(file_data)
        return Util.serialize(message)
    except IndexError:
        # @brief if exception occurs during parsing of input, return as if the command syntax as invalid
        raise ValueError("invalid command")


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



def on_response_put_change(message : Message) :
    return

def on_response_get(message: Message) :
    val = Util.bit2byte(message)

    file_name = val[1].decode("utf-8").replace(chr(0), "")
    ch : str = ''
    with os.scandir(BASE_DIR) as dir:
        flag : bool = False
        for x in dir:
            if x.name == file_name:
                flag = True
        
        ##
        # @brief Checks if file already exists
        #

        if flag:
            while ch not in ["y", "n"]:
                ch = input(file_name + " already exists. Do you want to overwrite? (y/n) ")
    try:
        if ch == "y" or not flag:
            with open(BASE_DIR + file_name, "wb") as f:
                f.write(val[-1])

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



arg_helper = """usage: tcp_client [-a address] [-p port] [-f base_folder] [-F absolute_folder] [-v | --version] [-h | --help | -?]

This are the commands used:
\t-d\t\t Activate debug mode
\t-a address\t\t Set address of this client (default: 127.0.0.1)
\t-p port\t\t\t Set port number of this client (default: 1025)
\t-f base_folder\t\t Set relative base path of the FTP client (default: /dir/client)
\t-F absolute_folder\t Set absolute base path of the FTP client (default: $pwd)"""



if __name__ == "__main__":
    cmd = arguments.ParserArgs(helper = arg_helper, version="tcp_server version 1.0")

    cmd.get_args()

    params = cmd.parameters(["-a", "-p", "-f", "-F", "-d"])

    if "-f" in params:
        client_dir = params["-f"]
    elif "-F" in params:
        BASE_DIR = params["-F"]
    


    client = TcpClient("127.0.0.1", **params)

    client.on_send(
    (RequestType.PUT, on_send_put),
    (RequestType.GET, on_send_get),
    (RequestType.CHANGE, on_send_change),
    (RequestType.HELP, on_send_help),
    )

    client.on_response(
    (ResponseType.OK_PUT_CHANGE, on_response_put_change),
    (ResponseType.OK_GET, on_response_get),
    (ResponseType.HELP, on_response_help),
    (ResponseType.ERROR_UNKNOWN, on_response_unknown),
    (ResponseType.ERROR_NOT_FOUND, on_response_not_found),
    (ResponseType.ERROR_NO_CHANGE, on_response_no_change),
    )
    client.connect()