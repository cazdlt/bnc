from bnc import bnc,ElementoBNC
import requests

def test_search():
    
    
    biblio=bnc()
    res=biblio.search("bullerengue")
    assert len(res)==12

    res=biblio.search("fqwe9fwqhefwef")
    assert len(res)==0

def test_elemento():
    
    elem=ElementoBNC("/client/es_ES/bd/search/detailnonmodal/ent:$002f$002fSD_ASSET$002f0$002fSD_ASSET:71077/ada?qu=bullerengue")
    assert elem.titulo=="El bullerengue Socorro Yépes"
    assert elem.url_contenido=="/client/es_ES/search/asset/71077/0"

def test_elemento_fullurl():
    
    url="https://catalogoenlinea.bibliotecanacional.gov.co/client/es_ES/bd/search/detailnonmodal/ent:$002f$002fSD_ASSET$002f0$002fSD_ASSET:58056/ada?qu=san+jacinto"
    elem=ElementoBNC(url)
    assert elem.titulo=="[Gaitas corridas y porros] [recurso electróncio] / [Gaiteros de San Jacinto]"
    assert elem.url_contenido=="/client/es_ES/search/asset/58056/0"

def test_download():
    
    url="https://catalogoenlinea.bibliotecanacional.gov.co/client/es_ES/bd/search/detailnonmodal/ent:$002f$002fSD_ASSET$002f0$002fSD_ASSET:58059/ada?qu=san+jacinto&rw=12&isd=true"
    elem=ElementoBNC(url)
    res=elem.downloadContent()
    assert len(res)==10027008