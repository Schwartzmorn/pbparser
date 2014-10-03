import webapp2
import traceback
import re
import pbmodel

class PBAdmin(webapp2.RequestHandler):
    def _refillForm(self, iHTML):
        iHTML = iHTML.replace("&$modelName", self.request.get("modelName", ""))
        iHTML = iHTML.replace("&$url", self.request.get("url", ""))
        iHTML = iHTML.replace("&$filt", self.request.get("filt", ""))
        iHTML = iHTML.replace("&$selector", self.request.get("selector", ""))
        iHTML = iHTML.replace("&$name", self.request.get("name", ""))
        iHTML = iHTML.replace("&$exSelector", self.request.get("exSelector", ""))
        iHTML = iHTML.replace("&$attribute", self.request.get("attribute", ""))
        iHTML = iHTML.replace("&$regex", self.request.get("regex", ""))
        return iHTML

    def _modelAction(self, iHTML):
        action = self.request.get("actionModel")
        if action == "Put":
            if self.request.get("modelName") and self.request.get("modelName") != "":
                try:
                    pbmodel.setPBModel(self.request.get("modelName"), self.request.get("url"), self.request.get("filt"), self.request.get("selector"))
                except:
                    iHTML = iHTML.replace("&$res", "Problem occurred when saving the model" + str(self.request.get("modelName", "none")) + "\n" + traceback.format_exc())
            else:
                iHTML = iHTML.replace("&$res", "Model has no name!")
            iHTML = self._refillForm(iHTML)
        elif action == "Get":
            try:
                aModel = pbmodel.getPBModel(self.request.get("modelName"))
                aString = str(aModel.name) + ": url:" + str(aModel.url) + " filter: " + str(aModel.filt) + " selector: " + str(aModel.selector) + "\n"
                aDataLine = pbmodel.getPBDataLineExtractor(self.request.get("modelName"))
                aString += aDataLine.toString()
                if aModel.name:
                    iHTML = iHTML.replace("&$modelName", aModel.name)
                if aModel.url:
                    iHTML = iHTML.replace("&$modelUrl", aModel.url)
                if aModel.filt:
                    iHTML = iHTML.replace("&$modelFilt", aModel.filt)
                if aModel.selector:
                    iHTML = iHTML.replace("&$modelSelector", aModel.selector)
                iHTML = iHTML.replace("&$res", aString)
            except:
                iHTML = iHTML.replace("&$res", "Problem occurred when retrieving the model " + str(self.request.get("modelName", "none")) + "\n" + traceback.format_exc())
        elif action == "Delete":
            try:
                pbmodel.removePBModel(self.request.get("modelName"))
                iHTML = iHTML.replace("&$res", "Model " + self.request.get("modelName", "") + "was removed")
            except:
                iHTML = iHTML.replace("&$res", "Problem occurred when removing the model " + str(self.request.get("modelName", "none")) + "\n" + traceback.format_exc())
            iHTML = self._refillForm(iHTML)
        return iHTML

    def _extractorAction(self, iHTML):
        action = self.request.get("actionExtractor")
        if action == "Put":
            if self.request.get("modelName") and self.request.get("modelName") != "" and self.request.get("name") and self.request.get("name") != "":
                try:
                    pbmodel.setPBModelExtractor(self.request.get("modelName"), self.request.get("name"), self.request.get("exSelector"), self.request.get("attribute"), self.request.get("regex"))
                except:
                    iHTML = iHTML.replace("&$res", "Problem occurred when saving the extractor" + str(self.request.get("modelName", "none")) + " " + str(self.request.get("name", "none")) + "\n" + traceback.format_exc())
            iHTML = self._refillForm(iHTML)
        elif action == "Get":
            if self.request.get("modelName") and self.request.get("modelName") != "" and self.request.get("name") and self.request.get("name") != "":
                try:
                    aExModel = pbmodel.getPBModelExtractor(self.request.get("modelName"), self.request.get("name"))
                    aString = self.request.get("modelName") + "." + aExModel.name + " " + str(aExModel.selector) + " " + str(aExModel.attr)
                    iHTML = iHTML.replace("&$res", aString)
                    iHTML = iHTML.replace("&$modelName", self.request.get("modelName"))
                    iHTML = iHTML.replace("&$name", aExModel.name)
                    iHTML = iHTML.replace("&$exSelector", aExModel.selector)
                    iHTML = iHTML.replace("&$attribute", aExModel.attr)
                    iHTML = iHTML.replace("&$regex", aExModel.regex)
                except:
                    iHTML = iHTML.replace("&$res", "Problem occurred when retrieving the extractor" + str(self.request.get("modelName", "none")) + " " + str(self.request.get("name", "none")) + "\n" + traceback.format_exc())
            
        elif action == "Delete":
            try:
                pbmodel.getPBModelExtractor(self.request.get("modelName"), self.request.get("name"))
                iHTML = iHTML.replace("&$res", "Model " + self.request.get("modelName", "") + "." + self.request.get("name", "") + "was removed")
            except:
                iHTML = iHTML.replace("&$res", "Problem occurred when removing the model " + str(self.request.get("modelName", "none")) + " " + str(self.request.get("name", "none")) + "\n" + traceback.format_exc())
            iHTML = self._refillForm(iHTML)
        return iHTML

    def post(self):
        f = open("admin.html")
        theHTML = str(f.read())
        if self.request.get("actionModel"):
            theHTML = self._modelAction(theHTML)
        elif self.request.get("actionExtractor"):
            theHTML = self._extractorAction(theHTML)
        theHTML = re.sub("\&\$[a-zA-Z0-9]+", "", theHTML)
        self.response.headers["Content-Type"] = "text/html"
        self.response.write(theHTML)

    def get(self):
        f = open("admin.html", "r")
        theHTML = f.read()
        self.response.headers["Content-Type"] = "text/html"
        theHTML = re.sub("\&\$[a-zA-Z0-9]+", "", theHTML)
        self.response.write(theHTML)
