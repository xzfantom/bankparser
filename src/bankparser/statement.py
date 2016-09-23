from datetime import datetime
import bankparser.config as config
from bankparser.statementline import *
from bankparser.config import *


class Statement:
    account = None
    currency = DEFAULT_CURRENCY
    bank =None
    lines = []

    def print(self):
        print('statement {0} {1}'.format(self.bank,self.account))
        for line in self.lines:
            print('{0} {1} {2}'.format(line.date,line.amount,line.description))







