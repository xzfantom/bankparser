from datetime import datetime
import bankparser.config as config

class StatementLine:
    date = datetime.now()
    amount = 0.0
    description = ""
    account = ""
    # invest type
    action = "" #buy, sell
    securityname = "" # имя ценной бумаги
    price = 0.0 # Цена
    quantity = 0.0 # Количество бумаг
    commission = 0.0 # Комиссия


