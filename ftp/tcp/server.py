from ast import arg
import pickle
import socket as sok
from threading import Thread
from types import FunctionType
from typing import Any, Callable, List, Tuple
from bitarray import util

from ftp.parser.message import Message, Util
from ftp.parser.message_type import MessageType, RequestType, ResponseType


class TcpServer():
    _DEFAULT_PORT = 1025
    _MAX_BUFFER = 1024

    def __init__(self, ip_addr) -> None:
        self.thread = None
        self.socket = sok.socket(sok.AF_INET, sok.SOCK_STREAM)
        self.socket.setsockopt(sok.SOL_SOCKET, sok.SO_REUSEADDR, 1)
        self.socket.bind( (ip_addr, self._DEFAULT_PORT) )
        self.ip_address = ip_addr
        self.recv_functions : List[Tuple[RequestType, FunctionType]] = []

    def _init_app(self) -> str:
        return """-- FTP Server initializing on {ip}:{port}
-- Version 1.0.0 by Kevin de Oliveira
-- help for list of available commands and some concepts guiding""".format(ip = self.ip_address, port = self._DEFAULT_PORT)

    def listen(self):
        self.socket.listen()
        print(self._init_app())
        while True:
            try:
                conn, addr = self.socket.accept()
                self.thread = Thread(target=self.handle_listen, args=(conn, addr))
                self.thread.start()
                if self.thread:
                    self.thread.join()
            except KeyboardInterrupt:
                print("Closing connection")
                self.socket.close()
                return

        

    def handle_listen(self, conn : sok.socket, addr : sok.AddressInfo):
        print("""> New connection {addr}:{port}""".format(addr = addr[0], port=addr[1]))
        while True:
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
                        
                        
                    

            




    def on_receive(self, *args : Callable[[sok.AddressInfo, Message], bytes]):
        for x in args:
            self.recv_functions.append(x)

    @staticmethod
    def parse_packet(data : bytes) -> Message:
        return Util.deserialize(data, MessageType.REQUEST)

    


