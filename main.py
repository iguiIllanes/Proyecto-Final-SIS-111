#Author: Ignacio Illanes Bequer
#Github:https://github.com/iguiIllanes/

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.color import Color
from time import sleep
from ics import Calendar, Event


background_color = '#0C8699'

url = "https://neo.ucb.edu.bo/"

materias_blacklist = []

navegador = webdriver.Chrome()
# navegador.set_window_position(-10000, 1150)

correo=''
pswd=''
def get_user_input(): #obtiene el correo y la contrasena para google sign in
    correo = email_Entry.get()
    pswd = pass_Entry.get()
    if pswd == '' or correo == '':
        messagebox.showwarning('Aviso', 'Correo o contraseña vacios.')
    elif '@ucb.edu.bo' in correo:
        google_sign_in(correo, pswd)
        generate_calendar()
        return
    else:
        messagebox.showwarning('Aviso', 'Correo incorrecto. debe ser un correo con dominio @ucb.edu.bo')


def format_blacklist(blacklist_string): #Formatea el texto de open_blacklist_window para que se pueda colocar en materias_blacklist
    aux=''
    for letra in blacklist_string:
        if letra != '/': aux+=letra
        else:
            materias_blacklist.append(aux)
            aux=''
    materias_blacklist.append(aux)
    return


def open_blacklist_window(): #Crea una ventana para anadir elementos materias_blacklist
    blacklist_window = tk.Toplevel()
    blacklist_window.title('Editar lista negra')
    blacklist_window.geometry('{}x{}+{}+{}'.format(700, 200, half_width, half_height))
    blacklist_window['background'] = background_color
    blacklist_text = tk.Label(blacklist_window, text='Escribe el NOMBRE COMPLETO de la asignatura o grupo del calendario que quieres que no se tome en cuenta.\nSeparalos con /', bg=background_color, fg='#fff')
    blacklist_text.pack()
    blacklist_texfield = tk.Entry(blacklist_window, width=50)
    blacklist_texfield.pack()
    blacklist_buttons_frame = tk.Frame(blacklist_window, bg=background_color)
    blacklist_buttons_frame.pack(expand=True)
    blacklist_cancel_button = tk.Button(blacklist_buttons_frame, text="Cancelar", height=2, command=lambda:blacklist_window.destroy())
    blacklist_cancel_button.pack(padx=(0,50), side=tk.LEFT)
    blacklist_add_button = tk.Button(blacklist_buttons_frame, text="Añadir", height=2, command=lambda:[format_blacklist(blacklist_texfield.get()), blacklist_window.destroy()])
    blacklist_add_button.pack(side=tk.LEFT)
    blacklist_window.mainloop()





def google_sign_in(nombre_de_usuario, password): #Inicia sesion en NEO-LMS con la cuenta de google
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

def materia_color_link(): #Crea un vinculo entre el codigo de la materia y su color asignado en el calendario
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

def retornar_cal(): #Retorna un arreglo de diccionarios con la informacion extraida del calendario
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
    

def generate_calendar(): #Genera el archivo ics con los eventos del calendario de NEO-LMS
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
    navegador.quit()

    messagebox.showinfo('Exito', 'Calendario generado!')


#Main
window = tk.Tk(className=' NEO Calendar Generator') #Crea la GUI principal
window_width = 900
window_height = 500
half_width = int(window.winfo_screenwidth()/2 - window_width/2)
half_height = int(window.winfo_screenheight()/2 - window_height/2)
window.geometry('{}x{}+{}+{}'.format(window_width, window_height, half_width, half_height))
window['background']=background_color



logo_frame = tk.Frame(window)
logo_frame.pack(expand=True)

logo_img = ImageTk.PhotoImage(Image.open('resources/images/neo-lms-logo.png'))
logo = tk.Label(logo_frame, image=logo_img, height=250)
logo.pack(expand=True)



credentials_frame = tk.Frame(window,bg=background_color)
credentials_frame.pack(expand=True)

email_Entry = tk.Entry(credentials_frame, width=30)
email_Label = tk.Label(credentials_frame, text='Correo:', bg=background_color, fg='#fff')
email_Label.pack(padx=(0,10),  side=tk.LEFT)
email_Entry.pack(side=tk.LEFT)

pass_Entry = tk.Entry(credentials_frame, width=30)
pass_Label = tk.Label(credentials_frame, text='Contraseña:', bg=background_color, fg='#fff')
pass_Label.pack(padx=(80,10),  side= tk.LEFT)
pass_Entry.pack(side=tk.LEFT)



buttons_frame = tk.Frame(window, bg=background_color)
buttons_frame.pack(expand=True)

blacklist_button = tk.Button(buttons_frame, text='Lista Negra', height=2, command=lambda:open_blacklist_window())
blacklist_button.pack(side=tk.LEFT)

exportar_button = tk.Button(buttons_frame, text='Exportar Calendario', height=2, command=lambda:[messagebox.showinfo('Aviso', 'Espera al mensaje que indica que el calendario se exporto con exito.'), get_user_input()])
exportar_button.pack(padx=(50,0), side=tk.LEFT)

window.mainloop()