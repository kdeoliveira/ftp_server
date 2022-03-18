
import bitarray


class packet:

    def __init__(self, max_bits : int = 0) -> None:
        self.body = bitarray.bitarray(max_bits)
        self.body.clear()
        self.size = max_bits

    def __init__(self, max_bits : int, fill : bool = False, *args) -> None:
        self.body = bitarray.bitarray(max_bits)
        self.size = max_bits
        self.body.clear()

        if fill:
            self.body.fill()
            self.size = len(self.body)


    def __call__(self, val : str) -> 'packet':
        self.body = val

    def value(self) -> bitarray.bitarray:
        return self.body


    def set_size(self, val: int) -> None:
        self.body = bitarray.bitarray(val)
        self.body.clear()
        self.size = val


    def __str__(self) -> str:
        return self.body.__str__()


    def __repr__(self) -> str:
        return self.body.__str__()

    