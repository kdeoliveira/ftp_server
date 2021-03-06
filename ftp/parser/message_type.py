##
# @file message_type.py
#
# @brief Enumaration classes for each method type used during FTP communication
#
#
# @section author_doxygen_example Author(s)
# - Created by Kevin de Oliveira on 04/01/2022.
# - Student ID: 40054907
#
# Copyright (c) 2022 Kevin de Oliveira.  All rights reserved.

from abc import abstractmethod
import enum
from typing import List



class MessageType(enum.Enum):
    """!
    Enum class for type of message sent
    """
    REQUEST = 0
    RESPONSE = 1

class MethodType(enum.Enum):
    @abstractmethod
    def get_format(self) -> List[int]:
        pass
    

class RequestType(MethodType):
    """!
    Enum class for type of Request sent
    """
    PUT = "000"
    GET = "001"
    CHANGE = "010"
    HELP = "011"

    def get_format(self):
        """!
        Format as the number of bits it is expected of the given method type

        @return List[int]: List containing number of bits per packet 
        """
        if self == RequestType.PUT:
            return [5, 32 * 8, 4 * 8]
        elif self == RequestType.GET:
            return [5, 32*8]
        elif self == RequestType.CHANGE:
            return [5, 32 * 8, 8, 32 * 8]
        elif self == RequestType.HELP :
            return [5]
        else:
            return []

class ResponseType(MethodType):
    """!
    Enum class for type of Response sent
    """
    OK_PUT_CHANGE = "000"
    OK_GET = "001"
    ERROR_NOT_FOUND = "010"
    ERROR_UNKNOWN = "011"
    ERROR_NO_CHANGE = "101"
    HELP = "110"

    def get_format(self):
        """!
        Format as the number of bits it is expected of the given method type

        @return List[int]: List containing number of bits per packet 
        """
        if self == ResponseType.OK_PUT_CHANGE:
            return [5]
        elif self == ResponseType.OK_GET:
            return [5, 32*8, 4*8]
        elif self == ResponseType.ERROR_NOT_FOUND:
            return [5]
        elif self == ResponseType.ERROR_UNKNOWN:
            return [5]
        elif self == ResponseType.ERROR_NO_CHANGE:
            return [5]
        elif self == ResponseType.HELP :
            return [5, 32 * 8]
        else:
            return []
