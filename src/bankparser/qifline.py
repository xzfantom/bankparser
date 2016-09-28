# Generate automatically by build.py
# don`t change manually

from datetime import datetime


class QIFLine:

   amount = 0.0 # Сумма
   date = datetime.now() # Дата проводки
   description = "" # Описание
   action = "" # Операция (для ценных бумаг): buy, sell. Для приведения к стандартным операциям используйте секцию [action]. Например [action] Покупка=buy
   securityname = "" # Имя ценной бумаги
   price = 0.0 # Цена (для ценных бумаг)
   quantity = 0.0 # Количество бумаг 
   commission = 0.0 # Комиссия (для ценных бумаг)


qifletters = {'amount': 'T', 'date': 'D', 'description': 'P', 'action': 'N', 'securityname': 'Y', 'price': 'I', 'quantity': 'Q', 'commission': 'O'}