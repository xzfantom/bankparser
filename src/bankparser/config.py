import configparser
from bankparser.confcommons import *
import os.path
import glob

#configfile='config.ini'
DEFAULT_CURRENCY = 'RUB'

SRCDIR = "src/bankparser/"

# Обязательные поля для добавления
FIELD_AMOUNT = {'name':'amount','type':'float','description':'Сумма','qif_letter':'T'}
FIELD_AMOUNTSIGN = {'name':'amountsign','type':'string','description':'Слово указание на списание или зачисление, для определения знака суммы','qif_letter':''}

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
        #accounts= {}
        #actions = {}
        #amountsigns = {}


        def _getinifile(self):
                bankinifile = self.bank + ".ini"
                paths = self._get_ini_paths()
                for path in paths:
                        bankinifile_src = os.path.join(path, bankinifile)
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
                        #print('bankini='.format(bankinifile))
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
                        for section in settings.sections():
                                if section != 'common':


                                        list = {}

                                        for key in settings[section]:
                                                #setattr(self,section,)
                                                #self.accounts[key] = settings[section][key]
                                                list[key] = settings[section][key]
                                        setattr(self, section, list)

                        # if 'accounts' in settings.sections():
                        #         setattr(self,'accounts',{})
                        #         for key in settings['accounts']:
                        #                   self.accounts[key] = settings['accounts'][key]
                        # # Чтение спика знаков
                        # if 'amountsigns' in settings.sections():
                        #         for key in settings['amountsigns']:
                        #                   self.amountsigns[key] = settings['amountsigns'][key]
                        # # Чтение названия операций для ценных бумаг
                        # if 'actions' in settings.sections():
                        #         for key in settings['actions']:
                        #                 self.actions[key] = settings['actions'][key]



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
