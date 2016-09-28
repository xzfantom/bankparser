import configparser
from bankparser.confcommons import *
import os.path
import glob

#configfile='config.ini'
DEFAULT_CURRENCY = 'RUB'

SRCDIR = "src/bankparser/"

class BankConfig:
        #_isreadini = False
        bank = ""
        inifile = ""
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

        def _getinifile(self):
                bankinifile = self.bank + ".ini"
                paths = self._get_ini_paths()
                for path in paths:
                        bankinifile_src = os.path.join(SRCDIR, bankinifile)
                        if os.path.exists(bankinifile_src):
                                return bankinifile_src
                return None

        def _get_ini_paths(self):
                paths=("",SRCDIR)
                return paths

        def get_list_banks(self):
                listpaths = self._get_ini_paths()
                for path in listpaths:
                        banks=None
                        banks = self._get_list_banks_in_dir(path)
                        if banks:
                                return banks
                return None

        def _get_list_banks_in_dir(self,dir):
                mask = os.path.join(dir, "*.ini")
                listbanks = []
                for file in glob.glob(mask):
                        inifile = os.path.basename(file)
                        bank = os.path.splitext(inifile)[0]
                        listbanks.append(bank)
                return listbanks

        def readini(self,bank):
                if self.bank != bank:
                        self.commons=ConfCommons()
                        self.bank=bank
                        bankinifile=self._getinifile()
                        self.inifile=bankinifile
                        settings = configparser.ConfigParser()
                        settings.read(bankinifile, encoding='utf-8')
                        if 'common' in settings.sections():
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
