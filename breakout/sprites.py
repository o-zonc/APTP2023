import random
from setting import *
import setting.chroma


class paddle:
    def __init__(self):
        self.width = 100
        self.height = 20
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 50
        self.speed = 30

    def squeeze(self, multiplier):
        if (self.width > WIDTH / 3):
            if (multiplier < 1):
                return
        self.width /= multiplier


class ball:
    def __init__(self):
        self.width = 20
        self.height = 20
        self.x = random.randint(self.width, WIDTH - self.width)
        self.y = HEIGHT // 2 - self.height // 2
        self.speed_x = random.choice([-5, 5])
        self.speed_y = 5

    def speedup(self, multiplier):
        if (abs(self.speed_x) < 1 or abs(self.speed_y) < 1):
            if (multiplier < 1):
                return
        self.speed_x *= multiplier
        self.speed_y *= multiplier


class brick:
    def __init__(self):
        self.width = 75
        self.height = 20
        self.gap = 5
        self.colors = setting.chroma.default
