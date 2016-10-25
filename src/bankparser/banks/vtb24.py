# Settings for vtb24
from bankparser.stdbank import StdBank

class Bank(StdBank):
    banktitle = 'ВТБ24'
    banksite = 'http://vtb24.ru'
    statementfile = 'statement.csv'
    encoding = 'cp1251'
    dateformat = '%Y-%m-%d %H:%M:%S'
    delimiter = ';'
    startafter = 'Номер карты/'
    type = 'Bank'
    fields = ['account', 'date', 'date-processing', 'amount-operation', 'currency-operation', 'amount', ' currency', 'description', 'status']
