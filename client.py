import pickle

import socket
import sys
import bitarray
from bitarray import util

from ftp.parser.packet import packet

from ftp.parser.message_type import MethodType, RequestType

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 1025  # The port used by the server





type : MethodType or None = None


val : bitarray.bitarray = util.hex2ba( bytes("kevindeoliveira", "ascii").hex() )

print(
len(val), 8*32
)



pak : packet = packet(3)
pak("011")

pak = pickle.dumps(pak)

val = util.serialize(
    val
)

print(util.deserialize(val))



print(pak)

print(
    pickle.loads(pak)
)



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    try:
        while True:
            msg = input("ftp> ")
            
            if msg:    
                try:
                    exec("type = RequestType.%s" % msg.split()[0].upper())
                    
                    s.sendall(
                        pickle.dumps(
                    bitarray.bitarray(type.value)
                        )
                    )

                except AttributeError as e:
                    print("Invalid message")
                except SyntaxError as e:
                    print("Invalid message")

    except KeyboardInterrupt:
        print("Closing connection")



    
    



