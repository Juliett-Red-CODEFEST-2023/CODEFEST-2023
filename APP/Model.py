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
import pytesseract
from PIL import Image
import os
import cv2
from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import easyocr

tagger = SequenceTagger.load("flair/ner-spanish-large")

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
            
            
def img_Info (img_Coord_N, img_Coord_W, img_Time): #parametros son listas de imagenes de donde se encuentra la información respectiva del lapso de tiempo en el que ubicó el objeto en cuestión con diferencial de medio segundo
    i = 0
    N = None
    W = None
    T = None
    while (i<len(img_Coord_N)):
        N_1 = pytesseract.image_to_string(Image.open(img_Coord_N[i]))  
        W_1 = pytesseract.image_to_string(Image.open(img_Coord_W[i]))
        T_1 = pytesseract.image_to_string(Image.open(img_Time[i]))
        try:#Verificacion de que la informacion tomada de la captura haya sido  
            N_ = N_1
            N_ = N_.replace('°','')
            N_ = N_.replace('\'','')
            N_ = N_.replace('\"','')
            N_ = N_.replace('.','')
            Contr = int(N_)
            if (len(N_) == 7):
                N = N_1
                W_ = W_1
                W_ = W_.replace('°','')
                W_ = W_.replace('\'','')
                W_ = W_.replace('\"','')
                W_ = W_.replace('.','')
                Contr = str(W_)
            if (len(W_) == 7):
                W = W_1
                T_ = T_1
                T_ = T_.replace(':','')
                T_ = T_.replace('/','')
                Contr = str(N_)
            if (len(N_) == 6 or len(N_) == 5):
                T = T_1
            i+=1
        except: 
            None
        if ((N == None) or (W == None) or (T == None)):
            return None

    info = {'N': N,'W': W,'Time':T}
    return info

def isFlattt(imagen):
    alpha = 255
    res = True
    # Convierte la imagen a una lista de valores de píxeles
    rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    # Divide la imagen en los canales R, G y B
    r, g, b = cv2.split(rgb)
    
    vec_R = r.flatten()
    vec_G = g.flatten()
    vec_B = b.flatten()
    
    # Calcula la desviación estándar de los valores de los píxeles
    std_R = np.std(vec_R, axis=0)
    std_G = np.std(vec_G, axis=0)
    std_B = np.std(vec_B, axis=0)
    
    if std_R < alpha or std_G < alpha or std_B < alpha:
        res = False

    return res

def cropImage(image):
    # Recorta la imagen usando la indexación de arrays en NumPy
    aim = image[300:420, 536:746]
    coord = image[42: 58, 946: 1228]
    time = image[136:174, 22:96]
    plt.imshow(aim)
    return aim, coord, time

def goodCrop(image):
    aim, coord, time = cropImage(image)
    
def findText(imagen):
    text = False
    pi = 0.415
    
    # Convierte la imagen a una lista de valores de píxeles
    rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
    # Divide la imagen en los canales R, G y B
    r, g, b = cv2.split(rgb)
    # Umbraliza el canal de color para evitar ruidos
    gu = g < pi
    
    aimG, coordG, timeG = cropImage(gu)
    
    reader = easyocr.Reader(['en'])

    strCoord = reader.readtext(coordG)
    print(strCoord)
    strTime = reader.readtext(timeG)
    print(strTime)
    if strCoord != None and strTime != None:
        text = True
        return text, strCoord, strTime
    else:
        return text
    
def getFrames(ruta_Video):
    # Crea un directorio para las imágenes, si no existe
    ext = ruta_Video.split("_")[1]
    ext = ext.split(".")[0]
    print(ext)
    out = "frames_" + ext
    
    if not os.path.exists(out):
        os.makedirs(out)
        os.makedirs(out + "/crops")

    # Abre el video
    video = cv2.VideoCapture(ruta_Video)
    
    # Obtiene el número total de frames, 
        #la tasa de frames por segundo 
        #y calcula la duración a minutos.
    minutes = video.get(cv2.CAP_PROP_FRAME_COUNT)/(video.get(cv2.CAP_PROP_FPS)*60)
    print(minutes)

    # Variable para llevar un registro del número de frame
    frame_num = 1
    # Variable para desplazar el registro del número de frame
    frame_offset = 10
    while len(os.listdir(out)) <= (10*minutes):
        # Lee un frame del video

        if frame_num % (300 + frame_offset) == frame_offset:
            buffer, frame = video.read()
            print("modulo 30 exitoso")
            # Si el frame no es válido (por ejemplo, hemos llegado al final del video), 
                # Si el frame no es válido y se tienen 2 imagenes por minuto, 
                    #se sale del bucle 
            if not buffer:
                print("not buffer")
                    # Si el frame no es válido y NO se tienen 2 imagenes por minuto,
                        #Se reinicia el contador y se desplaza el offset
                print("reinicia y hace offset")
                frame_num = 1
                frame_offset += 90

            else:
                    #if not isFlattt(frame):
                    # Guarda el frame como una imagen JPEG
                cv2.imwrite(out +'/frame{:04d}.jpg'.format(frame_num), frame)
                print("Creado frame: ", frame_num)
                aim, coord, time = cropImage(frame)
                cv2.imwrite(out +'/crops{:04d}.jpg'.format(frame_num), aim)

                    # Incrementa el número de frame
        frame_num += 1

    # Libera el video
    video.release()
    print("Proceso finalizado.")

