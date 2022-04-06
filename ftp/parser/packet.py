##
# @file Packet.py
#
# @brief Packet object containing bit array
#
#
# @section author_doxygen_example Author(s)
# - Created by Kevin de Oliveira on 04/01/2022.
# - Student ID: 40054907
#
# Copyright (c) 2022 Kevin de Oliveira.  All rights reserved.

import bitarray


class packet:
        

    def __init__(self, max_bits : int, fill : bool = False, *args) -> None:
        """!
        Object representing a packet as binary

        @param max_bits: int    Maximum size of this packet object
        @param fill: bool       Align the length of this packet to a multiple of 8 (1 byte)

        @return packet
        """
        self.body = bitarray.bitarray(max_bits)
        self.size = max_bits
        self.body.setall(0)
        if fill:
            self.body.fill()
            self.size = len(self.body)


    def __call__(self, val : str) -> 'packet':
        """!
        Append value to this object

        @param val: str Value to be appended
        
        @return packet
        """
        if len(val) != self.size:
            raise ValueError("Incorrect size provided")

        self.body = bitarray.bitarray(val)
        return self

    def value(self) -> bitarray.bitarray:
        """!
        Getter of the body attribute

        @return Bitarray object
        """
        return self.body

    def to_bytes(self) -> bytes:
        """!
        Returns the byte value of the body attribute

        @return Byte object
        """
        return self.body.tobytes()


    def set_size(self, val: int) -> None:
        """!
        Redefine the packet object size

        @param val: int Size of this packet object

        @return None
        """
        self.body = bitarray.bitarray(val)
        self.body.clear()
        self.size = val


    def __str__(self) -> str:
        return self.body.to01()


    def __repr__(self) -> str:
        return self.body.to01()

    