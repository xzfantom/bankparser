from datetime import datetime
from decimal import Decimal


class StatementLine:
    # start_fields qif_letter;description
    amount = Decimal(0)  # T;Сумма
    amountsign = ""  # ;Слово указание на списание или зачисление, для определения знака суммы
    account = ""  # ;Счет
    date = datetime.now()  # D;Дата проводки
    description = ""  # M;Описание
    action = ""  # N;Операция (для ценных бумаг): buy, sell. Для приведения к стандартным операциям используйте секцию [action]. Например [action] Покупка=buy
    securityname = ""  # Y;Имя ценной бумаги
    price = Decimal(0)  # I;Цена (для ценных бумаг)
    quantity = Decimal(0)  # Q;Количество бумаг
    commission = Decimal(0)  # O;Комиссия (для ценных бумаг)
    payee = ""  # P;Получатель платежа
    numbercheck = ""  # N;Номер чека (Номер транзакции ?)
    category = ""  # L;Название счета для списания/зачисления (второй счет проводки). Например, Расходы:Питание
    nkd = Decimal(0) #  ;НКД (для облигаций). Добавляется к цене облигации
    # end_fields

    def __repr__(self):
        return '<stline <date={0} amount={1} descr={2}>>'.format(self.date.strftime('%d-%m-%Y'), self.amount, self.description)
