from datetime import datetime
from bankparser.statement import *
from bankparser.statementline import *
from bankparser.qifline import *

class QIF:

    #statement = None
    lines = []
    type = "Bank"
    account = ""

    def __init__(self,statement = None):
        #self.statement=statement
        if statement:
            self.readstatement(statement)


    def save(self,filename):
        # Генерация файла
        strFile=self.genstr()

        with open(filename,'w',encoding='utf-8') as f:
            f.write(strFile)
        print('qif saved ({})'.format(filename))

    def printdeb(self):

        for line in self.lines:
            line.print()

    def readstatement(self,statement):
        """
        Преобразование выписки statement в строки qif

        :param statement:
        :return:
        """

        self.type = statement.type
        self.account = statement.account

        for stline in statement.lines:
            qiffields = [arg for arg in dir(QIFLine) if not arg.startswith('_')]
            statfields = [arg for arg in dir(StatementLine) if not arg.startswith('_')]
            qifline=QIFLine()
            for statfield in statfields:
                if statfield in qiffields:
                    setattr(qifline,statfield,getattr(stline,statfield))
            if qifline:
                self.lines.append(qifline)



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
        strFile += 'N'+ self.account + '\n'
        strFile += '^\n'

        strFile += '!Type:{}\n'.format(self.type)

        for line in self.lines:
            qiffields = [arg for arg in dir(QIFLine) if not arg.startswith('_')]
            for field in qiffields:
                value=getattr(line,field)
                qif_letter=qifletters[field]
                if value:
                    if field == 'date':
                        strFile += 'D' + line.date.strftime('%m/%d/%Y') + '\n'
                    else:
                        strFile += qif_letter + str(value) + '\n'

            strFile += '^\n'

        return strFile




