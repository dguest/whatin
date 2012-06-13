#!/usr/bin/env python2.7 
"""
usage: auto-complete-root.py <root file> [<path>]

Reads in <root file> and attempts to navigate recursively to the end of 
<path>. Returns path completions accessable from the last directory or tree 
in <path>. 

Author: Dan Guest <dguest@cern.ch> 
Date: Fri Jun  8 10:44:03 CEST 2012
"""
import sys, os
from tabroot import pyread

if __name__ == '__main__': 
    file_name = sys.argv[1]
    try: 
        dir_path = sys.argv[2].split('/')
    except IndexError: 
        dir_path = []

    items = pyread.read_file(
        root_file = file_name, 
        dir_path = dir_path)
    for subitem in items: 
        print subitem, 

