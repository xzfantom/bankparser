# Settings for alfa Отчет о движении денежных средств 2016 xml
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
              'comment': 'description', 'type': 'ad_type'}
    m_amountsign = {'списание': '-'}  # Замена поля amountsign

    # Типы транзакций в xml альфа-директ. Описания не нашел, смотрю по факту
    ad_types = {
        'trade_money': '0',  # стоимость ценных бумаг участвующих в сделке, НКД
        'trade_commission': '2',  # Комиссия банка за сделки
        'income': '6'  # Поступления (списания?), купоны, дивиденды
        }
    # Список типов транзакций для обработки
    ad_types_read = [ad_types['income']]

    def after_row_parsed(self, statementline, rawline):
        # обрабатываем только сделки с нужным типом
        if rawline['ad_type'] in self.ad_types_read:
            return statementline
        else:
            return None

