import re, traceback
from pbparser import selector
import logging

class DataExtractor:
    def toString(self):
        aString = self.name + ": attribute=" + (self._attr if self._attr else "[data]") + " selector=" + (self._selector.toString() if self._selector else "no selector") + " re=" + (self._re if self._re else "")
        return aString

    def extract(self, iNode):
        data = None
        try:
            res = iNode
            if self._selector:
                theRes = self._selector.search(iNode)
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
            logging.info("### ERROR ### Selector returned no result")
        return (self.name, data)

    def __init__(self, iSName, iSAttr, iSelector = None, iSRe = None):
        self.name = iSName
        self._attr = iSAttr
        if iSelector:
            self._selector = selector.getSelector(iSelector)
        else:
            self._selector = None
        self._re = iSRe

class DataLineExtractor:
    def toString(self):
        aString = ""
        for ex in self._dataExtractors:
            aString += ex.toString() + "\n"
        return aString

    def extractLine(self, iNode):
        res = {}
        for aEx in self._dataExtractors:
            key, value = aEx.extract(iNode)
            res[key] = value
        return res

    def addExtractor(self, iExtractor):
        self._dataExtractors.append(iExtractor)

    def __init__(self):
        self._dataExtractors = []
