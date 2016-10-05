import unittest
import os.path
import bankparser.parser as Parser

class ADMoneyTest(unittest.TestCase):

    bank = 'admoney'
    #statfile = 'samples/statement.csv'



    sampletxt=\
                [
                '12345;02;26/09/2016;02/10/2016',
                '',
                'Дата;Портфель;Рынок;Сумма;Тип операции;Наименование операции;Валюта',
                '28/09/2016 17:05:29;12345-000;КЦБ ММВБ;721,84;зачисление;Внешнее зачисление;RUR',
                '30/09/2016 19:12:00;12345-000;КЦБ ММВБ;0,44;списание;Комиссия;RUR'
                ]
    parser = Parser.StatementParser(bank, sampletxt)
    # def setUp(self):
    #     self.parser = Parser.StatementParser(self.bank, self.sampletxt)

    def test_bankname(self):
        self.assertEqual(self.parser.bank,self.bank,'Bank name in parser')

    def test_bankname2(self):
        self.assertEqual(self.parser.statement.bank,self.bank,'Bank name in statement')

    def test_account(self):
        self.assertEqual(self.parser.statement.account, '12345-000','account in statement')

    def test_line1amount(self):
        amount = self.parser.statement.lines[0].amount
        self.assertEqual(amount, 721.84, 'Amount in first line (+)')

    def test_line2amount(self):
        amount = self.parser.statement.lines[1].amount
        self.assertEqual(amount, -0.44, 'Amount in second line (-)')

    def test_linedescr(self):
        descr = self.parser.statement.lines[0].description
        self.assertEqual(descr, "Внешнее зачисление", 'Description in first line')


# if __name__ == '__main__':
#     unittest.main()