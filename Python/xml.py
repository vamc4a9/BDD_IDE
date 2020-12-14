from io import StringIO
from lxml import etree

class cXml:
    def __init__(self,xmlPath):
        self.xmlPath = xmlPath
        self.sXMLString = self.ReadFile()

    def ReadNode(self, sXPath):
        tree = etree.parse(self.xmlPath)
        return tree.xpath(sXPath)

    def UpdateNode(self, sXPath, sValue):
        tree = etree.parse(self.xmlPath)
        item = tree.xpath(sXPath)[0]
        item.text = sValue

    def insertNode(self, sParent, statement, parameters, xtrnlData, instructions):
        tree = etree.parse(self.xmlPath)
        parent = tree.xpath(sParent)[0]
        node_element = etree.Element("StepDefinition")
        node_element.set("Statement", statement)
        node_element.set("Parameters", parameters)
        node_element.set("ExternalData", xtrnlData)
        node_element.set("Instructions", instructions)
        parent.insert(1, node_element)

        obj_xml = etree.tostring(tree,
                                 pretty_print=True,
                                 xml_declaration=True)

        try:
            with open(self.xmlPath, "wb") as xml_writer:
                xml_writer.write(obj_xml)
        except IOError:
            pass

    def ReadFile(self):
        file = open(self.xmlPath, "r")
        Lines = file.readlines()
        file.close()
        sNewLine = ""
        return sNewLine.join(Lines)
