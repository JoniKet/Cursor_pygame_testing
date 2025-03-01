import pygame
import math
import random
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
        SCREEN_WIDTH, SCREEN_HEIGHT, BIRD_WIDTH, BIRD_HEIGHT,
        BIRD_RADIUS, ROTATION_SPEED, SHOOT_COOLDOWN, BIRD_COLOR,
        BIRD_THOUGHTS
    )
except ImportError:
    # Fall back to local import for direct execution
    from src.constants import (
        SCREEN_WIDTH, SCREEN_HEIGHT, BIRD_WIDTH, BIRD_HEIGHT,
        BIRD_RADIUS, ROTATION_SPEED, SHOOT_COOLDOWN, BIRD_COLOR,
        BIRD_THOUGHTS
    )

class Bird:
    """Bird class that represents the player character"""
    
    def __init__(self, x, y, assets):
        """Initialize bird position and assets"""
        self.x = x
        self.y = y
        self.assets = assets
        self.original_image = assets.get_image('bird')
        # Resize image if needed
        self.original_image = pygame.transform.scale(self.original_image, (BIRD_WIDTH, BIRD_HEIGHT))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        
        # Bird rotation attributes
        self.angle = 0  # In degrees, 0 is right, 90 is down
        
        # Thinking timer and messages
        self.thinking_timer = 0
        self.thinking_delay = 180  # Reduced from 300 to show thoughts more frequently
        self.current_thought = None
        self.thoughts = BIRD_THOUGHTS  # Use the thoughts from constants
        self.font = pygame.font.Font(None, 24)  # Increased font size from 20 to 24
        
    def update(self, target_angle=None):
        """Update bird state"""
        # Update rotation if target_angle provided
        if target_angle is not None:
            # Smooth rotation towards target
            angle_diff = (target_angle - self.angle) % 360
            if angle_diff > 180:
                angle_diff -= 360
            
            # Limit rotation speed
            rotation_speed = 5
            if abs(angle_diff) > rotation_speed:
                if angle_diff > 0:
                    self.angle += rotation_speed
                else:
                    self.angle -= rotation_speed
            else:
                self.angle = target_angle
                
            # Keep angle between 0-360
            self.angle %= 360
        
        # Rotate the bird image
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        # Thinking logic
        self.thinking_timer += 1
        if self.thinking_timer >= self.thinking_delay:
            self.thinking_timer = 0
            # 50% chance to show a thought (increased from 30%)
            if pygame.time.get_ticks() % 10 < 5:
                self.current_thought = random.choice(self.thoughts)
            else:
                self.current_thought = None
                
    def draw(self, screen):
        """Draw the bird on the screen"""
        screen.blit(self.image, self.rect)
        
        # Draw thought bubble if there's a current thought
        if self.current_thought:
            thought_surface = self.font.render(self.current_thought, True, (0, 0, 0))
            thought_rect = thought_surface.get_rect()
            
            # Position thought bubble above the bird
            bubble_x = self.x - thought_rect.width // 2
            bubble_y = self.y - 70  # Position slightly higher
            
            # Determine bubble color based on thought content
            bubble_color = (245, 245, 255)  # Default light color
            border_color = (100, 100, 150)  # Default border
            
            # Check for keywords to determine the emotion/tone of the thought
            if any(word in self.current_thought.lower() for word in ["pain", "suffer", "villain", "remorse"]):
                # Sad/guilty thoughts - blue tint
                bubble_color = (220, 220, 255)
                border_color = (80, 80, 180)
            elif any(word in self.current_thought.lower() for word in ["purpose", "meaning", "why", "what"]):
                # Philosophical thoughts - purple tint
                bubble_color = (240, 220, 255)
                border_color = (150, 100, 180)
            elif any(word in self.current_thought.lower() for word in ["exist", "consciousness", "real", "illusion"]):
                # Existential thoughts - yellow tint
                bubble_color = (255, 255, 220)
                border_color = (180, 180, 100)
            
            # Draw thought bubble background
            padding = 8  # Increased padding
            bubble_rect = pygame.Rect(
                bubble_x - padding,
                bubble_y - padding,
                thought_rect.width + padding * 2,
                thought_rect.height + padding * 2
            )
            # Draw bubble with determined color
            pygame.draw.rect(screen, bubble_color, bubble_rect, border_radius=12)
            pygame.draw.rect(screen, border_color, bubble_rect, width=2, border_radius=12)
            
            # Draw connecting dots
            dot_sizes = [4, 6, 8]  # Slightly larger dots
            for i, size in enumerate(dot_sizes):
                dot_x = self.x - size // 2
                dot_y = self.y - 25 - (i * 12)
                pygame.draw.circle(screen, bubble_color, (dot_x, dot_y), size)
                pygame.draw.circle(screen, border_color, (dot_x, dot_y), size, width=1)
            
            # Draw thought text
            screen.blit(thought_surface, (bubble_x, bubble_y)) 