import pygame
import os
import math

def create_background():
    WIDTH = 1200
    HEIGHT = 800
    
    # Create the surface
    surface = pygame.Surface((WIDTH, HEIGHT))
    
    # Draw sky gradient
    for y in range(HEIGHT-50):
        # Create a nice blue gradient for the sky
        progress = y / (HEIGHT-50)
        blue = int(235 * (1 - progress * 0.5))  # Darker blue at bottom
        green = int(206 * (1 - progress * 0.3))
        red = int(135 * (1 - progress * 0.2))
        color = (red, green, blue)
        pygame.draw.line(surface, color, (0, y), (WIDTH, y))
    
    # Draw clouds
    for i in range(5):
        x = (WIDTH / 5) * i + 100
        y = 100 + (i % 2) * 50
        # Draw multiple white circles for each cloud
        for dx in range(-20, 21, 20):
            pygame.draw.circle(surface, (255, 255, 255), (int(x + dx), int(y)), 30)
            pygame.draw.circle(surface, (255, 255, 255), (int(x + dx/2), int(y - 20)), 25)
    
    # Draw mountains in the background
    mountain_color = (101, 67, 33)  # Brown
    for i in range(5):
        x1 = (WIDTH / 4) * i - 100
        x2 = x1 + 300
        x3 = (x1 + x2) / 2
        y1 = HEIGHT - 50
        y2 = HEIGHT - 50
        y3 = HEIGHT - 200 - (i % 2) * 100
        pygame.draw.polygon(surface, mountain_color, [(x1, y1), (x2, y2), (x3, y3)])
    
    # Draw ground
    ground_rect = pygame.Rect(0, HEIGHT-50, WIDTH, 50)
    pygame.draw.rect(surface, (34, 139, 34), ground_rect)  # Forest green
    
    # Add some grass details
    for i in range(0, WIDTH, 30):
        grass_height = 10 + (i % 3) * 5
        grass_color = (0, 100 + (i % 3) * 20, 0)
        pygame.draw.line(surface, grass_color, 
                        (i, HEIGHT-50),
                        (i, HEIGHT-50-grass_height), 2)
    
    # Save the background
    pygame.image.save(surface, 'assets/background.png')

if __name__ == '__main__':
    pygame.init()
    create_background()
    pygame.quit() 