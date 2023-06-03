#!pip3 install config

import config
import importlib
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from flair.data import Sentence
from flair.models import SequenceTagger
import datetime
import pandas as pd
import csv
!pip3 install flair
!pip3 install python-dateutil
!pip3 install config
tagger = SequenceTagger.load("flair/ner-spanish-large")
print("Hola")
def datastructs():
    data_structs={}
    data_structs["mapa_ubicaciones"]=mp.newMap
    data_structs["mapa_textos"]=mp.newMap
    return data_structs 

inicializacion=True
data_structs=None
if inicializacion==True:
    print("Bienvenidos")
    data_structs=datastructs()
    input_type=input("Ingrese [ubicacion] si se trata de un string de ubicación o [texto] si se trata de un texto: ")
    text=input("Ingrese la ubicacion o el texto segun corresponda: ")
    p1_textos(input_type,text,data_structs,"NOTICIAS DE LA AMAZONIA_CODEFEST.xlsx")
    

def load_textos(name,data_structs):
    """
    Carga los datos en mapas
    """
    df = pd.read_excel(name)
    df.to_csv("CSV.csv", index=False)
    input_file= csv.DictReader(open("CSV.csv",encoding="utf-8"))
    lista=estructura["texto"]
    for i in input_file:
        addUbicaciones(i,data_structs)
        addTextos(i,data_structs)

def addUbicaciones(i,data_structs):
    info_adicional=GetInfo(i)
    org="Unknown"
    loc="Unknown"
    per="Unknown"
    dates=format_Fecha(i["FECHA"])
    misc="Unknown"
    impact="Neutral"
    if info_adicional.get("ORG",None)!=None:
        org=  info_adicional.get("ORG")
    if info_adicional.get("LOC",None)!=None:
        loc=info_adicional.get("LOC")[0]
    if info_adicional.get("MISC",None)!=None:
        loc=info_adicional.get("MISC")
    if info_adicional.get("IMPACT",None)!=None:
        impact="Negative"
    dic={"Text":i,"Org":org,"Loc":loc,"Per":per,"Dates":dates,"Misc":misc,"Impact":impact}
    mapa_ubicaciones=data_structs["mapa_ubicaciones"]
    if loc!= "Unknown":
        if mp.contains(mapa_ubicaciones,loc):
            entry=me.get(mapa_ubicaciones,loc)
            value=me.getValue(entry)
            value.append(dic)
            mp.put(mapa_ubicaciones,loc,value)
    else:
        mp.put(mapa_ubicaciones,loc,[dic])

          
def addTextos(i,data_structs):
    info_adicional=GetInfo(i["TEXTO"])
    org="Unknown"
    loc="Unknown"
    per="Unknown"
    dates=format_Fecha(i["FECHA"])
    misc="Unknown"
    impact="Neutral"
    if info_adicional.get("ORG",None)!=None:
        org=  info_adicional.get("ORG")
    if info_adicional.get("LOC",None)!=None:
        loc=info_adicional.get("LOC")[0]
    if info_adicional.get("MISC",None)!=None:
        loc=info_adicional.get("MISC")
    if info_adicional.get("IMPACT",None)!=None:
        impact="Negative"
    dic={"Text":i,"Org":org,"Loc":loc,"Per":per,"Dates":dates,"Misc":misc,"Impact":impact}
    mapa_textos=data_structs["mapa_textos"]
    newtexto=i.replace(" ","_")
    if not mp.contains(mapa_textos,newtexto):
          mp.put(mapa_textos,newtexto,dic)
                       
def GetInfo(info):
    oracion=Sentence(info["TEXTO"])
    tagger.predict(oracion)
    dic={}
    string=str(oracion)
    particion=string.split("→")
    if len(particion)>1:
        tags=particion[1].replace("[","")
        tags=tags.replace("]","")
        tags=tags.replace("\"","")
        lista=tags.split(",")
        for i in lista:
            todo=i.split("/")
            if len(todo)>1:
                valor=todo[0]
                atributo=todo[1]
                existe=dic.get(atributo,None)

                if atributo not in atributos_predeterminados:
                    if existe ==None:
                        dic[atributo]=[valor]    
                    else:
                        if valor not in dic[atributo]:
                            dic[atributo].append(valor)
                        
        #print('The following NER tags are found:')
        #for entity in oracion.get_spans('ner'):
            #pass
            #print(entity)
    return dic
                       
def p1_textos(input_type,text,data_structs,filename):
    load_textos(filename,data_structs)
    data_structs["mapa_ubicaciones"]=mapa_ubicaciones
    data_structs["mapa_textos"]=mapa_textos
    if input_type=="texto":
        lista=text.split(" ")
        size=len(lista)
        if size > 4:
            #es un texto
            exist=mp.contains(mapa_textos,text)
            if not exist:
                keys=mp.keySet(mapa_textos)
                entry=None
                for i in lt.iterator(keys):
                    if text in i:
                        entry=mp.get(mapa_textos,i)
                        break
                if entry!=None:
                    return me.getValue(entry)
                else:
                    return "No hay información disponible"
            else:
                    entry=mp.get(mapa_textos,text)
                    return me.getValue(entry) 
        else:
            #es una ubicacion
            exist=mp.contains(mapa_ubicaciones,text)
            if not exist:
                keys=mp.keySet(mapa_ubicaciones)
                entry=None
                for i in lt.iterator(keys):
                    if text in i:
                        entry=mp.get(mapa_ubicaciones,i)
                        break
                if entry != None:
                    return me.getValue(entry)
                else:
                    return "No hay información disponible"
            else:
                entry=mp.get(mapa_ubicaciones,text)
                return me.getValue(entry)
            
