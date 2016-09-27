import bankparser.config as config
import os
import sys
import argparse
import bankparser.parser
from bankparser.qif import *
from bankparser.config import *


def main(args=None):

    # conf=getBankConfig("vtb24")
    # conf.printdeb()
    # exit(0)

    parser = argparse.ArgumentParser()
    parser.add_argument('bank', help='Bank name')
    parser.add_argument('infile', help='path to bank file')
    parser.add_argument('--outfile', help='path to qif file')
    args = parser.parse_args()

    if args.outfile:
        newname = args.outfile
    else:
        newname = os.path.splitext(args.infile)[0]+'.qif'

    parser=bankparser.parser.StatementParser(args.bank,args.infile)
    parser.parse()

    qif=QIF(parser.statement)
    #qif.printdeb()

    qif.save(newname)

    return 0

if __name__ == "__main__":
    sys.exit(main())