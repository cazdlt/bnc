from bnc import bnc,ElementoBNC
import os
import re

# buscar="George List"
buscar="Bullerengue"
autor="List"
root_salida="output"
num_elementos=15

print("Buscando...")
resultados=bnc().search(buscar,max_elements=num_elementos,autor=autor)
assert len(resultados)>0,"Ningún elemento encontrado."
print(f"Se han recuperado los primeros {len(resultados)} elementos.")
print(f"Descargando los primeros {min(len(resultados),num_elementos)}\n")

catalogo="DESCARGADO:\n\n"
for idx,resultado in enumerate(resultados):
    
    if idx>num_elementos-1: #solo descarga los elementos indicados por el usuario
        break

    filename=re.sub('[\\\/\*\?\|\[\]\(\):"<>]',"",resultado.titulo)
    filename=re.sub("\s{2,}"," - ",filename)+" - "+resultado.fecha
    a,b = 'ÁÉÍÓÚÜáéíóúü','AEIOUUaeiouu'
    trans = filename.maketrans(a,b)
    filename=filename.translate(trans)
    
    path=f"./{root_salida}/{buscar}/{filename}"
    info=f"Título: {resultado.titulo}\n"
    info+=f"Autor: {resultado.autor}\n"
    info+=f"Fecha: {resultado.fecha}\n"
    info+=f"Tema: {resultado.tema}\n"
    info+=f"Formato: {resultado.formato}\n"
    info+=f"Descripcion: {resultado.descripcion}\n"
    info+=f"Ruta: {path}\n\n"
    catalogo+=info

    if os.path.isfile(f"{path}/info.txt"):
        print(f"El contenido de {resultado} ya ha sido descargado")
    else:
        os.makedirs(path, exist_ok=True)       
        print(f"\nDescargando de: {resultado}")
        resultado.downloadContent(path=path)

    open(f"{path}/info.txt","w+",encoding="utf-8").write(info)

open(f"./{root_salida}/{buscar}/catalogo.txt","w+",encoding="utf-8").write(catalogo)