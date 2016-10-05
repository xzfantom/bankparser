import csv
from datetime import datetime

from bankparser.config import *

from bankparser.statement import Statement, StatementLine


class StatementParser:

    _isopenfile = False
    bank = None
    fin = None
    statement = None
    cur_record = 0
    confbank = None

    def __init__(self,bank,fin):
        self.confbank = getBankConfig(bank)
        if type(fin)==str:
            encoding = self.confbank.commons.encoding
            f = open(fin, 'r', encoding=encoding)
            self.fin=f
            self._isopenfile = True
        else:
            self.fin=fin
        self.statement = Statement()
        self.bank = bank
        self.statement.bank=bank
        self.statement.type=self.confbank.commons.type
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
        self.statement.lines = [] # ????
        reader = self._split_records()
        for line in reader:
            self.cur_record += 1
            if not line:
                continue
            stmt_line = self._parse_record(line)
            if stmt_line:
                self.statement.lines.append(stmt_line)
        #print ('Parsed {} lines'.format(self.cur_record))
        return self.statement

    def _split_records(self):

        startafter = self.confbank.commons.startafter # getattr(self.confbank.commons,FIELD_STARTAFTER[CNAME])
        if startafter:
            flag = 0
            strFile = []
            for line in self.fin:
                if flag:
                    # print(line)
                    if not line in ['\n', '\r\n']:
                        strFile.append(line)
                if line.startswith(startafter): flag = 1
            self.fin=strFile

        fields = self.confbank.commons.fields # getattr(self.confbank.commons,FIELD_FIELDS[CNAME])
        bdelimiter= self.confbank.commons.delimiter # getattr(self.confbank.commons,FIELD_DELIMITER[CNAME])
        return csv.DictReader(self.fin, delimiter=bdelimiter, fieldnames=fields)

    def _parse_record(self,line):
        #print(line)

        sl = StatementLine()

        # Список имен полей для банка из ini файла
        inifields = self.confbank.commons.fields
        objfields = [arg for arg in dir(StatementLine) if not arg.startswith('_')]
        for field in objfields:
            if field in inifields:
                rawvalue = line[field]
                # Подмена значения из списка настроек, если список есть в настр. банка
                list = getattr(bankconfig,field,None)
                if list:
                    rawvalue = list.get(rawvalue,rawvalue)
                # Подстановка знака для суммы если он есть
                if field=='amount':
                    list = getattr(bankconfig, 'amountsign', None)
                    if list:
                        if 'amountsign' in line.keys():
                            sign=list.get(line['amountsign'],'')
                            rawvalue=sign + rawvalue
                        else:
                            pass
                            # print('no amountsign in line')
                            # print(line)
                value = self._parse_value(rawvalue, field)
                # if field=='action':
                #     value=self.confbank.actions.get(value.lower(),value)
                setattr(sl, field, value)
        if self.cur_record==1:
            self.statement.account=sl.account # getattr(sl,FIELD_ACCOUNT[CNAME])
        return sl

    def _parse_value(self, value, field):
        tp = type(getattr(StatementLine, field))
        if tp == datetime:
            return self._parse_datetime(value)
        elif tp == float:
            return self._parse_float(value)
        else:
            return value.strip()

    def _parse_datetime(self, value):
        date_format =  self.confbank.commons.dateformat
        return datetime.strptime(value, date_format)

    def _parse_float(self, value):
        val = value.replace(',', '.')
        return float(val)




