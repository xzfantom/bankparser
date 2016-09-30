import configparser
from bankparser.confcommons import *
import os.path
import glob

DEFAULT_CURRENCY = 'RUB'

#SRCDIR = "src/bankparser/"

#CNAME = 'name'
CCOMMON = 'common'

# Обязательные поля для добавления
#FIELD_AMOUNT = {CNAME:'amount','type':'float','description':'Сумма','qif_letter':'T'}
#FIELD_AMOUNTSIGN = {CNAME:'amountsign','type':'string','description':'Слово указание на списание или зачисление, для определения знака суммы','qif_letter':''}
#FIELD_ACCOUNT = {CNAME:'account','type':'string','description':'Счет','qif_letter':''}

# Поля commons
#FIELD_DELIMITER={CNAME: 'delimiter','default':'";"','description':'Разделитель полей'}
#FIELD_DATEFORMAT={CNAME: 'dateformat','default':'"%Y-%m-%d %H:%M:%S"','description':'Формат даты в банковском файле'}
#FIELD_ENCODING={CNAME: 'encoding','default':'"utf-8"','description':'Кодировка файла'}
#FIELD_FIELDS={CNAME: 'fields','default':'[]','description':'Имена полей в файле через пробел, нужные поля должны совпадать с именем в описанни доступных полей'}
#FIELD_STARTAFTER={CNAME: 'startafter','default':'None','description':'Начинать разбор строк со следующей, после стоки начинающейся с указанных символов'}
#FIELD_TYPE={CNAME: 'type','default':'"Bank"','description':'Тип выписки: Bank или Invst (обычная или операции с ценными бумагами)'}

class BankConfig:
        #_isreadini = False
        bank = ""
        inifile = ""
        commons = ConfCommons()

        def _getinifile(self):
                bankinifile = self.bank + ".ini"
                paths = self._get_ini_paths()
                for path in paths:
                        bankinifile_src = os.path.join(path, bankinifile)
                        if os.path.exists(bankinifile_src):
                                return bankinifile_src
                return None

        def _get_ini_paths(self):
                moddir=os.path.dirname(__file__)
                paths=("",moddir)
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
                        if not bankinifile:
                                raise FileNotFoundError ("Не найден ini для банка {}".format(bank))
                        #print('bankini='.format(bankinifile))
                        self.inifile=bankinifile
                        settings = configparser.ConfigParser()
                        settings.read(bankinifile, encoding='utf-8')
                        if CCOMMON in settings.sections():
                                # Список имен полей BankConfig
                                objfields = [arg for arg in dir(ConfCommons) if not arg.startswith('_')]
                                # Чтение общих настроек банка
                                for field in objfields:
                                        defaultvalue=getattr(self.commons,field)
                                        inivalue=settings[CCOMMON].get(field, defaultvalue)
                                        setattr(self.commons, field, inivalue)
                                # Список полей в массив
                                self.commons.fields = self.commons.fields.split(' ')

                                #self.commons.fields = self.commons.fields.split(' ')
                        # Чтение спика счетов
                        for section in settings.sections():
                                if section != CCOMMON:


                                        list = {}

                                        for key in settings[section]:
                                                #setattr(self,section,)
                                                #self.accounts[key] = settings[section][key]
                                                list[key] = settings[section][key]
                                        setattr(self, section, list)

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
