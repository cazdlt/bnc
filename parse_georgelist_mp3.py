#Divide el MP3 de los archivos de George List en su tracklist, según especificado en la descripción
import os
from pydub import AudioSegment 
import re
from itertools import zip_longest

def obtenerPistas(info_filepath):
    with open(info_filepath, encoding="utf-8") as info_file:
        for line in info_file:
            if line.find("Descripcion")==0: #Si Descripcion está al inicio de la linea
                descripcion=line.partition("Descripcion: ")[-1]

    #Obtiene y formatea lista de pistas a partir de la descripción
    tracklist=descripcion.partition(":")[-1]
    end_pistas=tracklist.rindex(")")

    #Los separadores de pistas no son consistentes
    #Algunas descripción están separadas por ";", otras por "--"
    # pistas=[p.strip() for p in tracklist[:end_pistas+1].split(";")]
    # if len(pistas)==1:
    #     pistas=[p.strip() for p in tracklist[:end_pistas+1].split("--")]

    pistas_idx=[m.start() for m in re.finditer("[0-9]+\.",tracklist)]
    pistas=[]
    for start,end in zip_longest(pistas_idx,pistas_idx[1:],fillvalue=-1):
        track=tracklist[start:end]
        end_pista=track.rindex(")")
        track=track[:end_pista+1]
        pistas.append(track)
    
    return pistas

def parseTracks(trackinfo):
    tracknumber,_,track=trackinfo.partition(".")

    name,_,length=track.rpartition("(")

    mins,secs=length[:-1].split(":")
    length_secs=int(secs)+60*int(mins)
    return (tracknumber,name.strip(),length_secs)

if __name__ == "__main__":
    filename="Música interpretada por los Gaiteros de San Jacinto y preguntas - George List - 1965"
    root="./output/George List"
    info_filepath=f"{root}/{filename}/info.txt"

    #obtener nombres y largos de pistas
    pistas=obtenerPistas(info_filepath)
    tracklist=[parseTracks(t) for t in pistas]

    audio_filepath=f"{root}/{filename}/{filename}.mp3"
    audio=AudioSegment.from_mp3(audio_filepath)
    audio = audio.set_frame_rate(48000)

    os.makedirs(f"{root}/{filename}/tracks", exist_ok=True)
    for number,name,length in tracklist:
        length*=1000 #convierte a ms
        track=audio[:length] #obtiene la pista actual
        audio=audio[length:] #recorta la pista actual

        name=re.sub("[\\\/]","-",name)
        name=re.sub("[\"\'\:]","",name)
        path_=f"{root}/{filename}/tracks/{name}.mp3"
        track.export(path_, format="mp3",tags={"track":number})