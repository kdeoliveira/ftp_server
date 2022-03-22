import math
from typing import List, Tuple

import bitarray
from bitarray import util
from ftp.parser.message_type import MessageType, MethodType, RequestType, ResponseType

from ftp.parser.packet import packet

class Message:
    def __init__(self, header_size : int, type: MethodType) -> None:
        """
        Encapsulates a packet object that is sent to the socket

        message is represented as: [header | data_1 | data_2 | ... | payload?]

        Parameters
        ---
        header_size: int
            Size of the header packet
        type: MethodType
            Type of message that will be sent

        Returns
        ---
        Returns nothing
        """
        self.header = packet(header_size)
        
        self.data : list[packet] = []
        self.type : MethodType = type

        self.header(self.type.value)

        self.size = header_size

        self.payload : packet or None = None



        self._token(
            self.type.get_format()
        )
        
    
    def _token(self, format : List[int]):
        """
        Internal function to include data into the message
        """
        if len(format) == 0:
            return None

        
        for x in format:
            self.data.append(
                packet(x)
            )
        
        self.size += sum(format)
        

    def parse(self, value : str) -> Tuple[packet, List[packet]] or None:
        """
        Parses input values into its respective data field

        Parameters
        ---
        value: str
            Inserts the values its respective data. Note that value must be represented in binary format

        Returns
        ---
        Returns a tuple containing the header packet and its data packets
        """
        if(value.__len__ == 0 or len(value) > self.size):
            return None
                       
        if not len(self.data):
            return None

        ind = 0
        
        for i, x in enumerate(self.data):
            x(value[ind :  ind + x.size ])            
            ind += x.size


        return (self.header, self.data)

    def add_payload(self, value : str) -> None:
        """
        Attach payload to this message

        Parameters
        ---
        value: str
            Value to be parsed into packet. Note that value must be represented in binary format
        """
        temp = bitarray.util.hex2ba( value.encode("utf-8").hex() ).to01()

        self.payload = packet(len(temp))
        self.payload(temp)

    def has_payload(self) -> bool:
        """
        Verifies if this message has a payload attached

        Returns
        ---
        Returns true if contains a paylaod; otherwise false
        """
        return self.payload is not None

    

    def __repr__(self) -> str:
        temp = "["+ self.header.__str__() +"]"
        for x in self.data:
            temp += x.__str__()
        return  temp
        
    def __str__(self) -> str:
        temp = "["+ self.header.__str__() +"]"
        for x in self.data:
            temp += x.__str__()
        return  temp


class Util:

    @staticmethod
    def serialize(msg : Message) -> bytes:
        """
        Serializes a Message object into bytes following its binary representation

        Parameters
        ---
        msg: Message
            Message object
        
        Returns
        ---
        Returns the extended byte representation of that message object
        """
        binary : bitarray.bitarray = bitarray.bitarray(endian="big")
        
        binary.extend(
            msg.header.body
        )


        for x in msg.data:
            binary.extend(
                x.body
            )
        
        if msg.has_payload():
            binary.extend(
                msg.payload.body
            )


        return util.serialize(binary)


    @staticmethod
    def deserialize(binary : bytes, type : MessageType) -> Message:
        """
        Deserialize the byte value into a Message object

        Parameters
        ---
        binary: bytes
            Input byte object to be deserialized
        type: MessageType
            Type of message that is to be deserialized
        
        Returns
        ---
        Returns a message object        
        """
        temp : bitarray.bitarray = util.deserialize(binary)
        
        if type == MessageType.REQUEST:
            msg = Message(3, RequestType(temp.to01()[:3]))

            if msg.type == RequestType.PUT:
                msg.parse(
                    temp.to01()[3:msg.size]
                )
                pk = packet(len(temp.to01()[msg.size:]))
                pk(temp.to01()[msg.size:])
                msg.payload = pk
            else:
                msg.parse(
                    temp.to01()[3:]
                )

            return msg

        elif type == MessageType.RESPONSE:
            msg = Message(3, ResponseType(temp.to01()[:3]))
            if msg.type == ResponseType.OK_GET:
                msg.parse(
                    temp.to01()[3:msg.size]
                )
                pk = packet(len(temp.to01()[msg.size:]))
                pk(temp.to01()[msg.size:])
                msg.payload = pk

            else:
                msg.parse(
                    temp.to01()[3:]
                )
        
            return msg
        
        else:
            raise ValueError("Incorrect Message type")
        



    @staticmethod
    def str2bit(val : str, size : int, with_count : bool = True, size_count : int or None = None ) -> str:
        """
        Converts a string value its equivalent binary representation in utf-8 encoding

        Note that python does not use standard representation of variable size
        Hence, manual conversion should be done

        Parameters
        ---
        val: str
            String to be converted
        size: int
            Size of the expected binary value
        with_count: bool
            Attach the binary represented size of paramters val
        size_count: int
            Size of the binary represented value for the portion representing the size of val
        
        Returns 
        ---
        Retuns a binary representation of the value passed
        """
        val = val.strip()

        data : str = util.hex2ba( val.encode("utf-8").hex() ).to01()

        if(len(data) > size): raise ValueError("Value passed is too big")


        if(len(data) < size):
            for _ in range(0, size - len(data)):
                data = "0" + data


        if with_count:
            count : int = util.int2ba(len(val)).to01()
            
            if size_count:
                count_size = size_count
            else:
                count_size = int( math.log2( int(size / 8) ) ) 

            if(len(count) < count_size):
                for _ in range(0, count_size - len(count)):
                    count = "0" + count

            return count + data
        else:
            return data
    @staticmethod
    def bit2byte(msg : Message) -> List[bytes]:
        """
        Converts a Message object to a list of byte equivalent values

        Parameters
        ---
        msg: Message
            Message object to be converted
        
        Returns
        ---
        List of bytes containing all packets encapsulated by the Message object
        """
        temp : list[bytes] = []
        for x in msg.data:
            temp.append(
                x.body.tobytes()
            )
        if msg.has_payload():
            temp.append(
                msg.payload.body.tobytes()
            )

        return temp



