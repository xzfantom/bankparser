# Settings for Priorbank
from bankparser.parsercsv import ParserCSV
import re

class Bank(ParserCSV):

    def __init__(self):
        super().__init__()
        self.banktitle = 'Приорбанк'
        self.banksite = 'https://www.prior.by/'
        self.statementfile = 'statement.csv'
        self.encoding = 'windows-1251'
        self.dateformat = '%d.%m.%Y %H:%M:%S'
        self.delimiter = ';'
        self.startafter = '"Тип","Дата операции"'
        self.stopafter = '"  Типы операций"'
        self.type = 'Bank'
        self.fields = ['date', 'description', 'amount-wo-comission', 'currency', 'date-operation', 'comission', 'amount', 'card']
        self.transaction_pattern = re.compile(r'^\d\d.\d\d.\d{4} \d\d:\d\d:\d\d;')
        self.account_pattern = re.compile(r'Номер контракта:;\.*(\d*)')

    def parse_header(self, content, statement):
        match = self.account_pattern.search(content)
        print(match)
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
        ar = line.split(";")
        if len(ar) == 9:
            return line

        ar.insert(4, "")
        ar[6] = "-" + ar[5]
        ll = ";".join(ar)
        print(ll)
        return ll
