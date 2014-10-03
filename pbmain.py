import urllib2
import sys
import re
import pbparser
import pbmodel
import pbadmin
import pbselector
import webapp2
import traceback
import json

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

class PBPMain (webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        url = re.search("/search/.*", self.request.url).group(0)
        url = url[8:len(url)]
        modelName = re.search("^[^/]*", url).group(0)
        search = url[len(modelName) + 1:len(url)]
        theModel = pbmodel.getPBModel(modelName)
        theDataLine = pbmodel.getPBDataLineExtractor(modelName)
        try:
            theUrl = theModel.url + search + theModel.filt
            aParser = parsePage(theUrl)
            aSelector = pbselector.getPBSelector(theModel.selector)
            res = aSelector.search(aParser.document)
            theRes = []
            for node in res:
                theRes.append(theDataLine.extractLine(node))
            self.response.write(json.dumps(theRes))
        except:
            self.response.write("error")
            print "error when writing page: "
            print traceback.format_exc()

application = webapp2.WSGIApplication([
    ('/search/.*', PBPMain),
    ('/admin', pbadmin.PBAdmin),
], debug=True)

