"""
Операции построения, генерации файлов

"""

import csv
import glob
import shutil
import os.path
from bankparser.config import *

class MyBuild:


    ffields =None
    pubdir = "c:/temp/andrey/bankparser/"

    typemap={'date':'datetime.now()','string':"\"\"",'float':'0.0'}

    fieldsfile = os.path.join(SRCDIR, "fields.csv")
    fields = list()
    commonfile = os.path.join(SRCDIR, "commons.csv")
    commons = list()
    #fieldsinfields=["name","type","description","qif_letter"]

    def __init__(self):
        with open(self.fieldsfile,"r",encoding="utf-8") as f:
            self.fields.append(FIELD_AMOUNT)
            self.fields.append(FIELD_AMOUNTSIGN)
            csvfields = list(csv.DictReader(f, delimiter=";"))
            for field in csvfields:
                self.fields.append(field) #=list(fields)


        with open(self.commonfile,"r",encoding="utf-8") as f:
            self.commons = list(csv.DictReader(f, delimiter="|"))




    def gen_files(self):
        #self.gen_fields_file('QIFLine')
        #self.gen_fields_file('StatementLine')
        self.write_files()
        print("readme generation...")
        self.readme_replace("commons")
        self.readme_replace("fields")
        self.readme_replace("banks")
        self.copy_script()

    def write_files(self):

        className='StatementLine'
        print("{} generation...".format(className))
        str = self.get_statement_str(className)
        self.write_file(className, str)
        className = 'QIFLine'
        print("{} generation...".format(className))
        str = self.get_statement_str(className)
        self.write_file(className, str)
        className = "ConfCommons"
        print("{} generation...".format(className))
        str = self.get_commons_str(className)
        self.write_file(className, str)

    def copy_script(self):


        # libs
        dest_dir = self.pubdir + "bankparser"
        mask=os.path.join(SRCDIR, "*.py")
        for file in glob.glob(mask):
            print("copyng file {}".format(file))
            shutil.copy(file, dest_dir)
        # rootfile
        rootfile=os.path.join(SRCDIR, "bankparsercli.py")
        dest_dir = self.pubdir
        print("copyng file {}".format(rootfile))
        shutil.copy(rootfile, dest_dir)
        # ini files
        mask = os.path.join(SRCDIR, "*.ini")
        for file in glob.glob(mask):
            print("copyng file {}".format(file))
            shutil.copy(file, dest_dir)
        # generate bat vtb24
        self.save_bat("statement.csv","vtb24")
        self.save_bat("report.txt","adshares")


    def save_bat(self,filetomove,bank):
        downloadsfolder= "c:\\Users\\Пользователь\\Downloads\\" + filetomove
        batstr = []
        destsl = self.pubdir.replace('/', '\\') + filetomove
        batstr += "move {0} {1}\n".format(downloadsfolder,destsl)
        batstr += "python.exe bankparsercli.py {0} {1}\n".format(bank,filetomove)
        batstr += "pause\n"
        with open(self.pubdir + bank +".bat", "w", encoding="cp866") as f:
            f.writelines(batstr)


    def readme_replace(self,blockname):
        startblock=".. {}_start\n".format(blockname)
        endblock=".. {}_finish\n".format(blockname)

        with open('readme.rst','r',encoding='utf-8') as f:
            filelines = f.readlines()
        newlines=[]
        readline=True
        for line in filelines:
            if line == endblock:
                readline = True
            if readline:
                newlines += line
            if line == startblock:
                readline = False
                newlines+=self.get_help(blockname)


        with open('readme.rst','w',encoding='utf-8') as f:
            f.writelines(newlines)


    def get_help(self,blockname):
        if blockname == "commons":
            return self.get_help_commons()
        elif blockname == "fields":
            return self.get_help_fields()
        elif blockname == "banks":
            return self.get_help_banks()

    def get_help_banks(self):
        # Получить список ini файлов
        listbanks=bankconfig.get_list_banks()
        str = []
        str += "\n"
        for bank in listbanks:
            confb=getBankConfig(bank)
            bankname=confb.commons.bankname
            banksite=confb.commons.banksite
            #bankini=os.path.basename(confb.inifile)
            #str += " * {0} {1} ({2})\n".format(bankname,banksite,bankini)
            str += "- `{0}`_ {4}. Параметр запуска **{3}**. Файл выписки {2}\n    .. _`{0}`: {1}\n".format(bankname, banksite,
                                                                                            confb.commons.statementfilename,
                                                                                            bank,
                                                                                            confb.commons.description)
            # if confb.commons.description:
            #     str += "* `{0}`_ ({4}). **{3}**. Файл выписки {2}\n    .. _`{0}`: {1}\n".format(bankname, banksite,confb.commons.statementfilename, bank,confb.commons.description)
            # else:
            #     str += "* `{0}`_. **{3}**. Файл выписки {2}\n    .. _`{0}`: {1}\n".format(bankname,banksite,confb.commons.statementfilename,bank)

        str += "\n"
        return  str

    def get_help_commons(self):
        """
        Генерация справки по настройкам в common

        :return:
        """
        str=[]
        str+="\n"
        str+="Описание настроек секции [common]: \n\n"
        for field in self.commons:
            str+=field['name']+"\n"
            if field['description'].startswith("Обязательное поле"):
                str += "   {0}\n".format(field['description'])
            else:
                str += "   {0}. По умолчанию: {1}\n".format(field['description'],field['default'])
            #str += "   По умолчанию: {0}\n\n".format(field['default'])
        str += "\n"

        return str


    def get_help_fields(self):
        """
        Генерация справки по полям

        :return:
        """
        str=[]
        str+="\n"
        str+="Описание полей: \n\n"
        for field in self.fields:
            str+=field['name']+"\n"

            str += "   {0}. Тип поля: {1}\n".format(field['description'],field['type'])
            #str += "   Тип поля: {0}\n\n".format(field['type'])

        str += "\n"

        return str

    def get_commons_str(self,className):
        str=[]
        #f.write("from datetime import datetime\n\n\n")
        str+="class {}:\n\n".format(className)
        for field in self.commons:

             str += "   {0} = {1} # {2}\n".format(field['name'], field['default'], field['description'])
        return str

    def write_file(self,className,lines):
        # Генерация файлов
        filename = os.path.join(SRCDIR,className.lower() + ".py")
        stline = open(filename, "w", encoding='utf-8')
        stline.write("# Generate automatically by build.py\n")
        stline.write("# don`t change manually\n\n")
        stline.writelines(lines)
        stline.close()






    def get_statement_str(self,className):
        str = []
        str += "from datetime import datetime\n\n\n"
        str += "class {}:\n\n".format(className)
        for field in self.fields:
            typestr = self.typemap.get(field['type'], field['type'])
            if className.lower() == 'statementline' or field['qif_letter'] != "":
                str += "   {0} = {1} # {2}\n".format(field['name'], typestr, field['description'])

        if className.lower() == 'qifline':
            #stline.write('   qifletters = {')
            #self.ffields.seek(0)
            qstr = ""
            for field in self.fields:

                if field['qif_letter'] != "":
                    if qstr != "":
                        qstr+=", "

                    qstr+= "'{0}': '{1}'".format(field['name'], field['qif_letter'])
            qstr+="}"
            qstr='\n\nqifletters = {' + qstr
            str += qstr
        return str





mybuild = MyBuild()
mybuild.gen_files()
mybuild.get_help_banks()
