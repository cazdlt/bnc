#leer audio quicktime del catálogo de la biblioteca nacional
import requests
from bs4 import BeautifulSoup
import re

class bnc():

    baseurl="https://catalogoenlinea.bibliotecanacional.gov.co"
    s=requests.Session()

    def downloadAudio(self,content_url,output_filename=None):
        """
        Descarga el archivo de audio encontrado en una página de contenido QuickTime de la Biblioteca Nacional de Colombia (e.g. https://catalogoenlinea.bibliotecanacional.gov.co/client/es_ES/search/stream/58063/false/0)
        Si {output_filename} existe, lo guarda en el workspace como {output_filename}.extension_original
        Lo devuelve al contexto donde fue llamada la función
        """
        r=self.s.get(self.baseurl+content_url)
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
        

if __name__ == "__main__":
    content_url="/client/es_ES/search/asset/58090/0"
    output_name="san_jacinto"
    sesion=bnc()
    mp3=sesion.downloadAudio(content_url,output_name)