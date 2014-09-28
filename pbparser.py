from HTMLParser import HTMLParser
import re

class PBData:
    def getType(self):
        return "data"
    def toText(self, iILevel = 0):
        aString = ""
        for i in range (0, iILevel):
            aString += "  "
        aString += self.data
        print aString
    def __init__(self, iSData, iOParent):
        self.data = iSData
        self.parentNode = iOParent

class PBNode:
    def addNode(self, iONode):
        self.childNodes.append(iONode)
    def getType(self):
        return "element"
    def toText(self, iILevel = 0):
        aString = ""
        for i in range (0, iILevel):
            aString += "  "
        aString += self.tag + ": "
        for key, value in self.attributes.iteritems():
            aString += key + "=" + value + " "
        print aString
        for aNode in self.childNodes:
            try:
                aNode.toText(iILevel + 1)
            except:
                print "### ERROR ###"
    def __init__(self, iSTag, iDAttributes, iOParent):
        self.childNodes = []
        self.attributes = {}
        self.classes = set()
        for key, value in iDAttributes:
            self.attributes[key] = value
            if key == "class":
                aLClasses = re.split("\s+", value)
                self.classes = set(aLClasses)
                if "" in self.classes:
                    self.classes.remove("")
        self.tag = iSTag
        self.parentNode = iOParent

class PBParser(HTMLParser):
    voidElements = set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'menuitem', 'meta', 'param', 'source', 'track', 'wbr'])
    def handle_starttag(self, iSTag, iDAttrs):
        aNode = PBNode(iSTag, iDAttrs, self._curNode)
        self._curNode.addNode(aNode)
        if iSTag not in PBParser.voidElements:
            self._curNode = aNode
    def handle_endtag(self, iSTag):
        if self._curNode == self.document:
            print "### ERROR ### Encountered unexpected end of tag " + iSTag
        elif self._curNode.tag != iSTag and iSTag not in PBParser.voidElements:
            print "### ERROR ### Encountered unexpected end of tag " + iSTag + ", expected " + self._curNode.tag
        else:
            if iSTag not in PBParser.voidElements:
                self._curNode = self._curNode.parentNode
    def handle_data(self, iSData):
        if re.match("^\s*$", iSData) == None:
            aNode = PBData(iSData, self._curNode)
            if self._curNode == None:
                self.pbTree.append(aNode)
            else:
                self._curNode.addNode(aNode)  
    def __init__(self):
        HTMLParser.__init__(self)
        self.document = PBNode("document", {}, None)
        self._curNode = self.document
