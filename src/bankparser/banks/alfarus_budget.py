# Settings for Альфабанк
from bankparser.parsercsv import ParserCSV
import re

class Bank(ParserCSV):

    def __init__(self):
        super().__init__()
        self.banktitle = 'Альфабанк'
        self.banksite = 'https://www.alfabank.by/'
        self.statementfile = 'statement.csv'
        self.encoding = 'windows-1251'
        self.dateformat = '%Y.%m.%d'
        self.delimiter = ';'
        self.startafter = '"Тип","Дата операции"'
        self.stopafter = '"  Типы операций"'
        self.type = 'Bank'
        self.fields = ['date', 'amountsign',  'category', 'amount', 'currency', 'account', 'description', 'comment']
        self.transaction_pattern = re.compile(r'"\d{4}.\d\d.\d\d";')
        self.m_amountsign = {'Расход': '-'}

    def get_transaction_table(self, lines):
        strfile = []
        for line in lines:
            match = self.transaction_pattern.search(line)
            if match:
                strfile.append(line)
    
        return strfile

