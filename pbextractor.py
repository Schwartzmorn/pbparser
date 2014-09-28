import pbselector
import re

class PBDataExtractor:
    def extract(self, iPBNode):
        data = None
        try:
            res = None
            if self._selector:
                theRes = self._selector.search(iPBNode)
                # the search returns a set, we just want one element
                for aRes in theRes:
                    res = aRes
                    break
            else:
                res = iPBNode
            if not self._attr:
                for aNode in res.childNodes:
                    if aNode.getType() == "data":
                        data = aNode.data
                        break
            else:
                data = iPBNode.attributes[self._attr]
            if self._re:
                data = re.search(self._re, data).group(0)
        except:
            print "### ERROR ### Selector returned no result"
        return (self.name, data)


    def __init__(self, iSName, iSAttr, iPBSelector = None, iSRe = None):
        self.name = iSName
        self._attr = iSAttr
        self._selector = iPBSelector
        self._re = iSRe

class PBDataLineExtractor:
    def extractLine(self, iPBNode):
        res = []
        for aEx in self._dataExtractors:
            res.append(aEx.extract(iPBNode))
        return res

    def __init__(self):
        self._dataExtractors = []
        self._dataExtractors.append(PBDataExtractor("title", None, pbselector.getPBSelector(".detLink"))) 
