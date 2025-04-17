import math
import random

class ButterflyRandom:
    def __init__(self, seed=None):
        self.seed = seed or random.random()

    def random(self):
        self.seed = math.sin(self.seed * 12.9898) * 43758.5453
        return self.seed - int(self.seed)

    def randint(self, a, b):
        return int(self.random() * (b - a + 1)) + a
