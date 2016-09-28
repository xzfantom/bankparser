import configparser
from bankparser.confcommons import *

#configfile='config.ini'
DEFAULT_CURRENCY = 'RUB'

class BankConfig:
        _isreadini = False
        commons = ConfCommons()

        # delimiter = ';'
        # bank = ""
        # encoding = "utf-8"
        # startafter = None
        # type = "Bank"
        # fields = []
        # dateformat = "%Y-%m-%d %H:%M:%S"
        accounts= {}
        actions = {}

        def clear(self):
                self._isreadini = False

        def readini(self,bank):
                if not self._isreadini:
                        self.bank=bank
                        bankinifile=bank+".ini"
                        settings = configparser.ConfigParser()
                        # settings=\
                        settings.read(bankinifile, encoding='utf-8')
                        # Список имен полей BankConfig
                        objfields = [arg for arg in dir(ConfCommons) if not arg.startswith('_')]
                        # Чтение общих настроек банка
                        for field in objfields:
                                defaultvalue=getattr(self.commons,field)
                                inivalue=settings["common"].get(field, defaultvalue)
                                setattr(self.commons, field, inivalue)
                        # Список полей в массив
                        self.commons.fields = self.commons.fields.split(' ')
                        # Чтение спика счетов
                        if 'accounts' in settings.sections():
                                for key in settings['accounts']:
                                          self.accounts[key] = settings['accounts'][key]
                        # Чтение названия операций для ценных бумаг
                        if 'actions' in settings.sections():
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
