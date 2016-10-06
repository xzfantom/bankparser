import os.path
import glob
import configparser

from bankparser.confcommons import *

CNAME = 'name'
CCOMMON = 'common'


class BankConfig:
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

    @staticmethod
    def _get_ini_paths():
        moddir = os.path.dirname(__file__)
        paths = ("", moddir)
        return paths

    def get_list_banks(self):
        listpaths = self._get_ini_paths()
        for path in listpaths:
            # banks = None
            banks = self._get_list_banks_in_dir(path)
            if banks:
                return banks
        return None

    @staticmethod
    def _get_list_banks_in_dir(folder):
        mask = os.path.join(folder, "*.ini")
        listbanks = []
        for file in glob.glob(mask):
            inifile = os.path.basename(file)
            bank = os.path.splitext(inifile)[0]
            listbanks.append(bank)
        return listbanks

    def readini(self, bank):
        if self.bank != bank:
            self.commons = ConfCommons()
            self.bank = bank
            bankinifile = self._getinifile()
            if not bankinifile:
                print('Не найден ini файл')
                raise FileNotFoundError("Не найден ini для банка {}".format(bank))
            # print('bankini='.format(bankinifile))
            self.inifile = bankinifile
            settings = configparser.ConfigParser()
            settings.read(bankinifile, encoding='utf-8')
            if CCOMMON in settings.sections():
                # Список имен полей BankConfig
                objfields = [arg for arg in dir(ConfCommons) if not arg.startswith('_')]
                # Чтение общих настроек банка
                for field in objfields:
                    defaultvalue = getattr(self.commons, field)
                    inivalue = settings[CCOMMON].get(field, defaultvalue)
                    setattr(self.commons, field, inivalue)
                # Список полей в массив
                self.commons.fields = self.commons.fields.split(' ')

                # self.commons.fields = self.commons.fields.split(' ')

            for section in settings.sections():
                if section != CCOMMON:

                    maplist = {}

                    for key in settings[section]:
                        maplist[key] = settings[section][key]
                    setattr(self, section, maplist)


bankconfig = BankConfig()


def get_bank_config(bank):
    bankconfig.readini(bank)
    return bankconfig
