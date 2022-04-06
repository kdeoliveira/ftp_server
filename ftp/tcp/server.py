##
# @file server.py
#
# @brief TCP Server logic and algorithm
#
#
# @section author_doxygen_example Author(s)
# - Created by Kevin de Oliveira on 04/01/2022.
# - Student ID: 40054907
#
# Copyright (c) 2022 Kevin de Oliveira.  All rights reserved.

from ast import arg
import pickle
import socket as sok
import sys
from threading import Thread
from types import FunctionType
from typing import Any, Callable, List, Tuple
from bitarray import util

from ftp.parser.message import Message, Util
from ftp.parser.message_type import MessageType, RequestType, ResponseType


class TcpServer():
    _DEFAULT_PORT = 1025
    _MAX_BUFFER = 4096

    def __init__(self, ip_addr, **kwargs) -> None:
        """!
        TCP Server interface that creates a new socket given the ip address provided for FTP communication purposes

        @param ip_addr: str     IP address which the TCP service would be listening to
        @param -p: int          Port value which socket will bind its connection
        @param -a: str          IP address that TCP service will be using

        @return TcpServer
        """
        self._debug = False
        self.thread = None
        self.socket = sok.socket(sok.AF_INET, sok.SOCK_STREAM)
        self.socket.setsockopt(sok.SOL_SOCKET, sok.SO_REUSEADDR, 1)
        for k,v in kwargs.items():
            if "-p" in k:
                self._DEFAULT_PORT = int(v)
            elif "-a" in k:
                ip_addr = v
            elif "-d" in k:
                self._debug = True
        self.socket.bind( (ip_addr, self._DEFAULT_PORT) )
        self.ip_address = ip_addr
        self.recv_functions : List[Tuple[RequestType, FunctionType]] = []

        self.is_connected = False

    def _init_app(self) -> str:
        """!
        Initial message printed into command-line when TCP service is initiated
        """
        return """-- FTP Server initializing on {ip}:{port}
-- Version 1.0.0 by Kevin de Oliveira
-- README contains a list of available commands and some concepts guiding""".format(ip = self.ip_address, port = self._DEFAULT_PORT)

    def listen(self):
        """!
        Starts a new threded TCP service by connecting to the respective server.

        @return None
        """
        self.socket.listen()
        print(self._init_app())
        if self._debug:
            print("Debug mode ON")
        while True:
            try:
                conn, addr = self.socket.accept()
                self.thread = Thread(target=self.handle_listen, args=(conn, addr))
                self.is_connected = True
                self.thread.start()

                # For non concurrent connection, join current thread so loop awaits for any active connection to be terminated before connecting any other socket
                # if self.thread:
                #     self.thread.join()
            except KeyboardInterrupt:
                    print("Closing server")
                    self.is_connected = False
                    self.socket.close()
                    return
            except BlockingIOError:
                print("EAGAIN error")
                continue

        

    def handle_listen(self, conn : sok.socket, addr : sok.AddressInfo):
        """!
        Internal function that is responsible for parsing any incoming and outgoing message sent to the TCP socket
        
        @return None
        """
        print("""> New connection {addr}:{port}""".format(addr = addr[0], port=addr[1]))

        while self.is_connected:
            try:
                # Socket is only able to receive MAX_BUFFER;
                # Therefore, ensure that maximum packet sent is no longer then _MAX_BUFFER or set socket to nonblocking -> socket.setblocking(False)
                # Otherwise, wait for any possible subsequent packet receival (parallel or different loop)                
                data = conn.recv(self._MAX_BUFFER)
                if not data:
                    print("Closing connection with:", addr)
                    return None
                if self._debug:
                    print("[DEBUG]", data)
                out = self.parse_packet(data)

                for x in self.recv_functions:
                    if(x[0] == out.type):
                        _data_send = x[1](addr, out)
                        if self._debug:
                            print("[DEBUG]", _data_send)
                        conn.sendto(_data_send, addr)


            except (BrokenPipeError, ConnectionResetError) as e:
                print(e, addr)
            except ValueError:
                message = Message(3, ResponseType.ERROR_UNKNOWN)
                message.parse("00000")
                conn.sendto( Util.serialize(message) , addr )
            except KeyboardInterrupt:
                return
            

    def on_receive(self, *args : Callable[[sok.AddressInfo, Message], bytes]):
        """!
        Attach a callback that is called when a message is received

        @param *args: List[Callable[[sok.AddressInfo, Message], bytes]] List of callable objects containing its Method type and respective callback function
        """
        for x in args:
            self.recv_functions.append(x)

    @staticmethod
    def parse_packet(data : bytes) -> Message:
        """!
        Deserializes incoming byte received by the TCP socket

        @param data: bytes  Byte object received by socket

        @return Message: object
        """
        return Util.deserialize(data, MessageType.REQUEST)

    


