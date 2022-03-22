"""
TCP socket interface representing FTP server
"""

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
    _MAX_BUFFER = 1024

    def __init__(self, ip_addr, **kwargs) -> None:
        """
        TCP Server interface that creates a new socket given the ip address provided for FTP communication purposes

        Parameters
        ---
        ip_addr: str
            IP address which the TCP service would be listening to
        -p: int
            port value which socket will bind its connection
        -a: str
            new IP address that TCP service will be using
        
        """
        self.thread = None
        self.socket = sok.socket(sok.AF_INET, sok.SOCK_STREAM)
        self.socket.setsockopt(sok.SOL_SOCKET, sok.SO_REUSEADDR, 1)
        for k,v in kwargs.items():
            if "-p" in k:
                self._DEFAULT_PORT = int(v)
            elif "-a" in k:
                ip_addr = v
        self.socket.bind( (ip_addr, self._DEFAULT_PORT) )
        self.ip_address = ip_addr
        self.recv_functions : List[Tuple[RequestType, FunctionType]] = []

        self.is_connected = False

    def _init_app(self) -> str:
        """
        Initial message printed into command-line when TCP service is initiated
        """
        return """-- FTP Server initializing on {ip}:{port}
-- Version 1.0.0 by Kevin de Oliveira
-- README contains a list of available commands and some concepts guiding""".format(ip = self.ip_address, port = self._DEFAULT_PORT)

    def listen(self):
        """
        Starts a new threded TCP service by connecting to the respective server.
        """
        self.socket.listen()
        print(self._init_app())
        while True:
            try:
                conn, addr = self.socket.accept()
                self.thread = Thread(target=self.handle_listen, args=(conn, addr))
                self.is_connected = True
                self.thread.start()
                if self.thread:
                    self.thread.join()
            except KeyboardInterrupt:
                    print("Closing server")
                    self.is_connected = False
                    self.socket.close()
                    return

        

    def handle_listen(self, conn : sok.socket, addr : sok.AddressInfo):
        """
        Internal function that is responsible for parsing any incoming and outgoing message sent to the TCP socket
        """
        print("""> New connection {addr}:{port}""".format(addr = addr[0], port=addr[1]))
        while self.is_connected:
            try:
                data = conn.recv(self._MAX_BUFFER)
                if not data:
                    return None
                
                out = self.parse_packet(data)
                
                for x in self.recv_functions:
                    if(x[0] == out.type):
                        conn.sendto(x[1](addr, out), addr)


            except BrokenPipeError as e:
                print(e, addr)
            except ValueError:
                message = Message(3, ResponseType.ERROR_UNKNOWN)
                message.parse("00000")
                conn.sendto( Util.serialize(message) , addr )
            except KeyboardInterrupt:
                return

    def on_receive(self, *args : Callable[[sok.AddressInfo, Message], bytes]):
        """
        Attach a callback that is called when a message is received

        Parameters
        ---
        *args: List[Callable[[sok.AddressInfo, Message], bytes]]
            List of callable objects containing its Method type and respective callback function
        """
        for x in args:
            self.recv_functions.append(x)

    @staticmethod
    def parse_packet(data : bytes) -> Message:
        """
        Deserializes incoming byte received by the TCP socket

        Parameters
        ---
        data: bytes
            Byte object received by socket

        Returns
        ---
        Message object
        """
        return Util.deserialize(data, MessageType.REQUEST)

    


