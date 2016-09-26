import configparser

configfile='config.ini'

FIELDS={'encoding': 'utf-8',
        'dateformat': '%Y-%m-%d %H:%M:%S'

        }

FIELD_ENCODING='encoding'
DEFAULT_ENCODING='utf-8'

DEFAULT_CURRENCY = 'RUB'

FIELD_DATEFORMAT='dateformat'
DEFAULT_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

FIELD_STARTAFTER = 'startafter'

FIELD_DELIMITER = 'delimiter'
DEFAULT_DELIMITER = ';'





class BankConfig:
        _isreadini = False
        delimiter = ';'
        bank = ""
        encoding = "utf-8"
        startafter = None
        type = "Bank"
        fields = []
        dateformat = "%Y-%m-%d %H:%M:%S"
        accounts= {}
        actions = {'buy': 'buy','sell': 'sell'}

        def readini(self,bank):
                if not self._isreadini:
                        self.bank=bank
                        bankinifile=bank+".ini"
                        settings = configparser.ConfigParser()
                        # settings=\
                        settings.read(bankinifile, encoding='utf-8')
                        # Список имен полей BankConfig
                        objfields = [arg for arg in dir(BankConfig) if not arg.startswith('_')]
                        # Чтение общих настроек банка
                        for field in objfields:
                                defaultvalue=getattr(self,field)
                                inivalue=settings["common"].get(field, defaultvalue)
                                setattr(self, field, inivalue)
                        # Список полей в массив
                        self.fields = self.fields.split(' ')
                        # Чтение спика счетов

                        for key in settings['accounts']:
                                self.accounts[key] = settings['accounts'][key]
                        # Чтение названия операций для ценных бумаг
                        for key in settings['actions']:
                                self.actions[key] = settings['actions'][key]

                        self._isreadini=True

        def printdeb(self):
                # Список имен полей BankConfig
                objfields = [arg for arg in dir(BankConfig) if not arg.startswith('_')]
                for field in objfields:
                        value = getattr(self, field)
                        print('{0} = {1}'.format(field,value))

bankconfig = BankConfig()

def getBankConfig(bank):
        bankconfig.readini(bank)
        return bankconfig




#with open(configfile, "r") as f:
    #settings = yaml.load(f)
#    settings = config.read(f, encoding='utf-8')
