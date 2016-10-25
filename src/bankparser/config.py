import os.path
import glob
import configparser
import importlib
#import bankparser.stdbank

#import bankparser.configcomm

#CNAME = 'name'
#CCOMMON = 'common'


class BankConfig:
    #bankname = ""
    #inifile = ""
    #commons = bankparser.configcomm.ConfCommons()
    bank = None

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
        path1 = os.path.join(moddir, 'banks')
        paths = [path1]
        return paths

    @staticmethod
    def get_list_banks():
        listpaths = BankConfig._get_ini_paths()
        for path in listpaths:
            # banks = None
            banks = BankConfig._get_list_banks_in_dir(path)
            if banks:
                return banks
        return None

    @staticmethod
    def _get_list_banks_in_dir(folder):
        mask = os.path.join(folder, "*.py")
        listbanks = []
        for file in glob.glob(mask):
            inifile = os.path.basename(file)
            bank = os.path.splitext(inifile)[0]
            listbanks.append(bank)
        return listbanks

    def _read_ini(self):
        """
        Чтене настроек пользователя для банка из ini файла
        ini файлы ищем в:
        ~/.bankparser

        :return:
        """
        inifile = self.bank.bankname + '.ini'
        inifiles = []
        userpath = os.path.expanduser('~/.bankparser')
        inifiles.append(os.path.join(userpath,inifile))

        settings = configparser.ConfigParser()
        settings.read(inifiles, encoding='utf-8')


        for section in settings.sections():


                maplist = {}

                for key in settings[section]:
                    maplist[key] = settings[section][key]
                setattr(self.bank, section, maplist)


    def read_bank(self, bankname):
        if (not self.bank) or (self.bank.bankname != bankname):
            #self.commons = bankparser.configcomm.ConfCommons()
            #self.bankname = bankname
            # bankinifile = self._getinifile()
            # if not bankinifile:
            #     print('Не найден ini файл')
            #     raise FileNotFoundError("Не найден ini для банка {}".format(bank))
            # print('bankini='.format(bankinifile))
            modbank = importlib.import_module("bankparser.banks." + bankname)
            if not modbank:
                print('Не найден py файл')
                raise FileNotFoundError("Не найден файл .py для банка {}".format(bankname))
            bankcls = getattr(modbank, 'Bank')
            self.bank = bankcls()
            self.bank.bankname = bankname
            self._read_ini()
            self.bank.after_config_readed()
            # func = getattr(self.bank,'after_config_readed', None)
            # if func:
            #     func()
            # self.inifile = bankinifile
            # settings = configparser.ConfigParser()
            # settings.read(bankinifile, encoding='utf-8')
            # if CCOMMON in settings.sections():
            #     # Список имен полей BankConfig
            #     objfields = [arg for arg in dir(bankparser.configcomm.ConfCommons) if not arg.startswith('_')]
            #     # Чтение общих настроек банка
            #     for field in objfields:
            #         defaultvalue = getattr(self.commons, field)
            #         inivalue = settings[CCOMMON].get(field, defaultvalue)
            #         setattr(self.commons, field, inivalue)
            #     # Список полей в массив
            #     self.commons.fields = self.commons.fields.split(' ')
            #
            #     # self.commons.fields = self.commons.fields.split(' ')
            #
            # for section in settings.sections():
            #     if section != CCOMMON:
            #
            #         maplist = {}
            #
            #         for key in settings[section]:
            #             maplist[key] = settings[section][key]
            #         setattr(self, section, maplist)


bankconfig = BankConfig()


def get_bank_config(bankname):
    bankconfig.read_bank(bankname)
    return bankconfig
