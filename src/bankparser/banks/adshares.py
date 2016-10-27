# Settings for adshares
from bankparser.stdbank import StdBank


class Bank(StdBank):
    parser = 'ParserCSV'
    banktitle = 'Альфа-директ'
    description = 'Отчет об урегулированных сделках 2016. CSV формат.'
    banksite = 'http://alfadirect.ru'
    statementfile = 'report.txt'
    encoding = 'cp1251'
    dateformat = '%d/%m/%Y'
    delimiter = ';'
    startafter = 'Дата урегулирования сделки;Портфель;'
    type = 'Invst'
    fields = ['date', 'account', 'market', 'Date-podtver', 'securityname', 'securitycod', 'action', 'quantity', 'price', 'amount', 'nkd', 'commission', 'Birj-comis', 'numbersdelki', 'numrepo', 'Subbroker-comis', 'Subagent-comis', 'contragent', 'primechanie']
    m_action = {'Куплено': 'Buy', 'Продано': 'Sell'}
    # переменные задаваемые в Ini файле
    m_vars = {'category': None}  # Денежный счет списания/зачисления

    def after_row_parsed(self, statementline, rawline):
        # Если пользователь указал счет расходов доходов, то используем его
        category = self.m_vars.get('category')
        if category:
            statementline.category = category
            statementline.action += 'X'

        # Прибавление комиссии
        statementline.amount += statementline.commission
        # Прибавление НКД
        nkd = None
        if statementline.nkd:
            statementline.amount += statementline.nkd
            nkd = ' НКД {} р. '.format(statementline.nkd)
        # Формирование описания сделки
        statementline.description = "{0} {1}. Цена {2}.{4}Номер сделки {3}".format(rawline['action'], statementline.securityname, statementline.price, rawline['numbersdelki'], nkd)

