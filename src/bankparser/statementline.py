from datetime import datetime
import bankparser.config as config

class StatementLine:
    date = datetime.now()
    amount = 0.0
    description = ""
    account = ""

