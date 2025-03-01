import pygame
import math
import os
import sys
import random

# Add parent directory to path for direct execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    # Try importing with full package path first (when run through main launcher)
    from games.Questioning_bird.src.constants import PIG_WIDTH, PIG_HEIGHT
except ImportError:
    # Fall back to local import for direct execution
    from src.constants import PIG_WIDTH, PIG_HEIGHT

class Pig:
    """Pig class that represents enemies moving toward the bird"""
    
    def __init__(self, x, y, target_x, target_y, speed, assets):
        """Initialize pig with position, target, and movement speed"""
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed
        self.assets = assets
        
        # Set up the image
        self.original_image = assets.get_image('pig')
        # Resize image if needed
        self.original_image = pygame.transform.scale(self.original_image, (PIG_WIDTH, PIG_HEIGHT))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        
        # Calculate movement direction to target
        self.calculate_direction()
        
        # Rotation angle
        self.angle = 0
        
    def calculate_direction(self):
        """Calculate movement direction vector toward target"""
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        
        # Calculate direction angle
        self.angle = math.degrees(math.atan2(dy, dx))
        
        # Normalize the direction vector
        distance = math.sqrt(dx*dx + dy*dy)
        if distance > 0:
            self.dx = dx / distance * self.speed
            self.dy = dy / distance * self.speed
        else:
            self.dx = 0
            self.dy = 0
            
    def update(self):
        """Update pig position and rotation"""
        # Move toward target
        self.x += self.dx
        self.y += self.dy
        
        # Recalculate direction periodically (every ~1 second at 60fps)
        if random.randint(0, 59) == 0:
            self.calculate_direction()
        
        # Rotate the image to face movement direction
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
    def draw(self, screen):
        """Draw the pig on the screen"""
        screen.blit(self.image, self.rect) 