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
import time

window = Tk() 
window.geometry("1100x600")
window.title("Agents Simulator")
window.config(background="#202124")
data = []

def plot_on_frame(series):
    n = len(series[0][1])
    x_values = list(range(1, n + 1))

    fig, ax = plt.subplots()
    for name, values in series:
        ax.plot(x_values, values, label=name)

    ax.set_xlabel("Cycle")
    ax.set_ylabel("Value")
    ax.legend()

    plt.show()

def runSimulation():
    N = int(entryAgents.get()) #liczba wszystkich agentów
    S = int(entrySAgents.get()) #liczba s-agentów
    C = int(entryCycles.get()) #liczba cykli
    kMin = int(entryKMin.get())
    kMax = int(entryKMax.get())
    ExpoA = float(entryExpoA.get())
    ExpoG = float(entryExpoG.get())
    x = float(entryX.get())
    y = float(entryY.get())
    z = float(entryZ.get())
    V0 = 1
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
        sumPHToS = 0.0 
        numberHJS = 0 
        sumPSToH = 0.0  
        numberSJH = 0 
        counterSSCoop = 0
        counterAllCoop = 0
        adj = {}

        for adjI in range(N):
            adj[adjI] = []

        # Parowanie kleintów z dostawca
        for iN in range(N):
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

            for j in range(N):
                vRepo = V0 if cycle == 0 else data[cycle - 1].V[j]
                L = Policy.hStep(vRepo, x)
                p = Policy.sBiasP(y, L) if iN in sAgent else L 
                if iN in sAgent and j in sAgent:
                    p = 1.0
                policyP = Policy.providerPolicy(Policy.randExpoD(ExpoA), p)

                L = Policy.hStep(vProv, x)
                r = Policy.sBiasR(z, L) if client in sAgent else L
                if iN in sAgent and j in sAgent:
                    r = 1.0
                policyR = Policy.reporterPolicy(Policy.randExpoD(ExpoG), policyP, r)
                meanPolicyR += policyR * vProv

                if iN in sAgent and j in sAgent: 
                    counterSSCoop += 1
                
                counterAllCoop += 1

                if iN in sAgent:
                    if j not in sAgent:
                        sumPSToH += policyP
                else:
                    if j in sAgent:
                        sumPHToS += policyP
            
            meanPolicyR /= numClients
            agentsR[iN] = meanPolicyR
        

        sortedByR = {k: v for k, v in sorted(agentsR.items(), key=lambda x: x[1])}

        meanRHigherSet = 0.0
        meanRLowerSet = 0.0
        iter = 0
        
        for value in sortedByR.values():
            if iter < len(sortedByR) // 2:
                meanRLowerSet += value
            else:
                meanRHigherSet += value
            iter += 1

        meanRHigherSet /= len(sortedByR) // 2
        meanRLowerSet /= len(sortedByR) // 2

        print(f'meanRHigherSet: {meanRHigherSet}, meanRLowerSet: {meanRLowerSet}')

        meanRLowerSet /= meanRHigherSet
        meanRHigherSet /= meanRHigherSet

        V = [0.0] * N
        iter = 0

        for key in sortedByR.keys():
            if iter < len(sortedByR) // 2:
                V[key] = meanRLowerSet
            else:
                V[key] = meanRHigherSet
            iter += 1

        meanVs = 0.0
        meanVh = 0.0

        for it in range(N):
            if it in sAgent:
                meanVs += V[it]
            else:
                meanVh += V[it]

        meanVh /= N - S
        meanVs /= S

        netOutFlow = (sumPHToS / numberHJS) - (sumPSToH / numberSJH)

        data.append(Cycle(V, meanVs, meanVh, netOutFlow))

        time.sleep(0.01)
        print(f'netOutflow: {netOutFlow}, sumPHToS: {sumPHToS}', end=' ')
        print(f'numberHJS: {numberHJS}, sumPSToH: {sumPSToH}, numberSJH: {numberSJH}')
        print(f'meanRHigherSet: {meanRHigherSet}, meanRLowerSet: {meanRLowerSet}')
        print(f'meanVs: {meanVs}, meanVh: {meanVh}')

        # print('Progres: ', (cycle + 1) / cycle * 100, end='\n\n')

    print(data)
    series = [
        ("meanVh", [cycle.meanVh for cycle in data]),
        ("meanVs", [cycle.meanVs for cycle in data]),
        ("netOutflow", [cycle.netOutFlow for cycle in data])
    ]

    plot_on_frame(series)


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

labelX = Label(window, 
                    text="x", 
                    font=('Arial', 9, 'bold'), 
                    fg="white", 
                    background="#202124")

labelY = Label(window, 
                    text="y", 
                    font=('Arial', 9, 'bold'), 
                    fg="white", 
                    background="#202124")

labelZ = Label(window, 
                    text="z", 
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
labelX.place(x=260, y=110)
labelY.place(x=260, y=140)
labelZ.place(x=260, y=170)

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

entryX = Entry(window,
                    font=('Arial', 9))    

entryY = Entry(window,
                    font=('Arial', 9))    

entryZ = Entry(window,
                    font=('Arial', 9))     
   
entryAgents.insert(0, "1000")
entrySAgents.insert(0, "150")
entryCycles.insert(0, "100")
entryKMin.insert(0, "50")
entryKMax.insert(0, "150")
entryExpoA.insert(0, "0.5")
entryExpoG.insert(0, "0.5")
entryX.insert(0, "0.1")
entryY.insert(0, "0.1")
entryZ.insert(0, "0.1")

entryAgents.place(x=100, y=50)
entrySAgents.place(x=100, y=80)
entryCycles.place(x=100, y=110)
entryKMin.place(x=100, y=140)
entryKMax.place(x=100, y=170)
entryExpoA.place(x=340, y=50)
entryExpoG.place(x=340, y=80)
entryX.place(x=340, y=110)
entryY.place(x=340, y=140)
entryZ.place(x=340, y=170)

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
