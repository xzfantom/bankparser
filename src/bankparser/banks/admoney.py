# Settings for alfa
from bankparser.stdbank import StdBank

class Bank(StdBank):
    banktitle = 'Альфа-директ'
    banksite = 'http://alfadirect.ru'
    description = 'Отчет о движении денежных средств 2016. CSV формат. Обрабатываются все движения по счету'
    statementfile = 'report.txt'
    encoding = 'cp1251'
    dateformat = '%d/%m/%Y %H:%M:%S'
    delimiter = ';'
    startafter = 'Дата;Портфель;'
    type = 'Bank'
    fields = ['date', 'account', 'market', 'amount', 'amountsign', 'description', 'currency']

    amountsign = {'списание': '-'}


