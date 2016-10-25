

class StdBank:
   """
   Стандартные настройки для банка
   """
   # start_fields description
   delimiter = ";"  # Разделитель полей
   startafter = None  # Начинать разбор строк со следующей, после стоки начинающейся с указанных символов
   dateformat = "%Y-%m-%d %H:%M:%S"  # Формат даты в банковском файле
   encoding = "utf-8"  # Кодировка файла
   fields = []  # Имена полей в файле, нужные поля должны совпадать с именем в описанни доступных полей
   type = "Bank"  # Тип выписки: Bank или Invst (обычная или операции с ценными бумагами)
   banksite = None # Ссылка на сайт банка
   banktitle = ''  # Название банка
   statementfile = ''  # Стандартное имя файла выписки
   description = ''  # Описание
   long_descr = '' # Длинное описание
   vars = {} # Пременные нужные для конкретного банка. Переопределяются в ini
   # end_fields


   def after_row_parse(self, statementline, rawline):
      pass

   def after_config_readed(self):
      pass

   def __repr__(self):
        return '<bank name={0}>'.format(self.bankname)
