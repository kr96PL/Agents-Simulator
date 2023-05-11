import random

class DataGenerator:
    def generate(self, amount, minV, maxV):
        data = []
        for x in range(amount):
            data.append([
                random.uniform(minV, maxV),
                random.uniform(minV, maxV)
            ])
        return data