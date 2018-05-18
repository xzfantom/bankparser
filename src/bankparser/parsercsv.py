import csv
import bankparser.parser

class ParserCSV(bankparser.parser.StatementParser):
    """
    Class for reading csv files
    """

    def __init__(self):
        super().__init__()
        self.delimiter = ";"
        self.startafter = str
        self.stopafter = str

    def _split_records(self):

        fields = self.fields
        bdelimiter = self.delimiter

        fin = self.content.split('\n')

        strfile = self.get_transaction_table(fin)
        return csv.DictReader(strfile, delimiter=bdelimiter, fieldnames=fields)

    def get_transaction_table(self, lines):
        startafter = self.startafter
        stopafter = self.stopafter

        if startafter:
            flag = 0
            strfile = []
            for line in lines:
                if stopafter and line.startswith(stopafter):
                    break
                if flag:
                    if line not in ['\n', '\r\n']:
                        strfile.append(line)
                if line.startswith(startafter):
                    flag = 1
        else:
            return lines
        return strfile
