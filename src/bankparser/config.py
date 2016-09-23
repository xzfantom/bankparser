import configparser

configfile='config.ini'

FIELDS={'encoding': 'utf-8',
        'dateformat': '%Y-%m-%d %H:%M:%S'

        }

FIELD_ENCODING='encoding'
DEFAULT_ENCODING='utf-8'

DEFAULT_CURRENCY = 'RUB'

FIELD_DATEFORMAT='dateformat'
DEFAULT_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

FIELD_STARTAFTER = 'startafter'

FIELD_DELIMITER = 'delimiter'
DEFAULT_DELIMITER = ';'

settings = configparser.ConfigParser()
#settings=\
settings.read(configfile,encoding='utf-8')


#with open(configfile, "r") as f:
    #settings = yaml.load(f)
#    settings = config.read(f, encoding='utf-8')
