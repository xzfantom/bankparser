import bankparser.config as config
import os
import argparse
import bankparser.parser
from bankparser.qif import *


parser = argparse.ArgumentParser()
parser.add_argument('bank', help='Bank name')
parser.add_argument('csvfile', help='path to bank file')
parser.add_argument('--outfile', help='path to qif file')
args = parser.parse_args()

if args.outfile :
    newname=args.outfile
else:
    newname=os.path.splitext(args.csvfile)[0]+'.qif'

parser=bankparser.parser.StatementParser(args.bank,args.csvfile)
parser.parse()

qif=QIF(parser.statement)
qif.save(newname)
