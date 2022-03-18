from typing import List, Tuple
from ftp.parser.message_type import MessageType, MethodType

from ftp.parser.packet import packet

class Message:
    def __init__(self, header_size : int, type: MethodType) -> None:
        self.header = packet(header_size)
        
        # self.msg_type : MessageType = MessageType(type.__str__()[:-4].upper())
        self.data : list[packet] = []
        self.type : MethodType = type
        self.size = header_size

        self._token(
            self.type.get_format()
        )
        
    
    def _token(self, format : List[int]):
        if len(format) == 0:
            return None

        for x in format:
            self.data.append(
                packet(x)
            )

        self.size += sum(format)
        

    def parse(self, value : str) -> Tuple[packet, List[packet]] or None:
        if(value.__len__ == 0 or len(value) > self.size):
            return None
        
        self.header(
            value[:3]
        )

        if not len(self.data):
            return None

        for i, x in enumerate(self.data):
            if i > 0:
                x(value[3 + self.data[i - 1].size : 3 + self.data[i - 1].size + x.size ])            
            else:
                x(value[3 : 3 + x.size])


        
        return (self.header, self.data)

        
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