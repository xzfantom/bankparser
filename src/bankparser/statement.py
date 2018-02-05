class Statement:

    def __init__(self, bank=None, typest='Bank', currency='RUB'):
        self.account = None
        self.bank = bank
        self.typest = typest
        self.currency = currency
        self.lines = []



