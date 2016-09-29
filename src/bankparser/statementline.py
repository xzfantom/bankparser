# Generate automatically by build.py
# don`t change manually

from datetime import datetime


class StatementLine:

   amount = 0.0 # Сумма
   amountsign = "" # Слово указание на списание или зачисление, для определения знака суммы
   account = "" # Счет
   date = datetime.now() # Дата проводки
   description = "" # Описание
   action = "" # Операция (для ценных бумаг): buy, sell. Для приведения к стандартным операциям используйте секцию [action]. Например [action] Покупка=buy
   securityname = "" # Имя ценной бумаги
   price = 0.0 # Цена (для ценных бумаг)
   quantity = 0.0 # Количество бумаг 
   commission = 0.0 # Комиссия (для ценных бумаг)
   payee = "" # Получатель платежа
   numbercheck = "" # Номер чека (Номер транзакции ?)
   category = "" # Название счета для списания/зачисления (второй счет проводки). Например, Расходы:Питание
