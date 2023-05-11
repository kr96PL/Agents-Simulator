import random
import math
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import *
from KMeans import *
from DataGenerator import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

window = Tk() #instance of window
window.geometry("840x420")
window.title("Agents Simulator")
window.config(background="#202124")

count = 0

def runSimulation():
    agents = int(entryAgents.get()) 
    sAgents = int(entrySAgents.get())
    print('Simulation running')
    print(agents)
    print(sAgents)

labelInputs = Label(window, 
                    text="- Inputs -", 
                    font=('Arial', 9, 'bold'), 
                    fg="white", 
                    background="#202124")

labelAgents = Label(window, 
                    text="Agents", 
                    font=('Arial', 9, 'bold'), 
                    fg="white", 
                    background="#202124")

labelSAgents = Label(window, 
                     text="s - Agents", 
                     font=('Arial', 9, 'bold'), 
                     fg="white", 
                     background="#202124")

labelKMin = Label(window, 
                    text="Kmin", 
                    font=('Arial', 9, 'bold'), 
                    fg="white", 
                    background="#202124")

labelKMax = Label(window, 
                     text="Kmax", 
                     font=('Arial', 9, 'bold'), 
                     fg="white", 
                     background="#202124")

labelInputs.place(x=20, y=20)
labelAgents.place(x=20, y=50)
labelSAgents.place(x=20, y=80)
labelKMin.place(x=20, y=110)
labelKMax.place(x=20, y=140)

entryAgents = Entry(window,
                    font=('Arial', 9))

entrySAgents = Entry(window,
                     font=('Arial', 9))

entryKMin = Entry(window,
                    font=('Arial', 9))

entryKMax = Entry(window,
                    font=('Arial', 9))

entryAgents.insert(0, "100")
entrySAgents.insert(0, "20")

entryAgents.place(x=150, y=50)
entrySAgents.place(x=150, y=80)
entryKMin.place(x=150, y=110)
entryKMax.place(x=150, y=140)

button = Button(window, 
                text="Simulate",
                command=runSimulation,
                font=("Arial", 9, 'bold'),
                fg="white",
                padx=10,
                bg="#cc5801",
                activeforeground="white",
                activebackground="#cc5801")

button.place(x=20, y=170)




data = DataGenerator().generate(100, 0, 1)

# x = []
# y = []

# for point in data:
#     x.append(point[0])
#     y.append(point[1])

# figure1 = plt.Figure(figsize=(5, 5), dpi=100)
# ax = figure1.add_subplot(111)

# ax.scatter(x, y, color="red")

# canvas = FigureCanvasTkAgg(figure1, window)
# canvas.draw()
# canvas.get_tk_widget().place(x=300, y=50)



data = DataGenerator().generate(100, 0, 1)

kmeans = KMeans(100, data, 2)

group = kmeans.group()

figure1 = plt.Figure(figsize=(5, 5), dpi=100)
ax = figure1.add_subplot(111)

for k in group:
    x = []
    y = []

    for point in k['data']:
        x.append(point[0])
        y.append(point[1])
    print(x)
    print(y)
    ax.scatter(x, y)

      


# ax.scatter(x, y, color="red")

canvas = FigureCanvasTkAgg(figure1, window)
canvas.draw()
canvas.get_tk_widget().place(x=300, y=50)

window.mainloop() #place window on computer screen, listen for events
