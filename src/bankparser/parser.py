import csv
from datetime import datetime

import bankparser.config
import bankparser.statement
import bankparser.statementline


class StatementParser:
    _isopenfile = False
    bank = None
    fin = None
    statement = None
    cur_record = 0
    confbank = None

    def __init__(self, bank, fin):
        self.confbank = bankparser.config.get_bank_config(bank)
        if type(fin) == str:
            encoding = self.confbank.commons.encoding
            self.fin = open(fin, 'r', encoding=encoding)
            self._isopenfile = True
        else:
            self.fin = fin
        self.statement = bankparser.statement.Statement()
        self.bank = bank
        self.statement.bank = bank
        self.statement.type = self.confbank.commons.type
        self._parse()

    def __del__(self):
        self._close_file()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close_file()

    def _close_file(self):
        if self._isopenfile:
            self.fin.close()
            self._isopenfile = False

    def _parse(self):
        # print('parsing...')
        self.statement.lines = []  # ????
        reader = self._split_records()
        for line in reader:
            self.cur_record += 1
            if not line:
                continue
            stmt_line = self._parse_record(line)
            if stmt_line:
                self.statement.lines.append(stmt_line)
        # print ('Parsed {} lines'.format(self.cur_record))
        return self.statement

    def _split_records(self):

        fields = self.confbank.commons.fields
        bdelimiter = self.confbank.commons.delimiter

        startafter = self.confbank.commons.startafter
        if startafter:
            flag = 0
            strfile = []
            for line in self.fin:
                if flag:
                    # print(line)
                    if line not in ['\n', '\r\n']:
                        strfile.append(line)
                if line.startswith(startafter):
                    flag = 1
            return csv.DictReader(strfile, delimiter=bdelimiter, fieldnames=fields)
        else:
            return csv.DictReader(self.fin, delimiter=bdelimiter, fieldnames=fields)

    def _parse_record(self, line):
        """
        Разбор одной строки. Строка должна быть поименована по названиям полей
        :param line:
        :return:
        """

        sl = bankparser.statementline.StatementLine()

        # Список имен полей для банка из ini файла
        inifields = self.confbank.commons.fields
        objfields = [arg for arg in dir(bankparser.statementline.StatementLine) if not arg.startswith('_')]
        for field in objfields:
            if field in inifields:
                rawvalue = line[field]
                # Подмена значения из списка настроек, если список есть в настр. банка
                changemap = getattr(bankparser.config.bankconfig, field, None)
                if changemap:
                    rawvalue = changemap.get(rawvalue, rawvalue)
                # Подстановка знака для суммы если он есть
                if field == 'amount':
                    changemap = getattr(bankparser.config.bankconfig, 'amountsign', None)
                    if changemap:
                        if 'amountsign' in line.keys():
                            sign = changemap.get(line['amountsign'], '')
                            rawvalue = sign + rawvalue
                        else:
                            pass
                            # print('no amountsign in line')
                            # print(line)
                value = self._parse_value(rawvalue, field)
                # if field=='action':
                #     value=self.confbank.actions.get(value.lower(),value)
                setattr(sl, field, value)
        if self.cur_record == 1:
            self.statement.account = sl.account
        return sl

    def _parse_value(self, value, field):
        tp = type(getattr(bankparser.statementline.StatementLine, field))
        if tp == datetime:
            return self._parse_datetime(value)
        elif tp == float:
            return self._parse_float(value)
        else:
            return value.strip()

    def _parse_datetime(self, value):
        date_format = self.confbank.commons.dateformat
        return datetime.strptime(value, date_format)

    @staticmethod
    def _parse_float(value):
        val = value.replace(',', '.')
        return float(val)
