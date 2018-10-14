from datetime import datetime
from decimal import Decimal


class StatementLine:
    # Поля GNUCash 3.3 для CSV
    #   Дата, Номер, Описание, Заметки, Transaction Comodity,
    #   Причина аннулирования, Действие, Счет, Депозит, Снято,
    #   Цена, Памятка, Согласовано, Reconcile Date, Transfer Action,
    #   Жиросчет, Transfer Memo, Transfer Reconciled, Transfer Reconcile Date

    # start_fields qif_letter;description
    date = datetime.now()  # D;Дата проводки; QIF, CSV
    numbercheck = ""  # N;Номер чека (Номер транзакции ?); QIF, CSV
    description = ""  # M;Описание; QIF, CSV
    notes = ""  # Заметки; CSV
    comodity = ""  # Валюта транзакции; CSV
    cancelreason = ""  # Причина аннулирования; CSV
    action = ""  # N;Операция (для ценных бумаг): buy, sell. Для приведения к стандартным операциям используйте секцию [action]. Например [action] Покупка=buy; QIF, CSV
    account = ""  # ;Счет; QIF, CSV
    amount = Decimal(0)  # T;Сумма
    amountsign = ""  # ;Слово указание на списание или зачисление, для определения знака суммы
    price = Decimal(0)  # I;Цена (для ценных бумаг); QIF, CSV
    memo = ""  # Памятка; CSV
    reconciled = ""  # Согласовано; CSV
    reconciledate = datetime.now()  # Дата согласования; CSV
    transferaction = ""  # Transfer Action; CSV
    giroaccount = ""  # Жиросчет; CSV
    transfermemo = ""  # Transfer Memo; CSV
    transferreconciled = ""  # Transfer Reconciled; CSV
    transferreconciledate = datetime.now()  # Transfer Reconcile Date; CSV    
    securityname = ""  # Y;Имя ценной бумаги    
    quantity = Decimal(0)  # Q;Количество бумаг
    commission = Decimal(0)  # O;Комиссия (для ценных бумаг)
    payee = ""  # P;Получатель платежа    
    category = ""  # L;Название счета для списания/зачисления (второй счет проводки). Например, Расходы:Питание
    nkd = Decimal(0) #  ;Накопленный куппоный доход (для облигаций). Добавляется к цене облигации
    # end_fields

    def __repr__(self):
        return '<stline <date={0} amount={1} descr={2}>>'.format(self.date.strftime('%d-%m-%Y'), self.amount, self.description)
