# Settings for adshares

commons = {
'bankname': 'Альфа-директ',
'description': 'отчет об урегулированных сделках 2016',
'banksite':'http://alfadirect.ru',
'statementfilename':'report.txt',
'encoding':'cp1251',
'dateformat':'%d/%m/%Y',
'delimiter':';',
'startafter': 'Дата урегулирования сделки;Портфель;',
'type':'Invst',
'fields': ['date', 'account', 'market', 'Date-podtver', 'securityname', 'securitycod', 'action', 'quantity', 'price', 'amount', 'nkd', 'commission', 'Birj-comis', 'numbersdelki', 'numrepo', 'Subbroker-comis', 'Subagent-comis', 'contragent', 'primechanie']
}

action={'Куплено': 'BuyX', 'Продано': 'SellX'}

# Денежный счет списания/зачисления
category = '[Активы:Долгосрочные активы:Ценные бумаги:Альфа-Директ:Деньги Альфа-Директ]'

def after_row_parse(statementline, rawline):
    statementline.category = category
    # Прибавление комиссии
    statementline.amount += statementline.commission
    # Прибавление НКД
    if statementline.nkd:
        statementline.amount += statementline.nkd
    # Формирование описания сделки
    statementline.description = "{0} {1}. Цена {2} р.. Номер сделки {3}".format(rawline['action'], statementline.securityname, statementline.price, statementline.numbercheck)
    if statementline.nkd:
        statementline.description += '. НКД {} р.'.format(statementline.nkd)
