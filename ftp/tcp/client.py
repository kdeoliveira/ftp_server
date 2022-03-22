"""
TCP socket interface representing FTP client
"""

import socket as sok
import sys
from threading import Thread, local
from types import FunctionType
from typing import Callable, List, Optional, Tuple
from unittest import result
from ftp.parser.message import Message, Util

from ftp.parser.message_type import MessageType, MethodType, RequestType, ResponseType

import signal




class TcpClient():
    _DEFAULT_PORT = 1025
    _MAX_BUFFER = 512

    def __init__(self, ip_addr, **kwargs) -> None:
        """
        TCP Client interface that creates a new socket given the ip address provided for FTP communication

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
        for k,v in kwargs.items():
            if "-p" in k:
                self._DEFAULT_PORT = int(v)
            elif "-a" in k:
                ip_addr = v
        self.ip_address = ip_addr
        self._is_connected = False
        self.create_message_functions : List[Tuple[MethodType, FunctionType] ] = []
        self.on_response_functions: List[Tuple[MethodType, FunctionType]] = []

        signal.signal(signal.SIGINT, self.handler)


    def connect(self):
        """
        Creates a TCP socket bounded to the given IP address and port provided. 
        Object creates a new thread where each new connection will respond to
        """
        try:
            
            self.socket.connect( (self.ip_address, self._DEFAULT_PORT) )
            self._is_connected = True
            self.thread = Thread(target = self.handle_connection, args=())
            self.thread.start()
            if self.thread:
                self.thread.join()

        except ConnectionRefusedError:
            #Implement timeout or repetition
            print("Unable to connect to server, try again")
        except KeyboardInterrupt:
            self.socket.close()
            self._is_connected = False
        except Exception:
            return

    
    def handle_connection(self):
        """
        Internal function which handles all single client-server communication
        Method is responsible for parsing any incoming and outgoing message sent through the TCP socket
        """
        lcls = locals()
        cmd_format : RequestType or None = None
        while self._is_connected:
            try:
                msg = self.cin()
                if len(msg):
                    try:
                        exec("cmd_format_lcls = RequestType.%s" % msg[0].upper(), globals(), lcls)
                        cmd_format = lcls["cmd_format_lcls"]
                        for x in self.create_message_functions:
                            if(x[0] == cmd_format):
                                self.socket.send( x[1](msg, cmd_format) )
                    except (AttributeError ,SyntaxError, IndexError) as e:
                        # print("Invalid message:", e)
                        # self.socket.send not necessary as the client application should be aware of the supported commands (eg. offline)
                        if msg[0] == "bye":
                            raise KeyboardInterrupt()

                        self.socket.send(
                            " ".join(msg).encode("utf-8")
                        )
                    except OSError as e:
                        print("OS Error occured: ",e)
                        return
                    except ValueError as e:
                        print(e)
                        continue

                    recv = self.socket.recv(self._MAX_BUFFER)
                    
                    if recv:
                        res = self.check_response(recv)
                        if type(res.type) is ResponseType:
                            for x in self.on_response_functions:
                                if res.type == x[0]:
                                    x[1](res)
                        else:
                            self._is_connected = False
                    else:
                        self._is_connected = False

            except (KeyboardInterrupt, OSError):
                return

    def check_response(self, data : bytes) -> Message:
        """
        Deserialize the incoming message

        Parameters
        ---
        data: bytes
            Byte object received by the socket
        
        Returns
        ---
        Deserialized message object
        """
        return Util.deserialize(data, MessageType.RESPONSE)


    def on_send(self, *args: Tuple[ MethodType ,Callable[[List[str], MethodType], bytes]]):
        """
        Attach a callback that is called when a message is sent

        Parameters
        ---
        *args: List[Tuple[ MethodType ,Callable[[List[str], MethodType], bytes]]]
            List of callable objects containing its Method type and respective callback function
        """
        for x in args:
            self.create_message_functions.append(x)

    def on_response(self, *args: Tuple[MethodType,  Callable[[Message], None ]] ):
        """
        Attach a callback that is called when a message is received

        Parameters
        ---
        *args: List[Tuple[MethodType,  Callable[[Message], None ]]]
            List of callable objects containing its Method type and respective callback function
        """
        for x in args:
            self.on_response_functions.append(x)


    def cin(self) -> List[str]:
        """
        Reads stdin from command-line. By default prints 'ftp>' before reading input
        """
        try:
            msg = input("ftp> ")
            return msg.strip().split()
        except EOFError:
            raise KeyboardInterrupt



    def handler(self, signum , frame):
        """
        Internal funtion used to define a signal handler that is called when a SIGINT signal is raised by this process
        """
        
        #stdin is locking. Hence after SIGINT the application will still hang
        #probable solution would be implementing the thread as daemon

        print("\nClosing FTP Connection. Press [ENTER] to finish")
        self._is_connected = False
        self.socket.close()
        
        # sys.stdin.close()