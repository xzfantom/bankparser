# Settings for Belinvestbank
from bankparser.parsercsv import ParserCSV
import re

class Bank(ParserCSV):

    def __init__(self):
        super().__init__()
        self.banktitle = 'Приорбанк'
        self.banksite = 'https://www.belinvestbank.by/'
        self.statementfile = 'statement.csv'
        self.encoding = 'windows-1251'
        self.dateformat = '%Y-%m-%d %H:%M:%S'
        self.delimiter = ';'
        self.startafter = '"Тип","Дата операции"'
        self.stopafter = '"  Типы операций"'
        self.type = 'Bank'
        self.fields = ['date', 'date-processing', 'account', 'operation-type', 'description', 
            'amount-currency', 'amount-operation', 'comission-operation', 'balance', 'amount', 'comission-amount', 'status']
        self.transaction_pattern = re.compile(r'\d{4}-\d\d-\d\d \d\d:\d\d:\d\d.*$')
        self.comission_pattern = re.compile(r'(;-*[\d|\s]+\.\d\d)(\/)')
        self.currency_pattern = re.compile(r' \b\w{3};')

    def get_transaction_table(self, lines):
        strfile = []
        for line in lines:
            match = self.transaction_pattern.search(line)
            if match:
                strfile.append(self.convert_line(line))
    
        return strfile

    def convert_line(self, line):
        # dividing amount from comission
        ll = self.comission_pattern.sub(r'\1;', line)
        # removing currency
        ll = self.currency_pattern.sub(";", ll)

        return ll
