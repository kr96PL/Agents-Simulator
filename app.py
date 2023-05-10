from tkinter import *

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

window.mainloop() #place window on computer screen, listen for events
