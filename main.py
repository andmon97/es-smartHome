import tkinter as tk 
from tkinter import *
from tkinter.font import BOLD
from tkinter import ttk
from PIL import Image, ImageTk

def simulate_sensors():
    print("simula sensori")

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
label_image.place(x=0, y=0, relwidth=1.0, relheight=1.0)



window.mainloop()