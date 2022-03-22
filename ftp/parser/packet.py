
import bitarray


class packet:
        

    def __init__(self, max_bits : int, fill : bool = False, *args) -> None:
        """
        Object representing a packet as binary

        Parameters
        ---
        max_bits: int
            Maximum size of this packet object
        fill: bool
            Align the length of this packet to a multiple of 8 (1 byte)
        """
        self.body = bitarray.bitarray(max_bits)
        self.size = max_bits
        self.body.setall(0)
        if fill:
            self.body.fill()
            self.size = len(self.body)


    def __call__(self, val : str) -> 'packet':
        """
        Append value to this object

        Parameters
        ---
        val: str
            Value to be appended
        Returns
        ---
        self
        """
        if len(val) != self.size:
            raise ValueError("Incorrect size provided")

        self.body = bitarray.bitarray(val)
        return self

    def value(self) -> bitarray.bitarray:
        """
        Getter of the body attribute

        Returns
        ---
        Bitarray object
        """
        return self.body

    def to_bytes(self) -> bytes:
        """
        Returns the byte value of the body attribute

        Returns
        ---
        Byte object
        """
        return self.body.tobytes()


    def set_size(self, val: int) -> None:
        """
        Redefine the packet object size

        Parameters
        ---
        val: int
            Size of this packet object
        """
        self.body = bitarray.bitarray(val)
        self.body.clear()
        self.size = val


    def __str__(self) -> str:
        return self.body.to01()


    def __repr__(self) -> str:
        return self.body.to01()

    