import csv
from datetime import datetime
from decimal import Decimal

import bankparser.config
import bankparser.statement
import bankparser.statementline


class StatementParser:
    """   Базовый класс для разбора выписки"""
    bankname = None
    filename = None
    content = None
    #fin = None
    statement = None
    #cur_record = 0
    confbank = None

    def __init__(self, bankname, filename, is_content=False):
        # read settings
        self.confbank = bankparser.config.get_bank_config(bankname)

        self.cur_record = 0
        if is_content:
            self.content = filename
        else:
            # read content file in the buffer
            self.filename = filename
            encoding = self.confbank.bank.encoding
            with open(filename, 'r', encoding=encoding)as f:
                self.content = f.read()
        self.statement = bankparser.statement.Statement()
        self.bankname = bankname
        self.statement.bank = bankname
        self.statement.type = self.confbank.bank.type
        self._parse()

    def _parse(self):
        self.statement.lines = []  # ????
        self.cur_record = 0
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
        return None


    def _parse_record(self, line):
        """
        Разбор одной строки. Строка должна быть поименована по названиям полей
        :param line:
        :return:
        """

        sl = bankparser.statementline.StatementLine()
        # print(self.confbank.imp.action)
        # Список имен полей для банка из ini файла
        inifields = line.keys() #self.confbank.bank.fields
        objfields = [arg for arg in dir(bankparser.statementline.StatementLine) if not arg.startswith('_')]
        for field in objfields:
            if field in inifields:
                rawvalue = line[field]
                # Подмена значения из списка настроек, если список есть в настр. банка
                changemap = getattr(self.confbank.bank, 'm_' + field, None)
                if changemap:
                    rawvalue = changemap.get(rawvalue, rawvalue)
                value = self._parse_value(rawvalue, field)
                setattr(sl, field, value)

        # Здесь нужно добавить строку с именем счета
        # SАктивы: Текущие активы: Наличные
        # sl.category = "Активы: Текущие активы: Наличные"


        # Подставление счета по содержимому описания
        # Строки которые нужно искать в описании
        listDescr=list(self.confbank.bank.m_descr_account.keys())
        for strFind in listDescr:
            if strFind in sl.description:
                sl.category = self.confbank.bank.m_descr_account[strFind]
                break

        # Подстановка знака для суммы если он есть
        if sl.amount and sl.amountsign == '-':
            sl.amount = sl.amount * Decimal(sl.amountsign+'1')

        # Первая строка содержит счет всей выписки
        if self.cur_record == 1:
            self.statement.account = sl.account

        sl = self.confbank.bank.after_row_parsed(sl, line)

        return sl

    def _parse_value(self, value, field):
        tp = type(getattr(bankparser.statementline.StatementLine, field))
        if tp == datetime:
            return self._parse_datetime(value)
        elif tp == float:
            return self._parse_float(value)
        elif tp == Decimal:
            return self._parse_decimal(value)
        else:
            return value.strip()

    def _parse_datetime(self, value):
        date_format = self.confbank.bank.dateformat
        return datetime.strptime(value, date_format)

    @staticmethod
    def _parse_float(value):
        val = value.replace(',', '.')
        return float(val)\

    @staticmethod
    def _parse_decimal(value):
        val = value.replace(',', '.').strip('0')
        val = val.replace(' ','')
        return Decimal(val)
