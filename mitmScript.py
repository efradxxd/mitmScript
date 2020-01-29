import multiprocessing
import requests
import json
import mitmproxy
from mitmproxy import http

viejo = ""
pagina = ""
paginastring=""
i=0

def request(flow):
    global viejo
    global bl
    global separacion
    global pagina
    global paginastring
    bl  = "https://meenkai.appspot.com/analisis/blacklist1"
    pagina= flow.request.pretty_url
    veces = 0
    veces+=pagina.count(".js")
    veces+=pagina.count(".gif")
    veces+=pagina.count(".png")
    veces+=pagina.count(".css")
    veces+=pagina.count(".jpg")
    veces+=pagina.count(".txt")
    veces+=pagina.count(".ico")
    
    
    if veces>0:                #Si es un archivo, se omite
        pass
    else:
        separacion = flow.request.pretty_url.split("/")
        if separacion[2] in viejo:       #Si el link se repite, no pasa nada
            pass 
        else:                            #Manda el url a otro nucleo y al servidor
            paginastring='/'.join(separacion)
            p2 = multiprocessing.Process(target=response(flow))
            p2.start()
            viejo = separacion[2]
            
def response(flow):
    if separacion[2] in viejo:       
        pass 
    else:
        if separacion[2] != "192.168.220.1":
            print("-"*70)
            print(paginastring, "funcion response")
            request_query= {"url":paginastring}
            response3 = requests.post(bl,json=request_query)
            resp3= response3.json()
                
            if resp3 == 1:
                print("Phishing")
                print ("Redirigiendo")
                archivo = open("archivo.html","r")           #Enviar a otra pagina
                data = str(archivo.read())
                flow.response.content=bytes(data,"UTF-8")
                
            else:
                global i
                i+=1
                print("No es phishing", i)
                print("-"*70)
        else:
            pass
