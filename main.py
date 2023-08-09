import re 
import time
import requests

from  colorama import Fore
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 



def buscarLlantasValidas(llantas, lista_llantas):
    frase_minusculas = llantas.lower()  # Convertir la frase a minúsculas para realizar una búsqueda insensible a mayúsculas y minúsculas

    for llanta in lista_llantas:
        palabra_minusculas = llanta.lower()  # Convertir la palabra a minúsculas para la comparación insensible a mayúsculas y minúsculas

        if palabra_minusculas in frase_minusculas:
            return True
    return False

def navegacion(url_complemento):
    url=f"https://www.virtualllantas.com/llantas-{url_complemento}"
    browser = webdriver.Firefox()
    browser.get(url)
    browser.maximize_window()
    browser.implicitly_wait(2)
    browser.find_element("xpath",'//*[@id="418535"]').click()
    browser.implicitly_wait(2)
    browser.find_element("xpath",'//*[@value="BOGOTA, D.C."]').click()
    browser.implicitly_wait(2)
    browser.find_element("xpath",'//*[@class="btn btn-primary btn-ubicacion-guardar"]').click()
    time.sleep(2)

    iter=1
    while True:
        scrollHeight = browser.execute_script("return document.body.scrollHeight")
        Height=250*iter
        browser.execute_script("window.scrollTo(0, " + str(Height) + ");")
        if Height > scrollHeight:
            print('End of page')
            break
        time.sleep(0.25)
        iter+=1


    #browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    #time.sleep(2)
    #browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    #browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    #browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    #browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    #time.sleep(2)

    lista_de_llantas_validas=["bridgestone","continental","yokohama","goodyear","nitto","kumho","general","hankook","falken","maxxis","hifly","ovation"]
    enlaces=[]
    Detalles_llanta=[]

    html=browser.page_source

    patron = r'<a\s+href="([^"]*)"\s+title="([^"]*)"[^>]*>'
    llantas_repetida=re.findall(patron,str(html))

    browser.close()


    for llantas in llantas_repetida:
        if buscarLlantasValidas(llantas[1],lista_de_llantas_validas):
            enlaces.append(llantas[0])
            Detalles_llanta.append(llantas[1])

    i=0
    for enlace in enlaces:
        patron_precio_antes = r'<p\s+class="antes"\s+style="[^"]+">\$<strike>([^<]+)</strike>'

        patron_precio_despues = r'<p\s+class="despues"\s+style="[^"]+">\$([^<]+)'

        resultado= requests.get(enlace)
        content= resultado.text

        precio_antes = re.search(patron_precio_antes, content)
        precio_despues = re.search(patron_precio_despues, content)

        precio_antes_valor = precio_antes.group(1) if precio_antes else None
        precio_despues_valor = precio_despues.group(1) if precio_despues else None



        Detalles_llanta[i]+=f",{url_complemento}"
        Detalles_llanta[i]+=","+str(precio_antes_valor)
        Detalles_llanta[i]+=","+str(precio_despues_valor)
        i=i+1
    print(Detalles_llanta)

anchos=[265]
perfiles=[70]
rines=[16]

for ancho in anchos:
    for perfil in perfiles:
        for rin in rines:
            navegacion(f"{ancho}-{perfil}r{rin}")















        
