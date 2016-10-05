import bankparser.statementline
import bankparser.qifline

class QIF:

    lines = []
    type = "Bank"
    account = ""

    def __init__(self,statement = None):
        #self.statement=statement
        if statement:
            self.readstatement(statement)


    def write(self,f):
        """
        Запись qif в файл
        :param filename:
        :return:
        """

        if isinstance(f, str):
            with open(f,'w',encoding='utf-8') as stream:
                self._write_to_stream(stream)
                #print('qif saved ({})'.format(f))
                #f1.write(strFile)
        else:
            self._write_to_stream(f)

    def _write_to_stream(self,stream):
        # Генерация файла
        strFile = self._genstr()
        stream.write(strFile)

    def readstatement(self,statement):
        """
        Преобразование выписки statement в строки qif

        :param statement:
        :return:
        """

        self.type = statement.type
        self.account = statement.account

        for stline in statement.lines:
            qiffields = [arg for arg in dir(bankparser.qifline.QIFLine) if not arg.startswith('_')]
            statfields = [arg for arg in dir(bankparser.statementline.StatementLine) if not arg.startswith('_')]
            qifline = bankparser.qifline.QIFLine()
            for statfield in statfields:
                if statfield in qiffields:
                    setattr(qifline,statfield,getattr(stline,statfield))
            if qifline:
                self.lines.append(qifline)



    def _genstr(self):
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
        strFile += 'N' + self.account + '\n'
        strFile += '^\n'

        strFile += '!Type:{}\n'.format(self.type)

        for line in self.lines:
            qiffields = [arg for arg in dir(bankparser.qifline.QIFLine) if not arg.startswith('_')]
            for field in qiffields:
                value=getattr(line,field)
                qif_letter=bankparser.qifline.qifletters[field]
                if value:
                    if field == 'date':
                        strFile += 'D' + line.date.strftime('%Y-%m-%d') + '\n'
                    else:
                        strFile += qif_letter + str(value) + '\n'

            strFile += '^\n'

        return strFile




