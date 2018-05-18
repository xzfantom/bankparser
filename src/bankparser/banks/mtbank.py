# Settings for mtbank
from bankparser.parsercsv import ParserCSV
import re

class Bank(ParserCSV):

    def __init__(self):
        super().__init__()
        self.banktitle = 'МТБанк'
        self.banksite = 'https://www.mtbank.by/'
        self.statementfile = 'statement.csv'
        self.encoding = 'UTF-8'
        self.dateformat = '%d.%m.%Y %H:%M:%S'
        self.delimiter = ','
        self.startafter = '"Тип","Дата операции"'
        self.stopafter = '"  Типы операций"'
        self.type = 'Bank'
        self.fields = ['type', 'date', 'date-processing', 'place', 'description', 'card', 'currency', 'amount-operation', 'amount', 'balance']

    def parse_header(self, content, statement):
        match = re.search(r'"Номер счета:","(.*)"', content)
        if (match):
            statement.account = match[1]
        return statement

    def get_transaction_table(self, lines):
        strfile = []
        for line in lines:
            match = re.search(r'("[A|T]","\d\d.\d\d.\d\d\d\d \d\d:\d\d:\d\d".*$)', line)
            if match:
                strfile.append(line)
    
        return strfile

#"[A|T]","\d\d.\d\d.\d\d\d\d \d\d:\d\d:\d\d".*$