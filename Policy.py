import random

class Policy:
    @staticmethod
    def hStep(v, x):
        return 1.0 if v >= 1 - x else .0

    @staticmethod  
    def sBiasP(y, L):
        return min(y, L)

    @staticmethod
    def sBiasR(z, L):
        return min(z, L)

    @staticmethod
    def providerPolicy(A, p):
        return min(A, p)
    
    @staticmethod
    def reporterPolicy(G, P, r):
        return min(G*P, r)

    @staticmethod
    def randExpoD(expo): 
        return pow(random.random(), 1.0 / expo)