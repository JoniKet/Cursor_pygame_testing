import pygame
import math
import os
import sys

# Add parent directory to path for direct execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    # Try importing with full package path first (when run through main launcher)
    from games.Questioning_bird.src.constants import (
        SCREEN_WIDTH, SCREEN_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT,
        BULLET_RADIUS, BULLET_SPEED
    )
except ImportError:
    # Fall back to local import for direct execution
    from src.constants import (
        SCREEN_WIDTH, SCREEN_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT,
        BULLET_RADIUS, BULLET_SPEED
    )

class Bullet:
    """Bullet class that represents projectiles fired by the bird"""
    
    def __init__(self, x, y, angle, assets):
        """Initialize bullet with position and direction angle"""
        self.x = x
        self.y = y
        self.angle = angle  # Direction angle in degrees, 0 is right, 90 is down
        self.speed = BULLET_SPEED
        self.assets = assets
        
        # Calculate velocity components based on angle
        angle_rad = math.radians(angle)
        self.dx = math.cos(angle_rad) * self.speed
        self.dy = math.sin(angle_rad) * self.speed
        
        # Set up the image
        self.original_image = assets.get_image('bullet')
        # Resize image if needed
        self.original_image = pygame.transform.scale(self.original_image, (BULLET_WIDTH, BULLET_HEIGHT))
        # Rotate image to match the angle
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self):
        """Update bullet position"""
        # Move bullet according to direction
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x, self.y)
        
    def draw(self, screen):
        """Draw the bullet on the screen"""
        screen.blit(self.image, self.rect) 