##
# @file arguments.py
#
# @brief Parses arguemnts provided in command-line
#
#
# @section author_doxygen_example Author(s)
# - Created by Kevin de Oliveira on 04/01/2022.
# - Student ID: 40054907
#
# Copyright (c) 2022 Kevin de Oliveira.  All rights reserved.

import sys
from types import FunctionType
from typing import List, Tuple




class ParserArgs:

    default_helper = ["-h", "--help", "-?"]
    default_version = ["-v", "--version"]


    def __init__(self, **kwargs) -> None:
        """! 
        Creates a ParserArgs object

        
        @param helper: str      Helper message to be displayed
        @param version: str     Version message to be displayed 

        @return ParserArgs
        """
        self.argv : list = []
        self.argn : int = 0
        self._helper : str = ""


        if kwargs.__len__ == 0 :
            return

        self._helper = kwargs.get("helper")
        self._version = kwargs.get("version")

        
    def get_args(self, args : List[str] or None = None) -> Tuple[list, int]:
        """!
        Get either arguments passed to parameter args or directly from sys.argv
        
        @param args: List[str]      List of arguments to be parsed

        @return Tuple[list, int]:   Tuple containg arguments and its length
        """

        if args is None or args.__len__ <= 1 :
            self.argv = sys.argv[1:]
            self.argn = len(sys.argv)
            return (self.argv, self.argn)

        self.argv = args[1:]
        self.argn = len(args)

        return (self.argv, self.argn)





    def parameters(self, format : List[str] or None = None) -> dict:
        """!
        List of accepted parameters on command-line

        @param format: List[str]    List of accepted parameters

        @return dict: Dictionary containing paramters and respective values
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
                try:
                    temp.update({
                        x: self.argv[i + 1]
                    })
                except IndexError:
                    temp.update({
                        x: True
                    })
            else:
                sys.exit("unknown option: "+x+"\n"+self._helper)
            
    
        return temp
