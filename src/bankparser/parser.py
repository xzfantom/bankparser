import csv
from datetime import datetime

from bankparser.config import *

from bankparser.statement import Statement, StatementLine

class StatementParser():

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
        else:
            self.fin=fin
        self.statement = Statement()
        self.bank = bank
        self.statement.bank=bank
        self.statement.type=self.confbank.commons.type


    def parse(self):
        #print('parsing...')
        reader = self.split_records()
        for line in reader:
            self.cur_record += 1
            if not line:
                continue
            stmt_line = self.parse_record(line)
            if stmt_line:
                self.statement.lines.append(stmt_line)
        print ('Parsed {} lines'.format(self.cur_record))
        return self.statement

    def split_records(self):

        #dialect=csv.Dialect()
        #dialect.delimiter=self.__confbank.get('delimiter',';')

        startafter = self.confbank.commons.startafter
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

        fields=self.confbank.commons.fields
        return csv.DictReader(self.fin, delimiter=self.confbank.commons.delimiter, fieldnames=fields)

    def parse_record(self,line):
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
                if field==FIELD_AMOUNT['name']:
                    list = getattr(bankconfig, FIELD_AMOUNTSIGN['name'], None)
                    if list:
                        sign=list.get(line[FIELD_AMOUNTSIGN['name']],'')
                        rawvalue=sign + rawvalue
                value = self.parse_value(rawvalue, field)
                # if field=='action':
                #     value=self.confbank.actions.get(value.lower(),value)
                setattr(sl, field, value)
        if self.cur_record==1:
            self.statement.account=sl.account
        return sl






    def parse_value(self, value, field):
        tp = type(getattr(StatementLine, field))

        if tp == datetime:
            return self.parse_datetime(value)
        elif tp == float:
            return self.parse_float(value)
        else:
            return value.strip()


    def parse_datetime(self, value):
        date_format=self.confbank.commons.dateformat
        return datetime.strptime(value, date_format)

    def parse_float(self, value):
        val = value.replace(',', '.')
        return float(val)




