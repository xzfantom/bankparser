import csv
import configparser
from datetime import datetime
from decimal import Decimal

import bankparser.config
import bankparser.statement
import bankparser.statementline



class StatementParser:
    """   Базовый класс для разбора выписки"""

    def __init__(self):
        # read settings
        self.bankname = None
        self.type = None

        self.filename = None
        self.encoding = "utf-8"
        self.content = None

        self.dateformat = '%d.%m.%Y %H:%M:%S'
        self.m_descr_account = {}
        self.fields = []



    def parse(self, filename, is_content: bool=False):
        """
        Parse file or string to statetement object

        :param filename: filename or string
        :param is_content: filename is string with statement content
        :return: Statetement object
        """

        if is_content:
            self.content = filename
        else:
            # read content file in the buffer
            self.filename = filename
            encoding = self.encoding
            with open(filename, 'r', encoding=encoding)as f:
                self.content = f.read()

        statement = bankparser.statement.Statement(bank=self.bankname, typest=self.type)
        statement = self.parse_header(self.content, statement)

        reader = self._split_records()
        for line in reader:
            if not line:
                continue
            stmt_line = self._parse_record(line)
            if stmt_line:
                statement.lines.append(stmt_line)
                # Первая строка содержит счет всей выписки
                if statement.account is None:
                    statement.account = stmt_line.account

        return statement

    def _split_records(self):
        """
        Virtual function, must be declared in childrens
        Splits self.content into array of dictionary values
        One line is one transaction. Contain key/values pairs
        Myst return this array
        :return: Array of dictionaries
        """
        raise NotImplementedError

    def _parse_record(self, line):
        """
        Разбор одной строки. Строка должна быть поименована по названиям полей
        :param line:
        :return:
        """

        sl = bankparser.statementline.StatementLine()
        # Список имен полей для банка из ini файла
        inifields = line.keys() #self.confbank.bank.fields
        objfields = [arg for arg in dir(bankparser.statementline.StatementLine) if not arg.startswith('_')]
        for field in objfields:
            if field in inifields:
                rawvalue = line[field]
                # Подмена значения из списка настроек, если список есть в настр. банка
                changemap = getattr(self, 'm_' + field, None)
                if changemap:
                    rawvalue = changemap.get(rawvalue, rawvalue)
                value = self._parse_value(rawvalue, field)
                setattr(sl, field, value)

        # Здесь нужно добавить строку с именем счета
        # SАктивы: Текущие активы: Наличные
        # sl.category = "Активы: Текущие активы: Наличные"

        # Подставление счета по содержимому описания
        # Строки которые нужно искать в описании
        listDescr=list(self.m_descr_account.keys())
        for strFind in listDescr:
            if strFind in sl.description:
                sl.category = self.m_descr_account[strFind]
                break

        # Подстановка знака для суммы если он есть
        if sl.amount and sl.amountsign == '-':
            sl.amount = sl.amount * Decimal(sl.amountsign+'1')


        sl = self.after_row_parsed(sl, line)

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
        date_format = self.dateformat
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

    def read_ini(self, inifile):
        """
        Read user settings from ini file
        """
        settings = configparser.ConfigParser()
        settings.optionxform = str
        settings.read(inifile, encoding='utf-8')

        for section in settings.sections():
            maplist = {}
            for key in settings[section]:
                maplist[key] = settings[section][key]
            setattr(self, 'm_' + section, maplist)

    def after_row_parsed(self, sl, line):
        """
        Additional actions after parsing row
        Stub function, can be overwritten in childrens
        """
        return sl

    def parse_header(self, content, statement):
        """
        Parsing header
        Stub function, can be overwritten in childrens
        """
        return statement