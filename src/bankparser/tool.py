import bankparser.config as config
import argparse
import bankparser.parser
from bankparser.qif import *

#import configparser

#configfile='config.ini'

#config = configparser.ConfigParser()
#settings=config.read(configfile,encoding='utf-8')



parser = argparse.ArgumentParser()
parser.add_argument('bank', help='Bank name')
parser.add_argument('csvfile', help='path to bank file')
parser.add_argument('--out-file', help='path to qif file')
args = parser.parse_args()

#encoding = config.settings[args.bank].get('encoding', 'utf-8')
#f = open(args.csvfile, 'r', encoding=encoding)


parser=bankparser.parser.StatementParser(args.bank,args.csvfile)
parser.parse()
qif=QIF(parser.statement)
qif.save('qif.qif')


#print(parser.statement.lines[0].description)
