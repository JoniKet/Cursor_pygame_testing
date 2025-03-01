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
        BULLET_RADIUS, BULLET_SPEED, SPECIAL_BULLET_GROWTH_RATE,
        SPECIAL_BULLET_MAX_SIZE
    )
except ImportError:
    # Fall back to local import for direct execution
    from src.constants import (
        SCREEN_WIDTH, SCREEN_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT,
        BULLET_RADIUS, BULLET_SPEED, SPECIAL_BULLET_GROWTH_RATE,
        SPECIAL_BULLET_MAX_SIZE
    )

class SpecialBullet:
    """Special bullet class for the angry bird's attack on the player"""
    
    def __init__(self, x, y, assets):
        """Initialize special bullet that grows and targets the player"""
        self.x = x
        self.y = y
        self.assets = assets
        self.angle = 270  # Straight up initially
        self.speed = BULLET_SPEED * 0.5  # Slower than regular bullets
        
        # Calculate initial velocity (straight up)
        angle_rad = math.radians(self.angle)
        self.dx = math.cos(angle_rad) * self.speed
        self.dy = math.sin(angle_rad) * self.speed
        
        # Set up the image with a red glow effect
        self.original_image = assets.get_image('bullet')
        self.width = BULLET_WIDTH * 2  # Start larger than normal bullets
        self.height = BULLET_HEIGHT * 2
        self.scale_factor = 1.0
        
        # Create a glowing effect
        self.create_glowing_bullet()
        
        # Initialize rect
        self.rect = self.image.get_rect(center=(x, y))
        
        # Growth tracking
        self.growth_rate = SPECIAL_BULLET_GROWTH_RATE
        self.max_size = SPECIAL_BULLET_MAX_SIZE
        self.current_size = max(self.width, self.height)
        
        # Phase tracking
        self.phase = "rising"  # rising, falling, growing
        self.rise_height = SCREEN_HEIGHT * 0.3  # Rise to 30% of screen height
        self.initial_y = y
        self.target_y = y - self.rise_height
        
        # Sound timers
        self.sound_timer = 0
        self.sound_interval = 30  # Frames between sounds during growing phase
        
        # Play initial launch sound
        self.assets.play_sound('shoot', volume=0.8)
        
    def create_glowing_bullet(self):
        """Create a glowing bullet effect"""
        # Create a larger surface for the glow
        glow_size = int(max(self.width, self.height) * 1.5)
        glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        
        # Draw outer glow (semi-transparent)
        center = glow_size // 2
        for radius in range(glow_size // 2, 0, -2):
            alpha = 150 if radius > glow_size // 3 else 255
            color = (255, 100, 50, alpha)  # Orange-red with alpha
            pygame.draw.circle(glow_surface, color, (center, center), radius)
        
        # Draw core (solid)
        pygame.draw.circle(glow_surface, (255, 50, 0), (center, center), glow_size // 4)
        
        # Scale to current size
        self.image = pygame.transform.scale(glow_surface, (int(self.width), int(self.height)))
        
    def update(self):
        """Update special bullet position and size"""
        if self.phase == "rising":
            # Move upward
            self.y += self.dy
            if self.y <= self.target_y:
                self.phase = "falling"
                # Change direction to fall back down
                self.dy = -self.dy * 0.5  # Slower fall
                # Play sound for phase change
                self.assets.play_sound('shoot', volume=0.6)
        
        elif self.phase == "falling":
            # Fall back down
            self.y += self.dy
            if self.y >= self.initial_y:
                self.phase = "growing"
                self.dy = 0  # Stop vertical movement
                # Start at center of screen horizontally
                self.x = SCREEN_WIDTH // 2
                self.y = SCREEN_HEIGHT // 2
                # Play sound for phase change
                self.assets.play_sound('special_attack', volume=0.7)
        
        elif self.phase == "growing":
            # Grow in size
            self.scale_factor *= self.growth_rate
            self.width *= self.growth_rate
            self.height *= self.growth_rate
            self.current_size = max(self.width, self.height)
            
            # Play growing sound at intervals
            self.sound_timer += 1
            if self.sound_timer >= self.sound_interval:
                self.sound_timer = 0
                # Increase volume as the bullet grows
                volume = min(1.0, 0.5 + (self.current_size / self.max_size) * 0.5)
                # Alternate between sounds for variety
                if self.current_size < self.max_size * 0.5:
                    self.assets.play_sound('special_attack', volume=volume)
                else:
                    # Use explosion sound as it gets bigger
                    self.assets.play_sound('explosion', volume=volume)
            
            # Recreate the image at the new size
            self.create_glowing_bullet()
            
            # Check if we're about to reach max size
            if self.current_size >= self.max_size * 0.9 and self.current_size < self.max_size:
                # Play final explosion sound as we approach max size
                self.assets.play_sound('game_over', volume=1.0)
        
        # Update rect position
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
    def is_done(self):
        """Check if the bullet has reached its maximum size"""
        return self.current_size >= self.max_size
        
    def draw(self, screen):
        """Draw the special bullet on the screen"""
        screen.blit(self.image, self.rect) 