from datetime import datetime
from bankparser.statement import *
from bankparser.statementline import *

class QIFLine:
    date = datetime.now()
    amount = 0.0
    description = ""
    account = ""

class QIF:

    statement = None

    def __init__(self,statement):
        self.statement=statement


    def save(self,filename):
        # Генерация файла
        strFile=self.genstr()

        with open(filename,'w',encoding='utf-8') as f:
            f.write(strFile)
        print('qif saved ({})'.format(filename))

    def genstr(self):
        strFile=""

        # !Account
        # NJoint Brokerage  Account
        # ^
        # !Type:Bank
        # D03 / 04 / 10
        # T - 20.28
        # PYOUR LOCAL SUPERMARKET
        # ^
        # D03 / 03 / 10
        # T - 421.35
        # PSPRINGFIELD WATER UTILITY
        # ^

        strFile += '!Account\n'
        strFile += 'N'+ self.statement.account + '\n'
        strFile += '^\n'

        strFile += '!Type:Bank\n'

        for line in self.statement.lines:

            strFile+='D'+ line.date.strftime('%m/%d/%Y') + '\n'
            strFile+='T'+str(line.amount) + '\n'
            strFile+='P'+str(line.description) + '\n'

            strFile += '^\n'

        return strFile




