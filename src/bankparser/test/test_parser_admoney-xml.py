import unittest
from decimal import Decimal

import bankparser.parserxml


class ADMoneyTest(unittest.TestCase):
    bank = 'admoney-xml'

    sampletxt = """<?xml version='1.0' encoding='windows-1251' ?>
<ROOT>
<details>
<detail>
			<money_account>11111</money_account>
			<a_date>19/10/2016 14:58:14</a_date>
			<volume>258.30</volume>
			<acc_code>12345-000</acc_code>
			<place_name>КЦБ ММВБ</place_name>
			<direction>зачисление</direction>
			<comment>Внешнее зачисление: купон</comment>
			<broker_nds>0.00</broker_nds>
			<other_nds>0.00</other_nds>
			<type>6</type>
			<curr>RUR</curr>
		</detail>
		<detail>
			<money_account>11111</money_account>
			<a_date>21/10/2016 00:13:55</a_date>
			<volume>0.40</volume>
			<acc_code>12345-000</acc_code>
			<place_name>КЦБ ММВБ</place_name>
			<direction>списание</direction>
			<comment>Комиссия банка</comment>
			<broker_nds>0.00</broker_nds>
			<other_nds>0.00</other_nds>
			<type>6</type>
			<curr>RUR</curr>
		</detail>
		<detail>
			<money_account>11111</money_account>
			<a_date>21/10/2016 00:13:55</a_date>
			<volume>0.41</volume>
			<acc_code>12345-000</acc_code>
			<place_name>КЦБ ММВБ</place_name>
			<direction>списание</direction>
			<comment>Оплата НКД по сделкам покупки ц.б.  на биржевом рынке</comment>
			<broker_nds>0.00</broker_nds>
			<other_nds>0.00</other_nds>
			<type>0</type>
			<curr>RUR</curr>
		</detail>
		<detail>
			<money_account>11111</money_account>
			<a_date>21/10/2016 00:13:55</a_date>
			<volume>991.80</volume>
			<acc_code>12345-000</acc_code>
			<place_name>КЦБ ММВБ</place_name>
			<direction>списание</direction>
			<comment>Оплата сделок покупки  ц.б. на биржевом рынке</comment>
			<broker_nds>0.00</broker_nds>
			<other_nds>0.00</other_nds>
			<type>0</type>
			<curr>RUR</curr>
		</detail>
	</details>
	<accounts>
		<account>
			<curr>RUR</curr>
			<money_account>11111</money_account>
			<money_income_rest>1042.56</money_income_rest>
			<money_real_rest>308.25</money_real_rest>
			<money_saldo>-734.31</money_saldo>
			<income_tran>258.30</income_tran>
			<outcome_tran>0.00</outcome_tran>
			<income_trade>0.00</income_trade>
			<outcome_trade>992.21</outcome_trade>
			<subbroker_fee>0.00</subbroker_fee>
			<broker_fee>0.40</broker_fee>
			<other_fee>0.00</other_fee>
			<broker_nds>0.00</broker_nds>
			<other_nds>0.00</other_nds>
			<is_official>Y</is_official>
			<taxes>0.00</taxes>
			<IsCurMark>0</IsCurMark>
		</account>
		<account>
			<curr>USD</curr>
			<money_account />
			<money_income_rest>0.00</money_income_rest>
			<money_real_rest>0.00</money_real_rest>
			<money_saldo>0.00</money_saldo>
			<income_tran>0.00</income_tran>
			<outcome_tran>0.00</outcome_tran>
			<income_trade>0.00</income_trade>
			<outcome_trade>0.00</outcome_trade>
			<subbroker_fee>0.00</subbroker_fee>
			<broker_fee>0.00</broker_fee>
			<other_fee>0.00</other_fee>
			<broker_nds>0.00</broker_nds>
			<other_nds>0.00</other_nds>
			<is_official>Y</is_official>
			<taxes>0.00</taxes>
			<IsCurMark>0</IsCurMark>
		</account>
		<account>
			<curr>EUR</curr>
			<money_account />
			<money_income_rest>0.00</money_income_rest>
			<money_real_rest>0.00</money_real_rest>
			<money_saldo>0.00</money_saldo>
			<income_tran>0.00</income_tran>
			<outcome_tran>0.00</outcome_tran>
			<income_trade>0.00</income_trade>
			<outcome_trade>0.00</outcome_trade>
			<subbroker_fee>0.00</subbroker_fee>
			<broker_fee>0.00</broker_fee>
			<other_fee>0.00</other_fee>
			<broker_nds>0.00</broker_nds>
			<other_nds>0.00</other_nds>
			<is_official>Y</is_official>
			<taxes>0.00</taxes>
			<IsCurMark>0</IsCurMark>
		</account>
		<account>
			<curr>RUR</curr>
			<money_account>11111-2</money_account>
			<money_income_rest>0.00</money_income_rest>
			<money_real_rest>0.00</money_real_rest>
			<money_saldo>0.00</money_saldo>
			<income_tran>0.00</income_tran>
			<outcome_tran>0.00</outcome_tran>
			<income_trade>0.00</income_trade>
			<outcome_trade>0.00</outcome_trade>
			<subbroker_fee>0.00</subbroker_fee>
			<broker_fee>0.00</broker_fee>
			<other_fee>0.00</other_fee>
			<broker_nds>0.00</broker_nds>
			<other_nds>0.00</other_nds>
			<is_official>Y</is_official>
			<taxes>0.00</taxes>
			<IsCurMark>1</IsCurMark>
		</account>
		<account>
			<curr>USD</curr>
			<money_account>22222</money_account>
			<money_income_rest>0.00</money_income_rest>
			<money_real_rest>0.00</money_real_rest>
			<money_saldo>0.00</money_saldo>
			<income_tran>0.00</income_tran>
			<outcome_tran>0.00</outcome_tran>
			<income_trade>0.00</income_trade>
			<outcome_trade>0.00</outcome_trade>
			<subbroker_fee>0.00</subbroker_fee>
			<broker_fee>0.00</broker_fee>
			<other_fee>0.00</other_fee>
			<broker_nds>0.00</broker_nds>
			<other_nds>0.00</other_nds>
			<is_official>Y</is_official>
			<taxes>0.00</taxes>
			<IsCurMark>1</IsCurMark>
		</account>
		<account>
			<curr>EUR</curr>
			<money_account>33333</money_account>
			<money_income_rest>0.00</money_income_rest>
			<money_real_rest>0.00</money_real_rest>
			<money_saldo>0.00</money_saldo>
			<income_tran>0.00</income_tran>
			<outcome_tran>0.00</outcome_tran>
			<income_trade>0.00</income_trade>
			<outcome_trade>0.00</outcome_trade>
			<subbroker_fee>0.00</subbroker_fee>
			<broker_fee>0.00</broker_fee>
			<other_fee>0.00</other_fee>
			<broker_nds>0.00</broker_nds>
			<other_nds>0.00</other_nds>
			<is_official>Y</is_official>
			<taxes>0.00</taxes>
			<IsCurMark>1</IsCurMark>
		</account>
		<account>
			<curr>GBP</curr>
			<money_account />
			<money_income_rest>0.00</money_income_rest>
			<money_real_rest>0.00</money_real_rest>
			<money_saldo>0.00</money_saldo>
			<income_tran>0.00</income_tran>
			<outcome_tran>0.00</outcome_tran>
			<income_trade>0.00</income_trade>
			<outcome_trade>0.00</outcome_trade>
			<subbroker_fee>0.00</subbroker_fee>
			<broker_fee>0.00</broker_fee>
			<other_fee>0.00</other_fee>
			<broker_nds>0.00</broker_nds>
			<other_nds>0.00</other_nds>
			<is_official>Y</is_official>
			<taxes>0.00</taxes>
			<IsCurMark>1</IsCurMark>
		</account>
		<account>
			<curr>CHF</curr>
			<money_account />
			<money_income_rest>0.00</money_income_rest>
			<money_real_rest>0.00</money_real_rest>
			<money_saldo>0.00</money_saldo>
			<income_tran>0.00</income_tran>
			<outcome_tran>0.00</outcome_tran>
			<income_trade>0.00</income_trade>
			<outcome_trade>0.00</outcome_trade>
			<subbroker_fee>0.00</subbroker_fee>
			<broker_fee>0.00</broker_fee>
			<other_fee>0.00</other_fee>
			<broker_nds>0.00</broker_nds>
			<other_nds>0.00</other_nds>
			<is_official>Y</is_official>
			<taxes>0.00</taxes>
			<IsCurMark>1</IsCurMark>
		</account>
	</accounts>
	<service>
		<builddate>2016-10-24T11:06:27.490</builddate>
		<code>0</code>
		<error_msg>Отчет успешно получен.</error_msg>
		<from_date>17/10/2016</from_date>
		<to_date>23/10/2016</to_date>
		<full_name>ФИО</full_name>
		<treaty>12345</treaty>
		<portfolio>Все портфели.</portfolio>
	</service>
</ROOT>
"""
    parser = bankparser.parserxml.ParserXML(bank, sampletxt, is_content=True)

    # def setUp(self):
    #     self.parser = Parser.StatementParser(self.bank, self.sampletxt)

    def test_bankname(self):
        self.assertEqual(self.parser.bankname, self.bank, 'Bank name in parser')

    def test_bankname2(self):
        self.assertEqual(self.parser.statement.bank, self.bank, 'Bank name in statement')

    def test_account(self):
        self.assertEqual(self.parser.statement.account, '12345-000', 'account in statement')

    def test_linescount(self):
        count = len(self.parser.statement.lines)
        self.assertEqual(count, 2)

    def test_line1amount(self):
        amount = self.parser.statement.lines[0].amount
        self.assertEqual(amount, Decimal('258.30'), 'Amount in first line (+)')

    def test_line2amount(self):
        amount = self.parser.statement.lines[1].amount
        self.assertEqual(amount, Decimal('-0.4'), 'Amount in second line (-)')


    def test_linedescr(self):
        descr = self.parser.statement.lines[0].description
        self.assertEqual(descr, "Внешнее зачисление: купон", 'Description in first line')
