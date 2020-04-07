#leer audio quicktime del catálogo de la biblioteca nacional
import requests
from bs4 import BeautifulSoup
import re

class ElementoBNC():
    """
       Carga info del elemento a partir de su url relativa
       e.g.
       Para cargar:
       https://catalogoenlinea.bibliotecanacional.gov.co/client/es_ES/bd/search/detailnonmodal/ent:$002f$002fSD_ASSET$002f0$002fSD_ASSET:58063/ada?qu=bullerengue
    
        llamar: 
            url="https://catalogoenlinea.bibliotecanacional.gov.co/client/es_ES/bd/search/detailnonmodal/ent:$002f$002fSD_ASSET$002f0$002fSD_ASSET:58063/ada?qu=bullerengue"
            elemento=ElementoBNC(url)    
    """

    baseurl="https://catalogoenlinea.bibliotecanacional.gov.co"
    
    def __init__(self, url, sesion=None):
        
        if not sesion:
            sesion=requests.Session()
        self.s=sesion

        if "https" in url:
            r=sesion.get(url)
        else:
            r=sesion.get(self.baseurl+url)            

        soup=BeautifulSoup(r.content,"lxml")
        biblio=soup.find(class_="detail_biblio")

        self.url=url
        self.titulo=soup.find(class_="displayElementText TITLE").text

        autor=soup.find(class_="displayElementText AUTHOR")
        if autor:
            self.autor=autor.text
        else:
            self.autor=""
            

        fecha=soup.find(class_="displayElementText PERIOD_DATE")
        if fecha:
            self.fecha=fecha.text
        else:
            self.fecha=""

        self.tema=soup.find(class_="displayElementText SUBJECT").text
        self.formato=soup.find(class_="displayElementText DIGITAL_FORMAT").text
        self.url_contenido= soup.find("a",title="Enlace externo al activo")["href"].partition(self.baseurl)[-1]
        self.descripcion= soup.find(class_="displayElementLabel DESCRIPTION DESCRIPTION_label").next_sibling.next_sibling.text

    def __str__(self):
        return f"{self.titulo} - {self.autor} ({self.fecha})"

    def downloadContent(self, output_filename=None):
        """
        Descarga el archivo de audio encontrado en una página de contenido QuickTime de la Biblioteca Nacional de Colombia (e.g. https://catalogoenlinea.bibliotecanacional.gov.co/client/es_ES/search/stream/58063/false/0)
        Si {output_filename} existe, lo guarda en el workspace como {output_filename}.extension_original
        Lo devuelve al contexto donde fue llamada la función
        """
        r=self.s.get(self.baseurl+self.url_contenido)
        soup=BeautifulSoup(r.content,'lxml')
        scripts=soup.findAll("script",src=None)
        assert len(scripts)==1, "Más de un o ningún archivo de contenido encontrado"

        script=scripts[0]
        src=re.findall("[^,()]+",script.text)[1].split("'")[1]
        url=self.baseurl+src
        print(f"Descargando archivo de audio de {url}")
        r2=self.s.get(url)

        if output_filename:
            headers=r2.headers
            original_name=headers["Content-Disposition"].partition("''")[-1]
            extension=original_name.split(".")[-1]

            salida=f"{output_filename}.{extension}"
            print(f"Guardando archivo {original_name} como {salida}")
            open(salida,"wb").write(r2.content)

        #Devuelve archivo para trabajar con él
        return r2.content

class bnc():
    """
       Buscar, descargar del catálogo de la Biblioteca Nacional de Colombia
       https://catalogoenlinea.bibliotecanacional.gov.co/client/es_ES/bd/?
    """
    baseurl="https://catalogoenlinea.bibliotecanacional.gov.co"

    def __init__(self, sesion=None):
        if sesion:
            self.s=sesion
        else:
            self.s=requests.Session()
    
    
    def search(self,filter_,max_elements=12):
        """
            max_elements siempre se redondea a ceil(12)
            e.g. 
                si max_elements=15 devuelve 24 elementos
                si max_elements=12 devuelve 12 elementos

            Devuelve lista de Elementos
            Máximo {max_elements}
        """
        url=self.baseurl+"/client/es_ES/bd/search/results"

        todos=[]
        for rw in range(0,max_elements,12):
            #print(rw)
            query={
                "qu":filter_,
                "rw":rw
            }

            r=self.s.get(url,params=query)            

            soup=BeautifulSoup(r.content,"lxml")
            results=soup.findAll(class_="results_bio")

            urls=map(lambda e: e.find(class_="displayDetailLink").a["href"],results)
            elements=map(lambda url: ElementoBNC(url),list(urls))
            todos.extend(list(elements))

        return todos
        

if __name__ == "__main__":
    
    sesion=bnc()
    resultados=sesion.search("george list",max_elements=24)

    print(resultados)