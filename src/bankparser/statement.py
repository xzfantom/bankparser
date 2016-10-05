from datetime import datetime
import bankparser.config as config
from bankparser.statementline import *
from bankparser.config import *


class Statement:
    account = None
    currency = DEFAULT_CURRENCY
    bank =None
    lines = []
    type = "Bank"








