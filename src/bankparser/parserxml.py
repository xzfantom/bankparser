import xml.etree.cElementTree as ElTree
import bankparser.parser


class ParserXML(bankparser.parser.StatementParser):

    def _split_records(self):

        tree = ElTree.fromstring(self.content)

        xpath = self.confbank.bank.xpath_tolines
        field_maps = self.confbank.bank.fields # = {'xml tag name': 'line field name', ... }
        keys = field_maps.keys()
        # convert xml to array of lines
        # only tag text read!
        lines = []
        for detail in tree.findall(xpath):
            line = {}
            for key in keys:
                value = detail.find(key).text
                newkey = field_maps[key]
                line[newkey] = value
            lines.append(line)

        return lines



