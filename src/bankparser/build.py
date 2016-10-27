"""
Операции построения, генерации файлов

"""

import shutil
import os
import glob
#import configparser
import bankparser.config
import importlib

class MyBuild:
    srcdir = ''
    pubdir = "c:/temp/andrey/bankparser/"
    downloadsdir = "c:/Users/Пользователь/Downloads/"

    def __init__(self, pubdir=None, srcdir=None, downloadsdir=None):
        if pubdir:
            self.pubdir = pubdir
        if srcdir:
            self.srcdir = srcdir
        if downloadsdir:
            self.downloadsdir = downloadsdir

    def buid(self):
        """
        Автоматизированные операции построения исходников:
        Генерация файла qifline.py и справки по файлу statementline.py
        Генерация справки по файлу confcommons.py
        Генерация справки по банкам, на основе ini файлов в исходниках

        :return:
        """
        maps = self._parse_fields_py(os.path.join(self.srcdir, 'statementline.py'))
        print('qifline.py generation...')
        self._write_qifline(maps)
        print('readme fields generation...')
        self._readme_replace("fields", maps)
        print('readme common generation...')
        maps = self._parse_fields_py(os.path.join(self.srcdir, 'stdbank.py'))
        self._readme_replace("commons", maps)
        banks = self._get_banks()
        print('readme banks generation...')
        self._readme_replace("banks", banks)

    # def copy_script(self):
    #     """
    #     Копирует скрипт в каталог публикации (для отладочных целей)
    #     Генерит .bat файлы для банков
    #     :return:
    #     """
    #
    #     dest_dir = os.path.join(self.pubdir, "bankparser")
    #     from_dir = self.srcdir
    #     self._copy_files(from_dir=from_dir, to_dir=dest_dir, mask='*.py')
    #
    #     dest_dir = os.path.join(self.pubdir, "bankparser/banks")
    #     from_dir = os.path.join(self.srcdir,'banks')
    #     self._copy_files(from_dir=from_dir, to_dir=dest_dir, mask='*.py')
    #
    #     # rootfile
    #     rootfile = os.path.join(self.srcdir, "bankparsercli.py")
    #     dest_dir = self.pubdir
    #     shutil.copy(rootfile, os.path.join(dest_dir, 'bankparser.py'))
    #     # generate bat vtb24
    #     banks = self._get_banks()
    #     print('generating .bat files for banks')
    #     for bank in banks:
    #         self._save_bat(bank['statementfile'], bank['bankname'])

    # def _copy_files(self, from_dir, to_dir, mask):
    #     if not os.path.exists(to_dir):
    #         print('creating dir {}'.format(to_dir))
    #         os.makedirs(to_dir)
    #     mask1 = os.path.join(from_dir, mask)
    #     print('coping {0} files to {1}'.format(mask, to_dir))
    #     for file in glob.glob(mask1):
    #         shutil.copy(file, to_dir)

    @staticmethod
    def _parse_fields_py(filename):
        """
        Считывает поля класса из файла py обрамленные
        # start_fields имя поля1;имя поля2;...
        # end_fields
        сами поля задаются в комментариях, разделяемые ;
        :param filename:
        :return:
        """
        startstr = '# start_fields'
        endstr = '# end_fields'
        f = open(filename, 'r', encoding='utf-8')
        isreading = False
        maps = []  # итоговый массив со значениями
        fields = []  # имена полей в комментариях
        for line in f:
            line = line.strip()
            if isreading:
                if line == endstr:
                    break
                mapf = {}
                # str=line.strip()
                ar = line.split('=')
                mapf['name'] = ar[0].strip()
                ar = ar[1].split('#')
                mapf['value'] = ar[0].strip()
                if len(fields) == 1:
                    mapf[fields[0]] = ar[1].strip()
                else:
                    ar = ar[1].split(';')
                    count = len(ar)
                    if count == len(fields):
                        for i in range(count):
                            mapf[fields[i]] = ar[i].strip()
                    else:
                        raise BaseException('Ошибка с полями в файле {}'.format(filename))
                maps.append(mapf)
                # print(mapf)
            if line.startswith(startstr):
                isreading = True
                # Получить список полей из комментария
                # # start_fields имя поля1;имя поля2;...
                lens = len(startstr)
                fields = line[lens:].split(';')
                for i in range(len(fields)):
                    fields[i] = fields[i].strip(' \n')

        f.close()

        return maps

    def _write_qifline(self, maps):
        filename = os.path.join(self.srcdir, 'qifline.py')
        text = self._get_qifline_text(maps)
        self._write_file(filename, text)

    @staticmethod
    def _get_qifline_text(maps):
        """
        Получение текста класса qifline


        :param maps:
        :return: Текст класса qifline
        """
        classname = 'QIFLine'
        strclass = []
        strclass += "from datetime import datetime\n"
        strclass += "from decimal import Decimal\n\n\n"
        strclass += "class {}:\n".format(classname)
        strqiflet = ""
        for field in maps:
            if field['qif_letter'] != "":
                # typestr = self.typemap.get(field['type'], field['type'])
                strclass += "    {0} = {1}  # {3}; {2}\n".format(field['name'], field['value'], field['description'],
                                                                 field['qif_letter'])

                if strqiflet != "":
                    strqiflet += ", "
                strqiflet += "'{0}': '{1}'".format(field['name'], field['qif_letter'])
        strqiflet = '\n\nqifletters = {' + strqiflet + '}\n'
        strclass += strqiflet

        return strclass

    def _write_file(self, filename, lines, encoding='utf-8', commentchar='#'):
        with open(filename, "w", encoding=encoding) as f:
            f.writelines(self._get_header(commentchar))
            f.writelines(lines)

    # def _save_bat(self, filetomove, bank):
    #     batstr = []
    #     batstr += "@echo off\n"
    #     batstr += self._get_header('rem')
    #     batstr += "set bankfile={}\n".format(filetomove)
    #     batstr += "set bank={}\n".format(bank)
    #     batstr += "set downloadsdir={}\n".format(self.downloadsdir.replace('/', '\\'))
    #     batstr += "set curdir=%~dp0\n\n"
    #     batstr += "\n"
    #
    #     batstr += "move %downloadsdir%%bankfile% %curdir%%bankfile%\n"
    #     batstr += "python.exe bankparser.py convert %bank% %curdir%%bankfile%\n".format(bank, filetomove)
    #     batstr += "pause\n"
    #
    #     filename = os.path.join(self.pubdir, bank + ".bat")
    #
    #     with open(filename, "w", encoding="cp866") as f:
    #         f.writelines(batstr)

    @staticmethod
    def _get_header(commentchar='#'):
        headerstr = []
        headerstr += "{} Generate automatically by build.py\n".format(commentchar)
        headerstr += "{} don`t change manually\n\n".format(commentchar)
        return headerstr

    def _readme_replace(self, blockname, maps):
        startblock = ".. {}_start\n".format(blockname)
        endblock = ".. {}_finish\n".format(blockname)

        with open('../../readme.rst', 'r', encoding='utf-8') as f:
            filelines = f.readlines()
        newlines = []
        readline = True
        for line in filelines:
            if line == endblock:
                readline = True
            if readline:
                newlines += line
            if line == startblock:
                readline = False
                newlines += self._get_help(blockname, maps)

        with open('../../readme.rst', 'w', encoding='utf-8') as f:
            f.writelines(newlines)

    @staticmethod
    def _get_help(blockname, maps):
        if blockname == "commons":
            return mybuild._get_help_commons(maps)
        elif blockname == "fields":
            return mybuild._get_help_fields(maps)
        elif blockname == "banks":
            return mybuild._get_help_banks(maps)

    # def _get_banks2(self):
    #     #return bankparser.config.BankConfig.get_list_banks()
    #     bankspath = os.path.join(self.srcdir, 'banks')
    #     mask = os.path.join(bankspath, "*.py")
    #     listbanks = []
    #     for file in glob.glob(mask):
    #         # confbank = configparser.ConfigParser()
    #         # confbank.read(file, encoding='utf-8')
    #         #com = confbank['common']
    #         bankname =
    #         bankmod = importlib.import_module('bankparser.banks.'+bankname)
    #         curbank = {}
    #         curbank['bank'] = os.path.splitext(os.path.basename(file))[0]
    #         curbank['bankname'] = com.get('bankname', curbank['bank'])
    #         curbank['banksite'] = com.get('banksite', 'http://__')
    #         curbank['statementfilename'] = com.get('statementfilename', 'неизвестно')
    #         curbank['description'] = com.get('description', '')
    #         listbanks.append(curbank)
    #     return listbanks

    def _get_banks(self):
        banknames =  bankparser.config.BankConfig.get_list_banks()
        listbanks = []
        for bankname in banknames:
            # confbank = configparser.ConfigParser()
            # confbank.read(file, encoding='utf-8')
            #com = confbank['common']
            bankparser.config.get_bank_config(bankname)
            #bankmod = importlib.import_module('bankparser.banks.'+bankname)
            curbank = {}
            curbank['banktitle'] = bankparser.config.bankconfig.bank.banktitle
            curbank['bankname'] = bankparser.config.bankconfig.bank.bankname
            curbank['banksite'] = bankparser.config.bankconfig.bank.banksite
            curbank['statementfile'] = bankparser.config.bankconfig.bank.statementfile
            curbank['description'] = bankparser.config.bankconfig.bank.description
            listbanks.append(curbank)
        return listbanks


    @staticmethod
    def _get_help_banks(banks):
        helpstr = []
        helpstr += "\n"
        for bank in banks:
            bankparam = bank['bankname']
            bankname = bank['banktitle']
            banksite = bank['banksite']
            statementfilename = bank['statementfile']
            description = bank['description']

            #str = "- `{0}`_ {4}. Параметр запуска **{3}**. Файл выписки {2}\n    .. _`{0}`: {1}\n"
            str_bank = "- `{0} <{1}>`_ {4}. Параметр запуска **{3}**. Файл выписки {2}\n"
            helpstr += str_bank.format(bankname, banksite, statementfilename, bankparam, description)

        helpstr += "\n"
        return helpstr

    @staticmethod
    def _get_help_commons(maps):
        """
        Генерация справки по настройкам в common

        :return:
        """
        helpstr = []
        helpstr += "\n"
        helpstr += "Описание настроек секции [common]: \n\n"
        for field in maps:
            helpstr += field['name'] + "\n"
            if field['description'].startswith("Обязательное поле"):
                helpstr += "   {0}\n".format(field['description'])
            else:
                helpstr += "   {0}. По умолчанию: {1}\n".format(field['description'], field['value'])
        helpstr += "\n"

        return helpstr

    @staticmethod
    def _get_help_fields(maps):
        """
        Генерация текста справки по полям

        :return: Текст справки
        """
        typemaps = {'""': 'string', '\'\'': 'string', 'datetime.now()': 'datetime', '0.0': 'float'}
        helpstr = []
        helpstr += "\n"
        helpstr += "Описание полей: \n\n"
        for field in maps:
            helpstr += field['name'] + "\n"
            ftype = typemaps.get(field['value'], field['value'])
            helpstr += "   {0}. Тип поля: {1}\n".format(field['description'], ftype)

        helpstr += "\n"

        return helpstr


if __name__ == '__main__':
    mybuild = MyBuild()
    mybuild.buid()
    # mybuild.copy_script()
