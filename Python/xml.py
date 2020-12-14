from io import StringIO
from lxml import etree

class cXml:
    def __init__(self,xmlPath):
        self.xmlPath = xmlPath
        self.sXMLString = self.ReadFile()

    def ReadNode(self, sXPath):
        tree = etree.parse(self.xmlPath)
        return tree.xpath(sXPath)

    def ReadFile(self):
        file = open(self.xmlPath, "r")
        Lines = file.readlines()
        file.close()
        sNewLine = ""
        return sNewLine.join(Lines)
