# bnc
Descarga de contenido de la Bilioteca Nacional de Colombia (BNC). <br>
El contenido de la BNC es abierto y fácilmente descargable desde su catálogo, esta herramienta solo facilita esta operación. <br>
Capacidades:
- Realizar búsquedas de elementos 
    - También admite búsquedas por autor
    - Para descargar el contenido de todos los elementos encontrados en la búsqueda, ver el script "descargarCatálogo.py"
    - Modo de uso
        ```python
        from bnc import bnc
        buscar_por="Ejemplo"
        autor="Andrés Zamora" #buscar solo por autor. opcional
        max_elements=12 #número máximo de elementos a devolver. opcional. múltiplos de 12.
        resultados=bnc().search(buscar_por,autor=autor,max_elements=max_elements)
        ```

- Descargar el contenido de uno o varios elementos específicos del catálogo. 
    - Modo de uso:
        ```python
        from bnc import ElementoBNC
        url="https://catalogoenlinea.bibliotecanacional.gov.co/client/es_ES/bd/search/detailnonmodal/ent:$002f$002fSD_ASSET$002f0$002fSD_ASSET:58063/ada?qu=bullerengue"
        elemento=ElementoBNC(url) # también permite la url relativa (/client/es_ES/bd/...)

        ruta_descarga="/ruta/descarga" # opcional. si no se entrega este parámetro, no se descarga el contenido, únicamente se devuelve como variable
        nombre_descarga="bullerenge" # opcional. únicamente se tiene en cuenta si ruta_descarga existe. si no se entrega este parámetro, se descarga con su nombre original
        contenido_raw=elemento.downloadContent(path=ruta_descarga, filename=nombre_descarga)
        ```
- Para el contenido en el que en sus autores se encuentre George List, es posible analizar la descripción del elemento para separar su contenido de audio en difertentes pistas.
    - Ver *parse_georgelist_mp3.py*
