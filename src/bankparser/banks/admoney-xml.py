# Settings for alfa
from bankparser.stdbank import StdBank

class Bank(StdBank):
    parser = 'ParserXML'  # Имя класса парсера для разбора файла. ParserCSV or ParserXML
    banktitle = 'Альфа-директ'
    banksite = 'http://alfadirect.ru'
    description = 'Отчет о движении денежных средств 2016 xml'
    statementfile = 'xml.xml'
    encoding = 'cp1251'
    dateformat = '%d/%m/%Y %H:%M:%S'
    type = 'Bank'
    xpath_tolines = './details/detail'  # для формата xml путь к элементам перечисления. Например ./details/detail
    fields = {'a_date': 'date', 'acc_code': 'account', 'volume': 'amount', 'direction': 'amountsign',
              'comment': 'description', 'type': 'type'}

    def __init__(self):
        self.maps.amountsign = {'списание': '-'}


