import csv
import bankparser.parser

class ParserCSV(bankparser.parser.StatementParser):

    def _split_records(self):

        fields = self.confbank.bank.fields
        bdelimiter = self.confbank.bank.delimiter

        fin = self.content.split('\n')

        startafter = self.confbank.bank.startafter
        if startafter:
            flag = 0
            strfile = []
            for line in fin:
                if flag:
                    # print(line)
                    if line not in ['\n', '\r\n']:
                        strfile.append(line)
                if line.startswith(startafter):
                    flag = 1
            return csv.DictReader(strfile, delimiter=bdelimiter, fieldnames=fields)
        else:
            return csv.DictReader(fin, delimiter=bdelimiter, fieldnames=fields)



