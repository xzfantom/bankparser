# Generate automatically by build.py
# don`t change manually

from datetime import datetime


class QIFLine:

   amount = 0.0  # T; Сумма
   date = datetime.now()  # D; Дата проводки
   description = ""  # M; Описание
   action = ""  # N; Операция (для ценных бумаг): buy, sell. Для приведения к стандартным операциям используйте секцию [action]. Например [action] Покупка
   securityname = ""  # Y; Имя ценной бумаги
   price = 0.0  # I; Цена (для ценных бумаг)
   quantity = 0.0  # Q; Количество бумаг
   commission = 0.0  # O; Комиссия (для ценных бумаг)
   payee = ""  # P; Получатель платежа
   numbercheck = ""  # N; Номер чека (Номер транзакции ?)
   category = ""  # L; Название счета для списания/зачисления (второй счет проводки). Например, Расходы:Питание


qifletters = {'amount': 'T', 'date': 'D', 'description': 'M', 'action': 'N', 'securityname': 'Y', 'price': 'I', 'quantity': 'Q', 'commission': 'O', 'payee': 'P', 'numbercheck': 'N', 'category': 'L'}