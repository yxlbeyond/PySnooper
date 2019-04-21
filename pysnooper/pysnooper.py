# Copyright 2019 Ram Rachum.
# This program is distributed under the MIT license.

from future import standard_library
standard_library.install_aliases()
import sys
import os
import inspect
import types
import datetime as datetime_module
import re
import collections

import decorator

from . import utils
from . import pycompat
from .tracer import Tracer

        
def get_write_function(output):
    if output is None:
        def write(s):
            s += '\n'
            if isinstance(s, bytes): # Python 2 compatibility
                s = s.decode('utf-8')
            stderr = sys.stderr
            stderr.write(s)
    elif isinstance(output, (pycompat.PathLike, str)):
        def write(s):
            s += '\n'
            if isinstance(s, bytes): # Python 2 compatibility
                s = s.decode('utf-8')
            with open(output_path, 'a') as output_file:
                output_file.write(s)
    else:
        assert isinstance(output, utils.WritableStream)
        def write(s):
            s += '\n'
            if isinstance(s, bytes): # Python 2 compatibility
                s = s.decode('utf-8')
            output.write(s)
            
    return write
    
    

def snoop(output=None, variables=(), depth=1):
    write = get_write_function(output)
    @decorator.decorator
    def decorate(function, *args, **kwargs):
        target_code_object = function.__code__
        with Tracer(target_code_object=target_code_object,
                    write=write, variables=variables,
                    depth=depth):
            return function(*args, **kwargs)
    
    return decorate
    
    
    