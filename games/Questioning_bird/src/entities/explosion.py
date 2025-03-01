import pygame
import os
import sys

# Add parent directory to path for direct execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

class Explosion:
    """Explosion effect when a pig is hit by a bullet"""
    
    def __init__(self, x, y, assets):
        """Initialize explosion at the given position"""
        self.x = x
        self.y = y
        self.assets = assets
        self.frame = 0
        self.max_frames = 8  # Number of animation frames
        self.frame_delay = 3  # Frames to wait before advancing animation
        self.frame_counter = 0
        self.is_active = True
        
        # Get explosion image
        try:
            self.image = assets.get_image('explosion')
            # Scale if necessary
            self.image = pygame.transform.scale(self.image, (50, 50))
        except:
            # Fallback if no explosion image
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))  # Red square as fallback
            
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self):
        """Update explosion animation"""
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.frame += 1
            
            # Scale image based on frame for expanding effect
            scale_factor = 1.0 + (self.frame * 0.2)
            size = int(50 * scale_factor)
            
            # Also decrease opacity over time
            self.alpha = 255 - int((self.frame / self.max_frames) * 255)
            
            if self.frame >= self.max_frames:
                self.is_active = False
            else:
                try:
                    # Recreate image with new size and opacity
                    image = self.assets.get_image('explosion')
                    image = pygame.transform.scale(image, (size, size))
                    image.set_alpha(self.alpha)
                    self.image = image
                    self.rect = self.image.get_rect(center=(self.x, self.y))
                except:
                    # Fallback
                    self.image = pygame.Surface((size, size), pygame.SRCALPHA)
                    pygame.draw.circle(self.image, (255, 100, 0, self.alpha), 
                                     (size // 2, size // 2), size // 2)
                    self.rect = self.image.get_rect(center=(self.x, self.y))
                
    def draw(self, screen):
        """Draw the explosion on the screen"""
        if self.is_active:
            screen.blit(self.image, self.rect) 