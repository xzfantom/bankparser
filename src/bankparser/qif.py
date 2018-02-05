import bankparser.statementline
import bankparser.qifline


class QIF:
    lines = []
    type = "Bank"
    account = ""

    def __init__(self, statement=None):
        # self.statement=statement
        if statement:
            self.readstatement(statement)

    def write(self, f):
        """
        Запись qif в файл
        :param f: Имя файла или открытый поток
        :return:
        """

        if isinstance(f, str):
            with open(f, 'w', encoding='utf-8') as stream:
                self._write_to_stream(stream)
                # print('qif saved ({})'.format(f))
                # f1.write(strFile)
        else:
            self._write_to_stream(f)

    def _write_to_stream(self, stream):
        # Генерация файла
        strfile = self._genstr()
        stream.write(strfile)

    def readstatement(self, statement):
        """
        Преобразование выписки statement в строки qif

        :param statement:
        :return:
        """

        self.typest = statement.typest
        self.account = statement.account

        self.lines = []

        for stline in statement.lines:
            qiffields = [arg for arg in dir(bankparser.qifline.QIFLine) if not arg.startswith('_')]
            statfields = [arg for arg in dir(bankparser.statementline.StatementLine) if not arg.startswith('_')]
            qifline = bankparser.qifline.QIFLine()
            for statfield in statfields:
                if statfield in qiffields:
                    setattr(qifline, statfield, getattr(stline, statfield))
            if qifline:
                self.lines.append(qifline)

    def _genstr(self):
        strfile = ""

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

        strfile += '!Account\n'
        strfile += 'N' + self.account + '\n'
        strfile += '^\n'

        strfile += '!Type:{}\n'.format(self.type)

        for line in self.lines:
            qiffields = [arg for arg in dir(bankparser.qifline.QIFLine) if not arg.startswith('_')]
            for field in qiffields:
                value = getattr(line, field)
                qif_letter = bankparser.qifline.qifletters[field]
                if value:
                    if field == 'date':
                        strfile += 'D' + line.date.strftime('%Y-%m-%d') + '\n'
                    else:
                        strfile += qif_letter + str(value) + '\n'

            strfile += '^\n'

        return strfile
