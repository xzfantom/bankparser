import unittest
import datetime
from decimal import Decimal

import bankparser.parsercsv


class Vtb24Test(unittest.TestCase):
    bank = 'vtb24'

    sampletxt = """
Номер карты/счета/договора;Дата операции;Дата обработки;Сумма операции;Валюта операции;Сумма пересчитанная в валюту счета;Валюта счета;Основание;Статус',
'40817;2016-09-15 09:02:50;2016-09-15;11388,91;RUR;11388,91;RUR;Зарплата;Исполнено
'40817;2016-09-18 16:47:57;2016-09-18;-44,30;RUR;-44,30;RUR;Операция по карте;Исполнено
'40817;2016-09-18 16:20:25;2016-09-18;-644,00;RUR;-644,00;RUR;Оплата товаров и услуг;Исполнено
'40817;2016-09-18 14:19:26;2016-09-18;-1701,00;RUR;-1701,00;RUR;XXXXXX.;Исполнено
"""

    parser = bankparser.parsercsv.ParserCSV(bank, sampletxt, is_content=True)


    def setUp(self):

        # init change tables
        m_account = {'\'40817': 'my_account'}
        setattr(self.parser.confbank.bank, 'm_account', m_account)

        m_descr_account = {'Зарплата': 'Доходы:Зарплата'}
        setattr(self.parser.confbank.bank, 'm_descr_account', m_descr_account)

        self.parser._parse()

    def test_bankname(self):
        self.assertEqual(self.parser.bankname, self.bank, 'Имя банка в объекте parser')

    def test_bankname2(self):
        self.assertEqual(self.parser.statement.bank, self.bank, 'Имя банка в выписке')

    def test_account(self):
        self.assertEqual(self.parser.statement.account, '\'40817', 'Счет в выписке')

    def test_linescount(self):
        count = len(self.parser.statement.lines)
        self.assertEqual(count, 4)

    def test_lineaccount1(self):
        account = self.parser.statement.lines[0].account
        self.assertEqual(account, 'my_account')

    def test_lineamount1(self):
        amount = self.parser.statement.lines[0].amount
        self.assertEqual(amount, Decimal('11388.91'))

    def test_lineamount2(self):
        amount = self.parser.statement.lines[1].amount
        self.assertEqual(amount, Decimal('-44.30'))

    def test_linedescr(self):
        descr = self.parser.statement.lines[0].description
        self.assertEqual(descr, "Зарплата")

    def test_linecategory(self):
        category = self.parser.statement.lines[0].category
        self.assertEqual(category, "Доходы:Зарплата", "Category")

    def test_date(self):
        date1 = self.parser.statement.lines[0].date.date()
        self.assertEqual(date1, datetime.date(2016, 9, 15))
