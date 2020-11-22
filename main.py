# Author: Ignacio Andres Illanes Bequer
# github: https://github.com/iguiIllanes

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.color import Color
from time import sleep
import re
from ics import Calendar, Event

nombre_de_usuario = "ignacio.illanes@ucb.edu.bo"
password = "sj7n\-QY4@[t"

url = "https://neo.ucb.edu.bo/"


materias_blacklist = ['Centro', 'Grupo 1', 'Grupo 3', 'Grupo 4', 'Personal']

navegador = webdriver.Chrome() #Inicia una instancia de Chrome con Selenium

def google_sign_in(nombre_de_usuario, password):
    navegador.get(url)
    elemento = navegador.find_element_by_id("google_apps_btn") #Encuentra el boton de iniciar sesion con google en neo.ucb.bo a traves de su id
    elemento.click()
    elemento = navegador.find_element_by_xpath('//*[@id="identifierId"]') #Encuentra el campo para el correo electronico gracias a su XPATH
    elemento.send_keys(nombre_de_usuario)
    siguiente_btn = navegador.find_element_by_xpath('//*[@id="identifierNext"]/div/button') #Encuentra el boton siguiente
    siguiente_btn.click()
    sleep(3) #El programa espera 3 segundos hasta que la proxima parte de la pagina pueda cargar
    elemento = navegador.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input') #Encuentra el campo para la contrasena gracias a su XPATH
    elemento.send_keys(password)
    siguiente_btn = navegador.find_element_by_xpath('//*[@id="passwordNext"]/div/button') #Encuentra el boton siguiente
    siguiente_btn.click()
    print("Tiene 30 segundos para poder conceder el acceso a su cuenta de google desde el telefono")
    sleep(15)
    navegador.get(url+"my_calendar") 

def materia_color_link():
    materias = navegador.find_elements_by_class_name("calendar-item")
    materias_text = {}
    for materia in materias:
        if materia.text not in materias_blacklist:
            materia_new=""
            for letra in materia.text:
                if letra != ' ':
                    materia_new+=letra
                else:
                    break
            materias_text[materia.find_element_by_tag_name('label').get_attribute('data-color')] = materia_new
    return materias_text

def retornar_cal():
    calendario = []
    fechas = navegador.find_elements_by_class_name('editable')
    for fecha in fechas:
        date = fecha.get_attribute('data-add-event')
        separar=False #Desde lineas 44-61 formatea el texto para cumplir con el formato para el argumento de TODO
        anio=date[:4]
        mes=""
        dia=""
        for i in range(5,len(date)):
            if not separar:
                if date[i] != ',':
                    mes+=date[i]
                else:
                    separar=True
            else:
                if date[i] != ',':
                    dia+=date[i]
        if len(mes)==1:
            mes="0"+mes
        if len(dia)==1:
            dia="0"+dia
        fecha_new=anio+'-'+mes+'-'+dia+' 04:00:00'

        elementos_cal = fecha.find_elements_by_class_name('general_event') #esto convierte el recuadro del elemento del calendario neo de rgb a hexadecimal
        color_list=[]
        names={}
        materias_dict = materia_color_link()
        for elemento_cal in elementos_cal:
            rgb=elemento_cal.value_of_css_property('background-color')
            color=(Color.from_string(rgb).hex).upper()
            if color in materias_dict.keys(): 
                event_name=materias_dict[color]+' '+elemento_cal.text
                calendario.append({"name":event_name, "fecha":fecha_new})
    return calendario
    
#Main
google_sign_in(nombre_de_usuario, password)
calendar = Calendar()
calendario = retornar_cal()
for evento in calendario:
    event = Event()
    event.name = evento["name"]
    event.begin = evento["fecha"]
    calendar.events.add(event)
    calendar.events

with open('CalendarioNEO.ics', 'w') as mi_archivo:
    mi_archivo.writelines(calendar)
print("Calendario Generado!")