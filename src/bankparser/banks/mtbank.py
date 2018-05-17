# Settings for mtbank
from bankparser.stdbank import StdBank

class Bank(StdBank):
    banktitle = 'МТБанк'
    banksite = 'https://www.mtbank.by/'
    statementfile = 'statement.csv'
    encoding = 'UTF-8'
    dateformat = '%d.%m.%Y %H:%M:%S'
    delimiter = ','
    startafter = '"Тип","Дата операции"'
    stopafter = '"  Типы операций"'
    type = 'Bank'
    fields = ['type', 'date', 'date-processing', 'place', 'description', 'card', 'currency', 'amount-operation', 'amount', 'balance']
    m_descr_account = {}
