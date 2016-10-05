import os
import sys
import argparse
import bankparser.parser
import bankparser.qif


def main(args=None):

    parser = argparse.ArgumentParser()
    parser.add_argument('bank', help='Bank name')
    parser.add_argument('infile', help='path to bank file')
    parser.add_argument('--outfile', help='path to qif file')
    args = parser.parse_args()

    if args.outfile:
        newname = args.outfile
    else:
        newname = os.path.splitext(args.infile)[0]+'.qif'

    with bankparser.parser.StatementParser(args.bank,args.infile) as parser:
        count = len(parser.statement.lines)
        print('Обработано {} строк'.format(count))
        qif=bankparser.qif.QIF(parser.statement)
        qif.write(newname)
        print('qif saved ({})'.format(newname))

    return 0

if __name__ == "__main__":
    sys.exit(main())