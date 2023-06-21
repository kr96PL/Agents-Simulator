import sys
import random
import collections
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tkinter import *
from sklearn.cluster import KMeans
import numpy as np
from DataGenerator import *
from Policy import *
from Cycle import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import csv

window = Tk() 
window.geometry("1100x600")
window.title("Agents Simulator")
window.config(background="#202124")
DATA = collections.deque([])

def saveToCsv(series, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Cycle'] + [name for name, _ in series])  

        n = len(series[0][1])
        x_values = list(range(1, n + 1))

        for i in range(n):
            row = [x_values[i]] + [values[i] for _, values in series]
            writer.writerow(row)

def generateSAgents(agents, sAgents):
    sAgentList = [0] * agents

    indexes = random.sample(range(agents), sAgents)
    
    for index in indexes:
        sAgentList[index] = 1

    return sAgentList

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
    DATA.clear()
    N = int(entryAgents.get()) #liczba wszystkich agentów
    S = int(entrySAgents.get()) #liczba s-agentów
    C = int(entryCycles.get()) #liczba cykli
    kMin = int(entryKMin.get())
    kMax = int(entryKMax.get())
    expoA = float(entryExpoA.get())
    expoG = float(entryExpoG.get())
    x = float(entryX.get())
    y = float(entryY.get())
    z = float(entryZ.get())
    V0 = 1
    sAgentList = generateSAgents(N, S)

    for cycle in range(C):
        sumPhToS = 0.0
        numberHjs = 0
        sumPsToH = 0.0
        numberSjh = 0
        counterSsCoop = 0
        counterAllCoop = 0

        adj = [[0] * N for _ in range(N)]

        for i in range(N):
            clients = random.randint(kMin, kMax + 1)
            in_j = 0
            while in_j < clients:
                rn = random.randint(0, N - 1)
                if rn != i and adj[i][rn] != 1:
                    adj[i][rn] = 1
                    if sAgentList[i] == 1:
                        if sAgentList[rn] != 1:
                            numberSjh += 1
                    else:
                        if sAgentList[rn] == 1:
                            numberHjs += 1
                    in_j += 1

        agentsR = {}

        for it in range(N):
            clients = adj[it]
            v_prov = V0 if cycle == 0 else DATA[cycle - 1].V[it]
            num_clients = clients.count(1)
            mean_policy_r = 0.0

            for j in range(N):
                if adj[it][j] == 1:
                    v_repo = V0 if cycle == 0 else DATA[cycle - 1].V[j]
                    l = Policy.hStep(v_repo, x)
                    p = Policy.sBiasP(y, l) if sAgentList[it] == 1 else l
                    if sAgentList[it] == 1 and sAgentList[j] == 1:
                        p = 1.0
                    policy_p = Policy.providerPolicy(Policy.randExpoD(expoA), p)
                    l = Policy.hStep(v_prov, x)
                    r = Policy.sBiasR(z, l) if sAgentList[j] == 1 else l
                    if sAgentList[it] == 1 and sAgentList[j] == 1:
                        r = 1.0

                    policy_r = Policy.reporterPolicy(Policy.randExpoD(expoG), policy_p, r)
                    mean_policy_r += policy_r * v_prov
                    if sAgentList[it] == 1 and sAgentList[j] == 1:
                        counterSsCoop += 1
                    counterAllCoop += 1
                    if sAgentList[it] == 1:
                        if sAgentList[j] != 1:
                            sumPsToH += policy_p
                    else:
                        if sAgentList[j] == 1:
                            sumPhToS += policy_p

            mean_policy_r /= num_clients
            agentsR[it] = mean_policy_r


        formatDataKMeans = []

        for iR in range(len(agentsR)):
            formatDataKMeans.append([agentsR[iR], 1])

        kmeans = KMeans(n_clusters=2, random_state=42)
        kmeans.fit(formatDataKMeans)
        labels = kmeans.predict(formatDataKMeans)

        print("cycle " + str(cycle), labels)

        meanRHigherSet = 0.0
        meanRLowerSet = 0.0
        c1 = 0
        c0 = 0
        for x in range(len(labels)):
            if labels[x] == 1:
                meanRHigherSet += agentsR[x] 
                c1 += 1
            else:
                meanRLowerSet += agentsR[x]
                c0 += 1

    
        meanRHigherSet /= c1
        meanRLowerSet /= c0

        swap = False
        if meanRHigherSet < meanRLowerSet:
            tmp = meanRLowerSet
            meanRLowerSet = meanRHigherSet
            meanRHigherSet = tmp
            swap = True

        print(f'meanRHigherSet: {meanRHigherSet}, meanRLowerSet: {meanRLowerSet}')

        meanRLowerSet /= meanRHigherSet
        meanRHigherSet /= meanRHigherSet

        print(meanRLowerSet)
        print(meanRHigherSet)

        V = [0.0] * N

        iter = 0
        for label in labels:
            if label == 1:
                if swap:
                    V[iter] = meanRLowerSet
                else:
                    V[iter] = meanRHigherSet
            else:
                if swap:
                    V[iter] = meanRHigherSet
                else:
                    V[iter] = meanRLowerSet
            iter += 1

        meanVs = 0.0
        meanVh = 0.0

        for it in range(N):
            if sAgentList[it] == 1:
                meanVs += V[it]
            else:
                meanVh += V[it]

        meanVh /= N - S
        meanVs /= S

        netOutFlow = (sumPhToS / numberHjs) - (sumPsToH / numberSjh)

        DATA.append(Cycle(V, meanVs, meanVh, netOutFlow))

        time.sleep(0.01)
        print(f'netOutflow: {netOutFlow}, sumPHToS: {sumPhToS}', end=' ')
        print(f'numberHJS: {numberHjs}, sumPSToH: {sumPsToH}, numberSJH: {numberSjh}')
        print(f'meanRHigherSet: {meanRHigherSet}, meanRLowerSet: {meanRLowerSet}')
        print(f'meanVs: {meanVs}, meanVh: {meanVh}')

        print('Progres: ', (cycle + 1) / C * 100, end='\n\n')

    series = [
        ("meanVh", [cycle.meanVh for cycle in DATA]),
        ("meanVs", [cycle.meanVs for cycle in DATA]),
        ("netOutflow", [cycle.netOutFlow for cycle in DATA])
    ]

    saveToCsv(series, 'data.csv')
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
entryExpoA.insert(0, "10")
entryExpoG.insert(0, "10")
entryX.insert(0, "0.8")
entryY.insert(0, "0.8")
entryZ.insert(0, "0.8")

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
