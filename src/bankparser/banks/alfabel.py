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
        self.dateformat = '%d.%m.%Y'
        self.delimiter = ';'
        self.startafter = '"Тип","Дата операции"'
        self.stopafter = '"  Типы операций"'
        self.type = 'Bank'
        self.fields = ['date', 'description', 'amount', 'currency', 'amount-operation', 'currency-operation']
        self.transaction_pattern = re.compile(r'\d\d.\d\d.\d{4};')
        self.garbage_pattern = re.compile(r'(;\d{8}.{64})')
        self.account_pattern = re.compile(r'\.{3}(.*)\.{3}')

    def parse_header(self, content, statement):
        match = self.account_pattern.search(content)
        if (match):
            statement.account = match[1]
        return statement

    def get_transaction_table(self, lines):
        strfile = []
        for line in lines:
            match = self.transaction_pattern.search(line)
            if match:
                strfile.append(self.convert_line(line))
    
        return strfile

    def convert_line(self, line):
        # removing garbage from line
        ll = self.garbage_pattern.sub(";", line)

        return ll
