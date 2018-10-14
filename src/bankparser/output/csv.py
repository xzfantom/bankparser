import bankparser.statementline


class CSV:
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
            with open(f, 'w', encoding='windows-1251') as stream:
                self._write_to_stream(stream)

        else:
            self._write_to_stream(f)

    def _write_to_stream(self, stream):
        # Генерация файла
        strfile = self._genstr()
        stream.write(strfile)

    def readstatement(self, statement):
        """
        Преобразование выписки statement в строки csv

        :param statement:
        :return:
        """

        self.typest = statement.typest
        self.account = statement.account

        self.lines = []

        for stline in statement.lines:
            self.lines.append(stline)

    def _genstr(self):
        strfile = ""

        for line in self.lines:
            List = [line.date.strftime('%Y-%m-%d'),
                    line.numbercheck,
                    line.description,
                    line.notes,
                    line.comodity,
                    line.cancelreason,
                    line.action,
                    line.account,
                    str(line.amount),
                    line.amountsign,
                    str(line.price),
                    line.memo,
                    line.reconciled,
                    line.reconciledate.strftime('%Y-%m-%d'),
                    line.transferaction,
                    line.giroaccount,
                    line.transfermemo,
                    line.transferreconciled,
                    line.transferreconciledate.strftime('%Y-%m-%d')]
            strfile = strfile + ";".join(List) + "\n"

        return strfile
