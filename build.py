"""
Операции построения, генерации файлов

"""

import csv

class MyBuild:

    rootdir = "src/bankparser/"
    ffields =None
    #statementlinefile = rootdir + "statementline-test.py"


    typemap={'date':'datetime.now()','string':"\"\"",'float':'0.0'}

    fieldsfile = rootdir + "fields.csv"
    fields = list()
    commonfile = rootdir + "commons.csv"
    commons = list()
    #fieldsinfields=["name","type","description","qif_letter"]

    def __init__(self):
        with open(self.fieldsfile,"r",encoding="utf-8") as f:
            fields = csv.DictReader(f, delimiter=";")
            self.fields=list(fields)
        with open(self.commonfile,"r",encoding="utf-8") as f:
            self.commons = list(csv.DictReader(f, delimiter="|"))




    def gen_files(self):
        #self.gen_fields_file('QIFLine')
        #self.gen_fields_file('StatementLine')
        self.write_files()
        self.readme_replace()

    def write_files(self):
        className='StatementLine'
        str = self.get_statement_str(className)
        self.write_file(className, str)
        className = 'QIFLine'
        str = self.get_statement_str(className)
        self.write_file(className, str)
        className = "ConfCommons"
        str = self.get_commons_str(className)
        self.write_file(className, str)

    def readme_replace(self):
        with open('readme.rst','r',encoding='utf-8') as f:
            filelines = f.readlines()
        newlines=[]
        readline=True
        for line in filelines:
            if line == ".. fields_finish\n" or line == ".. commons_finish\n":
                readline = True
            if readline:
                newlines += line
            if line == ".. fields_start\n":
                readline = False
                newlines+=self.get_help_fields()
            if line == ".. commons_start\n":
                readline = False
                newlines += self.get_help_commons()
                #insert help

        with open('readme.rst','w',encoding='utf-8') as f:
            f.writelines(newlines)


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
            str += "   |{0}\n".format(field['description'])
            str += "   |По умолчанию: {0}\n\n".format(field['default'])

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
            str += "   {0}\n".format(field['description'])
            str += "   Тип поля: {0}\n\n".format(field['type'])

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
        filename = self.rootdir + className.lower() + ".py"
        stline = open(filename, "w", encoding='utf-8')
        stline.write("# Generate automatically from build.py\n")
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
