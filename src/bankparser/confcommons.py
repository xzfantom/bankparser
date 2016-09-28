# Generate automatically by build.py
# don`t change manually

class ConfCommons:

   delimiter = ";" # Разделитель полей
   startafter = None # Начинать разбор строк со следующей, после стоки начинающейся с указанных символов
   dateformat = "%Y-%m-%d %H:%M:%S" # Формат даты в банковском файле
   encoding = "utf-8" # Кодировка файла
   fields = [] # Имена полей в файле через пробел, нужные поля должны совпадать с именем в описанни доступных полей
   type = "Bank" # Тип выписки: Bank или Invst (обычная или операции с ценными бумагами)
   banksite = None # Ссылка на сайт банка
   bankname = None # Название банка
   statementfilename = '' # Стандартное имя файла выписки
   description = '' # Описание
