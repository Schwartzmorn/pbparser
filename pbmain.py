import urllib2
import sys
import re
import pbparser
import pbselector
import pbextractor

gUrlMain = "https://thepiratebay.se/search/"
gUrlSort = "/0/7/0"

def parsePage(iSUrl):
    try:
        response = urllib2.urlopen(iSUrl)
        aOParser = pbparser.PBParser()
        aOParser.feed(response.read())
        return aOParser
    except urllib2.URLError as e:
        print "Error: " + e.raison
    except:
        print "Unknown error"
    return None

def getPage(iSSearch):
    aStrings = re.split("\s+", iSSearch)
    first = True
    aSPage = ""
    for a in aStrings:
        if a != "":
            if not first:
                aSPage += "%20"
            else:
                first = False
            aSPage += a
    return gUrlMain + aSPage + gUrlSort

def main(args):
    if len(args) < 2:
        print "No search given"
    else:
        aSSearch = ""
        first = True
        aParser = parsePage(getPage(args[1]))
        aSelector = pbselector.getPBSelector(args[2])
        res = aSelector.search(aParser.document)
        print str(len(res)) + " results"
        dataLine = pbextractor.PBDataLineExtractor()
        for node in res:
            line = dataLine.extractLine(node)
            print line

if __name__ == "__main__":
    main(sys.argv)
