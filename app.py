import sys
import random
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tkinter import *
from KMeans import *
from DataGenerator import *
from Policy import *
from Cycle import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

window = Tk() 
window.geometry("1100x600")
window.title("Agents Simulator")
window.config(background="#202124")
data = []

def runSimulation():
    N = int(entryAgents.get()) #liczba wszystkich agentów
    S = int(entrySAgents.get()) #liczba s-agentów
    C = int(entryCycles.get()) #liczba cykli
    kMin = int(entryKMin.get())
    kMax = int(entryKMax.get())
    ExpoA = float(entryExpoA.get())
    ExpoG = float(entryExpoG.get())
    V0 = float(entryV0.get())
    x = 0.1
    y = 0.1
    z = 0.1
    sAgent = []

    #Losowe wybranie s-agentów z wszystkich agentów
    sAN = 0
    while (sAN < S):
        rand = random.randint(0, N)
        if rand not in sAgent:
            sAgent.append(rand)
            sAN += 1

    #iterowanie po każdym cyklu
    for cycle in range(C):
        sumPHToS = .0 
        numberHJS = 0 
        sumPSToH = .0  
        numberSJH = 0 
        counterSSCoop = 0
        counterAllCoop = 0
        adj = {}

        for adjI in range(N):
            adj[adjI] = []

        # Parowanie kleintów z dostawca
        for iN in range(N):
            countC = 0
            clients = random.randint(kMin, kMax)
            inJ = 0
            rn = 0
            
            while inJ < clients:
                rn = random.randint(0, N)
                if rn != iN and rn not in adj[iN]:
                    adj[iN].append(rn)
                    if iN in sAgent:
                        if rn not in sAgent:
                            numberSJH += 1
                    else:
                        if rn in sAgent:
                            numberHJS += 1
                    inJ += 1
        
        agentsR = {}

        for iN in range(N):
            clients = adj[iN]
            vProv = V0 if cycle == 0 else 1
            numClients = len(clients)
            meanPolicyR = .0

            for client in clients:
                vRepo = V0 if cycle == 0 else data[cycle - 1].V[client]
                L = Policy.hStep(vRepo, x)
                p = Policy.sBiasP(y, L) if iN in sAgent else L 
                if iN in sAgent and client in sAgent:
                    p = 1.0
                policyP = Policy.providerPolicy(Policy.randExpoD(ExpoA), p)

                L = Policy.hStep(vProv, x)
                r = Policy.sBiasR(z, L) if client in sAgent else L
                if iN in sAgent and client in sAgent:
                    r = 1.0
                policyR = Policy.reporterPolicy(Policy.randExpoD(ExpoG), policyP, r)
                meanPolicyR += policyR * vProv

                if iN in sAgent and client in sAgent: 
                    counterSSCoop += 1
                
                counterAllCoop += 1

                if iN in sAgent:
                    if client not in sAgent:
                        sumPSToH += policyP
                else:
                    if client in sAgent:
                        sumPHToS += policyP
            
            meanPolicyR /= numClients
            agentsR[iN] = meanPolicyR
        

        print(agentsR)
        sys.exit()
        

    # data = DataGenerator().generate(agents, 0, 1)
    # kmeans = KMeans(1000, data, 2)

    # group = kmeans.group()

    # figure1 = plt.Figure(figsize=(7, 5), dpi=100)
    # ax = figure1.add_subplot(111)

    # for k in group:
    #     x = []
    #     y = []

    #     for point in k['data']:
    #         x.append(point[0])
    #         y.append(point[1])
    #     ax.scatter(x, y)

    # canvas = FigureCanvasTkAgg(figure1, window)
    # canvas.draw()
    # canvas.get_tk_widget().place(x=340, y=50)

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

labelCycles = Label(window, 
                    text="Cycles", 
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

labelExpoA = Label(window, 
                    text="ExpoA", 
                    font=('Arial', 9, 'bold'), 
                    fg="white", 
                    background="#202124")

labelExpoG = Label(window, 
                    text="ExpoG", 
                    font=('Arial', 9, 'bold'), 
                    fg="white", 
                    background="#202124")

labelV0 = Label(window, 
                    text="V0", 
                    font=('Arial', 9, 'bold'), 
                    fg="white", 
                    background="#202124")
                       
labelInputs.place(x=20, y=20)
labelAgents.place(x=20, y=50)
labelSAgents.place(x=20, y=80)
labelCycles.place(x=20, y=110)
labelKMin.place(x=20, y=140)
labelKMax.place(x=20, y=170)
labelExpoA.place(x=260, y=50)
labelExpoG.place(x=260, y=80)
labelV0.place(x=260, y=110)

entryAgents = Entry(window,
                    font=('Arial', 9))

entrySAgents = Entry(window,
                    font=('Arial', 9))

entryCycles = Entry(window,
                    font=('Arial', 9))

entryKMin = Entry(window,
                    font=('Arial', 9))

entryKMax = Entry(window,
                    font=('Arial', 9))

entryExpoA = Entry(window,
                    font=('Arial', 9))

entryExpoG = Entry(window,
                    font=('Arial', 9))       

entryV0 = Entry(window,
                    font=('Arial', 9))           

entryAgents.insert(0, "1000")
entrySAgents.insert(0, "150")
entryCycles.insert(0, "100")
entryKMin.insert(0, "50")
entryKMax.insert(0, "150")
entryExpoA.insert(0, "0.5")
entryExpoG.insert(0, "0.5")
entryV0.insert(0, "0.1")

entryAgents.place(x=100, y=50)
entrySAgents.place(x=100, y=80)
entryCycles.place(x=100, y=110)
entryKMin.place(x=100, y=140)
entryKMax.place(x=100, y=170)
entryExpoA.place(x=340, y=50)
entryExpoG.place(x=340, y=80)
entryV0.place(x=340, y=110)

button = Button(window, 
                text="Simulate",
                command=runSimulation,
                font=("Arial", 9, 'bold'),
                fg="white",
                padx=10,
                bg="#cc5801",
                activeforeground="white",
                activebackground="#cc5801")

button.place(x=20, y=210)

window.mainloop() #place window on computer screen, listen for events
