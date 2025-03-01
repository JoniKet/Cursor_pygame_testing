import random
import math
import pygame
from .particle import VictorySparkle
from ..constants import WHITE

class VictoryEffect:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.sparkles = []
        self.time = 0
        self.font = pygame.font.Font(None, 120)
        self.small_font = pygame.font.Font(None, 48)
        
    def update(self):
        self.time += 1
        
        # Add new sparkles
        if self.time % 2 == 0:  # Add sparkles every other frame
            for _ in range(3):  # Add 3 sparkles at a time
                x = random.randint(0, self.width)
                y = random.randint(0, self.height)
                self.sparkles.append(VictorySparkle(x, y))
        
        # Update existing sparkles
        for sparkle in self.sparkles[:]:
            sparkle.update()
            if sparkle.lifetime <= 0:
                self.sparkles.remove(sparkle)
                
    def draw(self, screen, score):
        # Draw all sparkles
        for sparkle in self.sparkles:
            sparkle.draw(screen)
            
        # Draw shining victory text with pulsing effect
        scale = 1.0 + 0.1 * math.sin(self.time * 0.1)  # Pulsing scale
        
        # Main victory text
        text = self.font.render("YOU'RE A WINNER!", True, (255, 215, 0))  # Gold color
        text = pygame.transform.rotozoom(text, 0, scale)
        rect = text.get_rect(center=(self.width//2, self.height//2))
        screen.blit(text, rect)
        
        # Score text
        score_text = self.small_font.render(f"Final Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(self.width//2, self.height//2 + 80))
        screen.blit(score_text, score_rect)
        
        # Press ESC text
        esc_text = self.small_font.render("Press ESC to return to menu", True, WHITE)
        esc_rect = esc_text.get_rect(center=(self.width//2, self.height//2 + 140))
        screen.blit(esc_text, esc_rect) 