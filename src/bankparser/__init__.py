"""
bankparser

Convert banks statements to qif format

Original code:
https://github.com/partizand/bankparser

This fork:
https://github.com/xzfantom/bankparser

Bankparser works with Python 3

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
from bankparser.parsercsv import ParserCSV
from bankparser.parserxml import ParserXML
import bankparser.config

__version__ = "0.2.2"
__author__ = "partizand, xzfantom"
__license__ = "GPL3"
