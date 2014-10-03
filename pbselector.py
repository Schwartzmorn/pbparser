import re

class PBTagSelector:
    def __init__(self, iSTag):
        self.tag = iSTag
    def match(self, iPBNode):
        return iPBNode.tag == self.tag
    def toString(self):
        return self.tag

class PBAttributeSelector:
    def __init__(self, iSKey, iSValue):
        prune = False
        self.type = iSKey[-1:]
        if self.type in ['~', '|', '^', '$', '*']:
            prune = True
        if prune:
            self.key = iSKey[0:-1]
        else:
            self.key = iSKey
            self.type = ''
        self.value = iSValue
    def match(self, iPBNode):
        try:
            theval = iPBNode.attributes[self.key]
            if self.type == '':
                return theval == self.value
            elif self.type == '~':
                return re.search("\s" + self.value + "\s", theval) != None
            elif self.type == '^':
                return theval.startswith(self.value)
            elif self.type == '$':
                return theval.endswith(self.value)
            elif self.type == '*':
                return self.value in theval
            elif self.type == '|':
                return theval.startswith(self.value + "-") or theval == self.value
        except:
            return False
    def toString(self):
        return "[" + self.key + self.type + "=" + self.value + "]"

class PBClassSelector:
    def __init__(self, iSString):
        self.selectedClass = iSString
    def match(self, iPBNode):
        return self.selectedClass in iPBNode.classes
    def toString(self):
        return "." + self.selectedClass

class PBSelector:
    def _match(self, iPBNode):
        for aSelector in self._eSelectors:
            if not aSelector.match(iPBNode):
                return False
        return True

    def _searchChildren(iSelector, iPBNode, iResults):
        for aNode in iPBNode.childNodes:
            if aNode.getType() == "element":
                iResults |= iSelector._search(aNode)

    def search(self, iDocument):
        aSet = self._search(iDocument)
        return iDocument.sort(aSet)

    def _search(self, iPBNode):
        res = set()
        if self._match(iPBNode):
            if self._nextSelector:
                PBSelector._searchChildren(self._nextSelector, iPBNode, res)
            else:
                res.add(iPBNode)
                if self._selectorType == "descendant":
                    PBSelector._searchChildren(self, iPBNode, res)
            if self._selectorType == "descendant":
                PBSelector._searchChildren(self, iPBNode, res)
        else:
            if self._selectorType == "descendant":
                PBSelector._searchChildren(self, iPBNode, res)
        return res

    def _initESelectors(self, iSSelectors):
        self._eSelectors = []
        theSelectors = re.findall("\.([^\.\[]+)|\[([^\.\]]+)\]|([^\.\[]+)", iSSelectors)
        for aSelector in theSelectors:
            if aSelector[0] != "":
                self._eSelectors.append(PBClassSelector(aSelector[0]))
            elif aSelector[1] != "":
                key, value = re.split("=", aSelector[1])
                self._eSelectors.append(PBAttributeSelector(key, value))
            elif aSelector[2] != "":
                self._eSelectors.append(PBTagSelector(aSelector[2]))
            else:
                print "### ERROR ### unknown element selector"

    def _initHSelector(self, iSSelector):
        if re.match("\s*>", iSSelector):
            self._selectorType = "child"
        else:
            self._selectorType = "descendant"

    def __init__(self, iLESelectors, iLHSelectors):
        self._initESelectors(iLESelectors[0])
        self._initHSelector(iLHSelectors[0])
        if len(iLESelectors) > 1:
            self._nextSelector = PBSelector(iLESelectors[1:len(iLESelectors)], iLHSelectors[1:len(iLHSelectors)])
        else:
            self._nextSelector = None

    def toString(self):
        aString = ""
        if self._selectorType == "child":
            aString += ">"
        else:
            aString += " "
        for aSel in self._eSelectors:
            aString += aSel.toString()
        if self._nextSelector:
            aString += self._nextSelector.toString()
        return aString

def getPBSelector(iSSelector):
    aSelector = re.search("[^\s].*[^\s]", iSSelector).group(0)
    theESelectors = re.split("[\s>]+", aSelector)
    theHSelectors = re.split("[^\s>]+", aSelector)
    theHSelectors = theHSelectors[0:len(theHSelectors) - 1]
    if len(theESelectors) != len(theHSelectors):
        print "### ERROR ### Element and hierarchy selectors don't match"
        return None
    return PBSelector(theESelectors, theHSelectors)
