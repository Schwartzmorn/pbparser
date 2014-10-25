import re, urllib2, traceback, json
from pbparser import parser, selector
from pbadmin import admin, model
from pbproxy import proxy
import webapp2
import logging

def parsePage(iSUrl):
    try:
        response = urllib2.urlopen(iSUrl)
        aOParser = parser.Parser()
        aOParser.feed(response.read())
        return aOParser
    except urllib2.URLError as e:
        logging.info("Error: " + e.raison)
    except:
        logging.info(traceback.format_exc())
    return None

class PBMain (webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        url = re.search("/search/.*", self.request.url).group(0)
        url = url[8:len(url)]
        modelName = re.search("^[^/]*", url).group(0)
        search = url[len(modelName) + 1:len(url)]
        theModel = model.getPBModel(modelName)
        theDataLine = model.getDataLineExtractor(modelName)
        try:
            theUrl = theModel.url + search + theModel.filt
            aParser = parsePage(theUrl)
            logging.info(theModel.selector)
            aSelector = selector.getSelector(theModel.selector)
            res = aSelector.search(aParser.document)
            theRes = []
            for node in res:
                theRes.append(theDataLine.extractLine(node))
            self.response.write(json.dumps(theRes))
        except:
            self.response.write("error\n")
            print "error when writing page: "
            self.response.write(traceback.format_exc())

application = webapp2.WSGIApplication([
    ('/search/.*', PBMain),
    ('/admin', admin.PBAdmin),
    ('/proxy', proxy.PBProxy),
], debug=True)

