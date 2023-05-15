import tkinter as tk 
from tkinter import *
from tkinter.font import BOLD
from tkinter import ttk
from PIL import Image, ImageTk
import Sensor
import Effector
from pyswip import Prolog

def initialize_prolog():
    global prolog
    prolog = Prolog()
    prolog.consult("facts.pl")   
    prolog.consult("rules.pl") 


def simulate_sensors():
    print("simula sensori")
    Sensor.setSensorValue("brightness", "20", prolog)
    print(Sensor.getSensorValue("brightness", prolog))

    # Sensor.generete_random_sensors(prolog)
    # sensors = Sensor.getAllSensor(prolog)

    # i=0
    # for k, v in sensors.items():
    #      label_sensor_name = tk.Label(frame2, text=k, font=("Microsoft YaHei",10))
    #      label_sensor_name.grid(row=i, column=0, pady=7, padx=10)

    #      label_sensor_value = tk.Label(frame2, text=v[1], font=("Microsoft YaHei",10))
    #      label_sensor_value.grid(row=i, column=1, pady=7, padx=10)

    #      i=i+1

    


initialize_prolog()
window = tk.Tk()

window.title("Smart Room")
window.geometry("1000x1000")
window.resizable(False, False)

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)


frame1 = tk.Frame(window, background="blue", heigh="100", width="200")
frame2 = tk.Frame(window, background="yellow", heigh="100", width="200")
frame3 = tk.Frame(window, background="red", heigh="100",width="200")
frame4 = tk.Frame(window, background="purple", heigh="100", width="200")

frame1.pack(fill=X)
frame2.pack(fill=BOTH, expand=True, side=LEFT)
frame3.pack(fill=BOTH, expand=True, side=LEFT)
frame4.pack(fill=BOTH, expand=True, side=LEFT)



label_welcome = tk.Label(frame1, text="Welcome in your smart room", font=("Microsoft YaHei",16, BOLD))
label_welcome.pack(pady=20, padx=350)

button_simulate = tk.Button(frame1, text="Simulate sensors", font=("Microsoft YaHei",16), command=simulate_sensors)
button_simulate.pack(padx=10, pady=10)

label_action = tk.Label(frame1, text="Select your action", font=("Microsoft YaHei",10))
label_action.pack(pady=20, padx=350)

action_selected = tk.StringVar()
action_combobox = ttk.Combobox(frame1, textvariable=action_selected)
action_combobox["values"] = ["study", "movie", "sleep", "music", "clean"]
action_combobox.pack(padx=5)
action_combobox["state"] = "readonly"

def select_action(event):
      print(action_selected.get())

action_combobox.bind("<<ComboboxSelected>>", select_action)

photo = ImageTk.PhotoImage(file='pianta stanza.jpg')

label_image = tk.Label(frame3, image=photo, pady=0)
label_image.grid()



effectors = Effector.getAllEffectors()

i=0
for k, v in effectors.items():
    label_effector_name = tk.Label(frame4, text=k, font=("Microsoft YaHei",10))
    label_effector_name.grid(row=i, column=0, pady=7, padx=10)

    label_effector_value = tk.Label(frame4, text=v[1], font=("Microsoft YaHei",10))
    label_effector_value.grid(row=i, column=1, pady=7, padx=10)

    i=i+1

def explanation():
     print("explanation")

button_explanation = tk.Button(frame4, text="Ask explanation", font=("Microsoft YaHei",12), command=explanation)
button_explanation.grid(row = 10, column = 1, padx=10, pady=10)

window.mainloop()