import os
import sys
import argparse
import bankparser.parsercsv
import bankparser.config


# def get_version():
#     dist = pkg_resources.get_distribution("bankparser")
#     return dist.version


def list_banks(args):
    """
    Выводит список доступных банков
    :param args:
    :return:
    """
    print('list available banks:')
    banks = bankparser.config.bankconfig.get_list_banks()
    for bank in banks:
        print(bank)


def convert(args):
    """
    Конвертация в QIF
    :param args:
    :return:
    """
    print('Convert {0} file {1}'.format(args.bank, args.infile))

    outformat = "qif"
    if args.format:
        outformat = args.format    

    if args.outfile:
        newname = args.outfile
    else:
        newname = os.path.splitext(args.infile)[0] + '.out.' + outformat

    bank_parser = bankparser.config.bankconfig.get_parser(args.bank)

    if args.inifile:
        bank_parser.read_ini(args.inifile)

    statement = bank_parser.parse(args.infile)
    count = len(statement.lines)
    print('Read {} lines'.format(count))
    if outformat == "qif":
        from .output import qif
        out = qif.QIF(statement)
    else:
        from .output import csv
        out = csv.CSV(statement=statement)
    out.write(newname)
    print('file saved ({})'.format(newname))


def main(args=None):
    parser = argparse.ArgumentParser(description='Tool to convert proprietary bank statement ' +
                                                 'to QIf format. Ver {}'.format(bankparser.__version__))
    # parser.add_argument("-v", "--version", action="version",
    #                     version='bankparser version %s' % get_version(),
    #                     help="show current version and exit")
    subparsers = parser.add_subparsers(help='List of commands')

    # A list command
    list_parser = subparsers.add_parser('list', help='list available banks')
    list_parser.set_defaults(func=list_banks)
    # A convert command
    convert_parser = subparsers.add_parser('convert', help='Convert to qif format')
    convert_parser.add_argument('bank', help='Bank name')
    convert_parser.add_argument('infile', help='path to bank file')
    convert_parser.add_argument('--outfile', help='path to qif file')
    convert_parser.add_argument('--inifile', help='path to ini file')
    convert_parser.add_argument('--format', help='output file format (qif, csv)')
    convert_parser.set_defaults(func=convert)

    args = parser.parse_args()

    if not hasattr(args,"func"):
        parser.print_help()
        sys.exit(1)

    args.func(args)

if __name__ == "__main__":
    sys.exit(main())
