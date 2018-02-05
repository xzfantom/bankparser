class Statement:

    def __init__(self, account=None, bank=None, typest='Bank', currency='RUB'):
        self.account = account
        self.bank = bank
        self.typest = typest
        self.currency = currency
        self.lines = []



