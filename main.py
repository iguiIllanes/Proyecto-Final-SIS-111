# Autor: Ignacio Andres Illanes Bequer
# github: https://github.com/iguiIllanes

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

nombre_de_usuario = "ignacio.illanes@ucb.edu.bo"
password = "sj7n\-QY4@[t"

url = "https://neo.ucb.edu.bo/"

navegador = webdriver.Chrome() #Inicia una instancia de Chrome con Selenium
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
sleep(30)
navegador.get(url+"my_calendar")