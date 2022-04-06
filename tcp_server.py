#!/usr/bin/python3.8

##
# @file tcp_server.py
#
# @brief Main TCP server application which contains the implementation of the server-end of this FTP service. All protocols and file handling is defined in this file. 
#
#
# @section author_doxygen_example Author(s)
# - Created by Kevin de Oliveira on 04/01/2022.
# - Student ID: 40054907
#
# Copyright (c) 2022 Kevin de Oliveira.  All rights reserved.


import os
from re import S
from socket import socket

import bitarray
from ftp.cmd import arguments
from ftp.parser.message_type import MessageType, RequestType, ResponseType
from ftp.parser.message import Message, Util
from ftp.tcp.server import TcpServer


server_dir = "server"


BASE_DIR = os.getcwd() + os.sep + "dir" + os.sep + server_dir + os.sep


def response_ok() -> bytes:
    message = Message(3, ResponseType.OK_PUT_CHANGE)
    message.parse("00000")
    return Util.serialize(message)

def response_get(file_name : str, size : int, payload: str) -> bytes:
    message = Message(3, ResponseType.OK_GET)
    file_data = Util.str2bit(file_name, ResponseType.OK_GET.get_format()[1], with_count=True)
    file_size = bitarray.util.int2ba(size, length=32, endian="big").to01()
    message.parse(
    file_data + file_size
    )

    message.add_payload(payload)
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

    file_name = result[1].decode("utf-8").replace(chr(0), "")

    try:
        with open(BASE_DIR + file_name, "w") as f:
            f.write(result[-1].decode("utf-8").replace(chr(0), ""))

    except Exception:
        # @brief Although no response type is defined for PUT errors in the project description, excpetions may still occur if server has not enough privilege for accessing file or f.write fails.
        # Sending an ERROR_NO_CHANGE response in case the above issue happends
        return response_error_no_change()

    return response_ok()


def on_receive_get(addr, data : Message) -> bytes:

    result = Util.bit2byte(data)

    file_name = BASE_DIR + result[1].decode("utf-8")

    # @brief Remove embedded null pointer coming from raw data
    file_name = file_name.replace(chr(0), "")

    

    try:
        with open(file_name, "r") as open_file:
            f = open_file.read()
            size = os.path.getsize(file_name)
            
        return response_get(result[1].decode("utf-8").replace(chr(0), ""), size, f)
            
    except Exception as e:
        return response_error_not_found()



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
    return response_ok_help()




arg_helper = """usage: tcp_server [-a address] [-p port] [-f base_folder] [-F absolute_folder] [-v | --version] [-h | --help | -?]

This are the commands used:
\t-d\t\t Activate debug mode
\t-a address\t\t Set address of this server (default: 127.0.0.1)
\t-p port\t\t\t Set port number of this server (default: 1025)
\t-f base_folder\t\t Set relative base path of the FTP server (default: /dir/server)
\t-F absolute_folder\t Set absolute base path of the FTP server (default: $pwd)"""

if __name__ == "__main__":

    cmd = arguments.ParserArgs(helper = arg_helper, version="tcp_server version 1.0")

    cmd.get_args()

    params = cmd.parameters(["-a", "-p", "-f", "-F", "-d"])

    if "-f" in params:
        server_dir = params["-f"]
    elif "-F" in params:
        BASE_DIR = params["-F"]
    
    tcp_server = TcpServer("127.0.0.1", **params)

    

    tcp_server.on_receive(
    (RequestType.PUT , on_receive_put),
    (RequestType.GET, on_receive_get),
    (RequestType.CHANGE, on_receive_change),
    (RequestType.HELP, on_receive_help),
    )

    tcp_server.listen()