import random
import math 

class KMeans:

    def __init__(self, cycles, data, k):
        self.cycles = cycles
        self.data = data 
        self.k = k
        self.centroids = []
        self.result = []
        for x in range(k):
            kNumber = "Group" + str(x + 1)
            self.result.append({
                'index': kNumber,
                'data': []
            })

    def group(self):
        for x in range(self.k):
            self.drawCentroid()
        
        for point in self.data:
            count = 0
            centroidIndex = 0
            minDistance = float('inf')
            for centroid in self.centroids:
                distance = self.countEuclidesDistance(centroid, point)
                if distance < minDistance:
                    minDistance = distance
                    centroidIndex = count
                count += 1
            self.result[centroidIndex]['data'].append(point)

        return self.result

    def drawCentroid(self):
        randomIndex = random.randrange(0, len(self.data))
        for centroid in self.centroids:
            if centroid == self.data[randomIndex]:
                return self.drawCentroid()

        self.centroids.append(self.data[randomIndex])

    def countEuclidesDistance(self, point1, point2):
        distance = 0
        for x in range(len(point1)):
            distance += pow(point2[x] - point1[x], 2)
        return math.sqrt(distance)

        




