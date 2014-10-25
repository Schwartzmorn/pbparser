from google.appengine.ext import ndb
from pbparser import selector, extractor

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
    aQuery = PBModelExtractor.query(PBModelExtractor.modelName == iSName)
    res = aQuery.fetch()
    for line in res:
        line.key.delete()
    theModel = getPBModel(iSName)
    if theModel:
        theModel.key.delete()

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
        aModel.key.delete()

def getDataLineExtractor(iSModelName):
    res = extractor.DataLineExtractor()
    query = PBModelExtractor.query(PBModelExtractor.modelName == iSModelName)
    theExtractors = query.fetch()
    for anEx in theExtractors:
        aRe = (None if anEx.re == '' else anEx.re)
        anAttr = (None if anEx.attr == '' else anEx.attr)
        aSel = (None if anEx.selector == '' else anEx.selector)
        res.addExtractor(extractor.DataExtractor(anEx.name, anAttr, aSel, aRe))
    return res
