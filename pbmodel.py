from google.appengine.ext import ndb
import pbselector
import pbextractor

class PBModel(ndb.Model):
    name = ndb.StringProperty()
    url = ndb.StringProperty(indexed=False)
    filt = ndb.StringProperty(indexed=False)
    selector = ndb.StringProperty(indexed=False)

class PBModelExtractor(ndb.Model):
    modelName = ndb.StringProperty()
    name = ndb.StringProperty()
    selector = ndb.StringProperty(indexed=False)
    attr = ndb.StringProperty(indexed=False)
    re = ndb.StringProperty(indexed=False)

def getPBModel(iSName):
    aPBModelQuery = PBModel.query(PBModel.name == iSName)
    return aPBModelQuery.get()

def setPBModel(iSName, iSUrl, iSFilt, iSSelector):
    aPBModel = getPBModel(iSName)
    if not aPBModel:
        aPBModel = PBModel()
    aPBModel.name = iSName
    aPBModel.url = iSUrl
    aPBModel.filt = iSFilt
    aPBModel.selector = iSSelector
    aPBModel.put()

def removePBModel(iSName):
    aQuery = PBModelExtractor.query(PBModelExtractor.modelName == iSModelName)
    res = aQuery.fetch()
    for line in res:
        res.delete()
    theModel = getPBModel(iSName)
    if theModel:
        theModel.delete()

def getPBModelExtractor(iSModelName, iSName):
    aPBModelExtractorQuery = PBModelExtractor.query(PBModelExtractor.modelName == iSModelName,
                                                    PBModelExtractor.name == iSName)
    return aPBModelExtractorQuery.get()

def setPBModelExtractor(iSModelName, iSName, iSSelector, iSAttr, isRE):
    aModel = getPBModelExtractor(iSModelName, iSName)
    if not aModel:
        aModel = PBModelExtractor()
    aModel.modelName = iSModelName
    aModel.name = iSName
    aModel.selector = iSSelector
    aModel.attr = iSAttr
    aModel.re = isRE
    aModel.put()

def removePBModelExtractor(iSModelName, iSName):
    aModel = getPBModelExtractor(iSModelName, iSName)
    if aModel:
        aModel.delete()

def getPBDataLineExtractor(iSModelName):
    res = pbextractor.PBDataLineExtractor()
    query = PBModelExtractor.query(PBModelExtractor.modelName == iSModelName)
    theExtractors = query.fetch()
    for anEx in theExtractors:
        aRe = (None if anEx.re == '' else anEx.re)
        anAttr = (None if anEx.attr == '' else anEx.attr)
        aSel = (None if anEx.selector == '' else anEx.selector)
        res.addExtractor(pbextractor.PBDataExtractor(anEx.name, anAttr, aSel, aRe))
    return res
