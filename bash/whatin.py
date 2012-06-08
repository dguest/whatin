#!/usr/bin/env python2.7
"""
Dump info on root file. 
"""
if __name__ == "__main__":
    import sys, argparse
    from dumproot.parser import getFileFrom, dump

    parser = argparse.ArgumentParser(
        description = __doc__, 
        epilog = 'Author: Dan Guest <dguest@cern.ch>')


    parser.add_argument(
        'file_name', nargs='+', 
        help = "NOTE: must go before '-e' for tab-complete to work")
    parser.add_argument('-e', action = 'append', default = [], 
                        help = 'expand object in root file')

    args = parser.parse_args(sys.argv[1:])

    stuff_file,d = getFileFrom(','.join(args.file_name),
                               expand_list = args.e)

    dump(stuff_file)

    if d:
        raw_input('press enter to close hists')

            
    stuff_file.close()



