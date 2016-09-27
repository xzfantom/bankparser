# Generate automatically by build.py
# don`t change manually

from datetime import datetime


class StatementLine:

   date = datetime.now() # Дата проводки
   account = "" # Счет
   amount = 0.0 # Сумма
   description = "" # Описание
   action = "" # Операция (для ценных бумаг): buy, sell
   securityname = "" # Имя ценной бумаги
   price = 0.0 # Цена (для ценных бумаг)
   quantity = 0.0 # Количество бумаг 
   commission = 0.0 # Комиссия (для ценных бумаг)
