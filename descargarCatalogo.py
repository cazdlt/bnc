from bnc import bnc,ElementoBNC
import os
import re

buscar="George List"
root_salida="output"
num_elementos=2

print("Buscando...")
resultados=bnc().search(buscar,max_elements=num_elementos)
print(f"Se han recuperado los primeros {len(resultados)} elementos.")
print(f"Descargando los primeros {num_elementos}\n")

catalogo="DESCARGADO:\n\n"
for idx,resultado in enumerate(resultados):

    if idx>num_elementos-1:
        break

    filename=re.sub('[\\\/\*\?\|\[\]\(\):"<>]',"",resultado.titulo)
    filename=re.sub("\s{2,}"," - ",filename)

    path=f"./{root_salida}/{buscar}/{filename}"
    os.makedirs(path, exist_ok=True)

    info=f"Título: {resultado.titulo}\n"
    info+=f"Autor: {resultado.autor}\n"
    info+=f"Fecha: {resultado.fecha}\n"
    info+=f"Tema: {resultado.tema}\n"
    info+=f"Formato: {resultado.formato}\n"
    info+=f"Descripcion: {resultado.descripcion}\n"
    info+=f"Ruta: {path}\n\n"
    catalogo+=info

    print(f"\nDescargando de: {resultado}")
    resultado.downloadContent(path=path+"/"+filename)
    open(f"{path}/info.txt","w+",encoding="utf-8").write(info)

open(f"./{root_salida}/{buscar}/catalogo.txt","w+",encoding="utf-8").write(catalogo)