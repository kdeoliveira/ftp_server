from ast import arg
import socket as sok
from threading import Thread
from types import FunctionType
from bitarray import util


class TcpServer():
    _DEFAULT_PORT = 1025
    _MAX_BUFFER = 11*8

    def __init__(self, ip_addr) -> None:
        self.thread = None
        self.socket = sok.socket(sok.AF_INET, sok.SOCK_STREAM)
        self.socket.bind( (ip_addr, self._DEFAULT_PORT) )
        self.ip_address = ip_addr
        self.recv_functions = {}
        self.send_functions = {}



    def listen(self):
        self.socket.listen()
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
        while conn:
            data = conn.recv(self._MAX_BUFFER)
            if not data:
                return None
            
            print(
                addr, data, util.deserialize(data)
                )

        print("No connection")


    def on_receive(self):
        data = self.socket.recv(self._MAX_BUFFER)
        if not data:
            return None
        print(data.decode())
        
    
    def register_recv_functions(self, callback : object):
        if not callback:
            return

        self.recv_functions.update(callback)

    def register_send_functions(self, callback : object):
            if not callback:
                return

            self.send_functions.update(callback)



        