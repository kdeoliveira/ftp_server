
import sys
from types import FunctionType
from typing import List, Tuple
from xmlrpc.client import boolean



class ParserArgs:

    default_helper = ["-h", "--help", "-?"]
    default_version = ["-v", "--version"]


    def __init__(self, max : int, **kwargs) -> None:
        self.argv : list = []
        self.argn : int = 0
        self._helper : str = ""

        self._max_args : int = max

        if kwargs.__len__ == 0 :
            return

        self._helper = kwargs.get("helper")
        self._version = kwargs.get("version")

        




    def get_args(self, args : List[str] or None = None) -> Tuple[list, int]:
        if args is None or args.__len__ <= 1 :
            self.argv = sys.argv[1:]
            self.argn = len(sys.argv)
            return (self.argv, self.argn)

        self.argv = args[1:]
        self.argn = len(args)

        return (self.argv, self.argn)





    def parameters(self, format : List[str] or None = None) -> list:
        temp = []

        for i,x in enumerate(self.argv):
            if format and x in format and i < self.argn - 1:
                temp.append({
                    x,
                    self.argv[i + 1]
                })
            if x in self.default_helper:
                sys.exit(self._helper) if self._helper else 0
            elif x in self.default_version:
                sys.exit(self._version) if self._version else 0        
        return temp
