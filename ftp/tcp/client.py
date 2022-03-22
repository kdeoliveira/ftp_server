import os
import socket as sok
import sys
from threading import Thread, local
from types import FunctionType
from typing import Callable, List, Optional, Tuple
from unittest import result
from ftp.parser.message import Message, Util

from ftp.parser.message_type import MessageType, MethodType, RequestType, ResponseType

import signal


BASE_DIR = os.getcwd() + os.sep + "dir" + os.sep + "client"


class TcpClient():
    _DEFAULT_PORT = 1025
    _MAX_BUFFER = 512

    def __init__(self, ip_addr) -> None:
        self.thread = None
        self.socket = sok.socket(sok.AF_INET, sok.SOCK_STREAM)

        self.ip_address = ip_addr
        self._is_connected = False
        self.create_message_functions : List[Tuple[MethodType, FunctionType] ] = []
        self.on_response_functions: List[Tuple[MethodType, FunctionType]] = []

        signal.signal(signal.SIGINT, self.handler)


    def connect(self):
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
        lcls = locals()
        cmd_format : RequestType or None = None
        while self._is_connected:
            try:
                msg = self.cin()
                if len(msg):
                    try:
                        exec("cmd_format_lcls = RequestType.%s" % msg[0].upper(), globals(), lcls)
                        cmd_format = lcls["cmd_format_lcls"]
                        
                        # data : Optional[bytes] = None

                        for x in self.create_message_functions:
                            if(x[0] == cmd_format):
                                self.socket.send( x[1](msg, cmd_format) )
                            
                            
                    except (AttributeError ,SyntaxError, IndexError) as e:
                        # print("Invalid message:", e)
                        # self.socket.send not necessary as the client application should be aware of the supported commands (eg. offline)
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
        return Util.deserialize(data, MessageType.RESPONSE)


    def on_send(self, *args: Tuple[ MethodType ,Callable[[List[str], MethodType], bytes]]):
        for x in args:
            self.create_message_functions.append(x)

    def on_response(self, *args: Tuple[MethodType,  Callable[[Message], None ]] ):
        for x in args:
            self.on_response_functions.append(x)

    # def create_message(self, inp : List[str], type : RequestType) -> Message:
    #     message = Message(3, type)

    #     if type == RequestType.PUT:
    #         file_data = Util.str2bit(inp[1], message.data[1].size, with_count=True)
    #         file_size = "00000000000000000000000000000000"

    #         message.parse(
    #             file_data + file_size
    #         )

    #     return message

    def cin(self) -> List[str]:
        try:
            msg = input("ftp> ")
            return msg.strip().split()
        except EOFError:
            raise KeyboardInterrupt



    def handler(self, signum , frame):
        #stdin is locking. Hence after SIGINT the application will still hang
        #probable solution would be implementing the thread as daemon

        print("\nClosing FTP Connection. Press [ENTER] to finish")
        self._is_connected = False
        self.socket.close()
        
        # sys.stdin.close()