import datetime
import unittest
import io
from decimal import Decimal

import bankparser.parsercsv
import bankparser.qif


class QIFTest(unittest.TestCase):
    bank = 'vtb24'

    sampletxt = """
Номер карты/счета/договора;Дата операции;Дата обработки;Сумма операции;Валюта операции;Сумма пересчитанная в валюту счета;Валюта счета;Основание;Статус
'40817;2016-09-15 09:02:50;2016-09-15;10000,91;RUR;10000,91;RUR;Зарплата;Исполнено
'40817;2016-09-18 16:47:57;2016-09-18;-44,30;RUR;-44,30;RUR;Операция по карте;Исполнено
'40817;2016-09-18 16:20:25;2016-09-18;-644,00;RUR;-644,00;RUR;Оплата товаров и услуг;Исполнено
'40817;2016-09-18 14:19:26;2016-09-18;-1701,00;RUR;-1701,00;RUR;XXXXXX.;Исполнено
"""
    parser = bankparser.parsercsv.ParserCSV(bank, sampletxt, is_content=True)
    qif = bankparser.qif.QIF(parser.statement)

    def test_account(self):
        self.assertEqual(self.qif.account, '\'40817', 'Счет в qif')

    def test_lineamount1(self):
        amount = self.qif.lines[0].amount
        self.assertEqual(amount, Decimal('10000.91'))

    def test_lineamount2(self):
        amount = self.qif.lines[1].amount
        self.assertEqual(amount, Decimal('-44.30'))

    def test_linedescr(self):
        descr = self.qif.lines[0].description
        self.assertEqual(descr, "Зарплата")

    def test_linescount(self):
        count = len(self.qif.lines)
        self.assertEqual(count, 4)

    def test_date(self):
        date = self.qif.lines[0].date.date()
        self.assertEqual(date, datetime.date(2016, 9, 15))

    def test_write(self):
        output = io.StringIO()
        self.qif.write(output)
        contents = output.getvalue()
        output.close()
        etalon = """!Account
N'40817
^
!Type:Bank
T10000.91
D2016-09-15
MЗарплата
^
T-44.3
D2016-09-18
MОперация по карте
^
T-644
D2016-09-18
MОплата товаров и услуг
^
T-1701
D2016-09-18
MXXXXXX.
^
"""
        self.assertEqual(etalon, contents)
