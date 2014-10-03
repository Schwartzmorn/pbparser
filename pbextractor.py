import re
import pbselector
import traceback

class PBDataExtractor:
    def toString(self):
        aString = self.name + ": attribute=" + (self._attr if self._attr else "[data]") + " selector=" + (self._selector.toString() if self._selector else "no selector") + " re=" + (self._re if self._re else "")
        return aString

    def extract(self, iPBNode):
        data = None
        try:
            res = iPBNode
            if self._selector:
                theRes = self._selector.search(iPBNode)
                # the search returns a set, we just want one element
                if len(theRes) > 0:
                    res = theRes[0]
            if not self._attr:
                for aNode in res.childNodes:
                    if aNode.getType() == "data":
                        data = aNode.data
                        break
            else:
                data = res.attributes[self._attr]
            if self._re:
                data = re.search(self._re, data).group(0)
        except:
            print "### ERROR ### Selector returned no result"
            print traceback.format_exc()
        return (self.name, data)


    def __init__(self, iSName, iSAttr, iPBSelector = None, iSRe = None):
        self.name = iSName
        self._attr = iSAttr
        if iPBSelector:
            self._selector = pbselector.getPBSelector(iPBSelector)
        else:
            self._selector = None
        self._re = iSRe

class PBDataLineExtractor:
    def toString(self):
        aString = ""
        for ex in self._dataExtractors:
            aString += ex.toString() + "\n"
        return aString

    def extractLine(self, iPBNode):
        res = []
        for aEx in self._dataExtractors:
            res.append(aEx.extract(iPBNode))
        return res

    def addExtractor(self, iExtractor):
        self._dataExtractors.append(iExtractor)

    def __init__(self):
        self._dataExtractors = []
