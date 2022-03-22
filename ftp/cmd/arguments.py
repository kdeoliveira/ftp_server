
import sys
from types import FunctionType
from typing import List, Tuple




class ParserArgs:

    default_helper = ["-h", "--help", "-?"]
    default_version = ["-v", "--version"]


    def __init__(self, **kwargs) -> None:
        """
        Parse arguments passed in command-line

        Parameters
        ----------
        helper: str
            Helper message to be displayed
        version: str
            Version message to be displayed 

        Returns
        ----------
        returns: None
        """
        self.argv : list = []
        self.argn : int = 0
        self._helper : str = ""


        if kwargs.__len__ == 0 :
            return

        self._helper = kwargs.get("helper")
        self._version = kwargs.get("version")

        
    def get_args(self, args : List[str] or None = None) -> Tuple[list, int]:
        """
        Get either arguments passed to parameter args or directly from sys.argv
        
        Parameters
        ----------
        args: List[str]
            List of arguments to be parsed

        Returns
        ----------
        return: Tuple[list, int]
            Tuple containg arguments and its length
        """

        if args is None or args.__len__ <= 1 :
            self.argv = sys.argv[1:]
            self.argn = len(sys.argv)
            return (self.argv, self.argn)

        self.argv = args[1:]
        self.argn = len(args)

        return (self.argv, self.argn)





    def parameters(self, format : List[str] or None = None) -> dict:
        """
        List of accepted parameters on command-line

        Paramters
        ----------
        format: List[str]
            List of accepted parameters

        Returns 
        ----------
        return: dict
            Dictionary containing paramters and respective values
        """
        temp = {}

        for i,x in enumerate(self.argv):
            if x in self.default_helper:
                sys.exit(self._helper) if self._helper else 0
            elif x in self.default_version:
                sys.exit(self._version) if self._version else 0    

            if format and x[0] == "-" and x not in format:
                sys.exit("unknown option: "+x+"\n"+self._helper)

            elif format and x in format and i < self.argn - 1:
                temp.update({
                    x: self.argv[i + 1]
                })
            
    
        return temp
