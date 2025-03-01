import random
import math
import pygame
from ..constants import RED, YELLOW, ORANGE

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 10)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.lifetime = random.randint(20, 40)
        self.color = random.choice([RED, YELLOW, ORANGE])
        self.size = random.randint(2, 6)
        
    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.5  # Gravity effect
        self.lifetime -= 1
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

class VictorySparkle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 3)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.lifetime = random.randint(30, 60)
        self.color = random.choice([(255, 215, 0), (255, 255, 0), (255, 255, 255)])  # Gold, Yellow, White
        self.size = random.randint(2, 4)
        
    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += 0.1  # Gentle gravity
        self.lifetime -= 1
        
    def draw(self, screen):
        if self.lifetime > 0:
            alpha = min(255, self.lifetime * 8)
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size) 