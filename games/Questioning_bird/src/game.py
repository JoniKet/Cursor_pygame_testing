import pygame
import random
import os
import sys
import math

# Add parent directory to path for direct execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    # Try importing with full package path first (when run through main launcher)
    from games.Questioning_bird.src.constants import (
        SCREEN_WIDTH, SCREEN_HEIGHT, BIRD_WIDTH, BIRD_HEIGHT,
        PIG_WIDTH, PIG_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT,
        MAX_PIGS, MAX_BULLETS, STATE_GAME_OVER
    )
    from games.Questioning_bird.src.entities.bird import Bird
    from games.Questioning_bird.src.entities.pig import Pig
    from games.Questioning_bird.src.entities.bullet import Bullet
    from games.Questioning_bird.src.entities.explosion import Explosion
except ImportError:
    # Fall back to local import for direct execution
    from constants import (
        SCREEN_WIDTH, SCREEN_HEIGHT, BIRD_WIDTH, BIRD_HEIGHT,
        PIG_WIDTH, PIG_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT,
        MAX_PIGS, MAX_BULLETS, STATE_GAME_OVER
    )
    from entities.bird import Bird
    from entities.pig import Pig
    from entities.bullet import Bullet
    from entities.explosion import Explosion

class Game:
    """Main game class that handles the core gameplay"""
    
    def __init__(self, assets):
        """Initialize the game state"""
        self.assets = assets
        # Place bird in the center of the screen
        self.bird = Bird(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, assets)
        self.pigs = []
        self.bullets = []
        self.explosions = []
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.next_state = None
        
        # Create background (ground view)
        self.background = self.create_background()
        
        # Auto-shoot timer
        self.shoot_timer = 0
        self.shoot_delay = 45  # frames between shots
        
    def create_background(self):
        """Create a top-down ground view background"""
        # Create ground
        ground = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        ground.fill((76, 153, 0))  # Green grass
        
        # Add some ground details
        for _ in range(20):
            # Add random patches of darker grass
            patch_size = random.randint(20, 50)
            patch_x = random.randint(0, SCREEN_WIDTH - patch_size)
            patch_y = random.randint(0, SCREEN_HEIGHT - patch_size)
            pygame.draw.ellipse(ground, (60, 120, 0), (patch_x, patch_y, patch_size, patch_size))
            
        for _ in range(15):
            # Add random patches of lighter grass
            patch_size = random.randint(10, 30)
            patch_x = random.randint(0, SCREEN_WIDTH - patch_size)
            patch_y = random.randint(0, SCREEN_HEIGHT - patch_size)
            pygame.draw.ellipse(ground, (100, 180, 20), (patch_x, patch_y, patch_size, patch_size))
            
        # Add some rocks/stones
        for _ in range(8):
            stone_size = random.randint(5, 15)
            stone_x = random.randint(0, SCREEN_WIDTH - stone_size)
            stone_y = random.randint(0, SCREEN_HEIGHT - stone_size)
            pygame.draw.ellipse(ground, (128, 128, 128), (stone_x, stone_y, stone_size, stone_size))
            
        return ground
    
    def create_bullet(self):
        """Create a new bullet in the direction the bird is facing"""
        if len(self.bullets) < MAX_BULLETS:
            # Calculate bullet direction based on bird's angle
            angle_rad = math.radians(self.bird.angle)
            start_x = self.bird.x + math.cos(angle_rad) * (BIRD_WIDTH // 2)
            start_y = self.bird.y + math.sin(angle_rad) * (BIRD_HEIGHT // 2)
            
            bullet = Bullet(start_x, start_y, self.bird.angle, self.assets)
            self.bullets.append(bullet)
            self.assets.play_sound('shoot')
    
    def add_pig(self, x, y):
        """Add a new pig at the specified position, moving toward the bird"""
        if len(self.pigs) < MAX_PIGS:
            # Random speed between min and max
            speed = random.uniform(1, 3)
            pig = Pig(x, y, self.bird.x, self.bird.y, speed, self.assets)
            self.pigs.append(pig)
            
    def update(self):
        """Update the game state"""
        # Update bird and rotate toward nearest pig
        if self.pigs:
            # Find the nearest pig
            nearest_pig = min(self.pigs, key=lambda pig: 
                math.sqrt((pig.x - self.bird.x)**2 + (pig.y - self.bird.y)**2))
            
            # Calculate angle to the nearest pig
            dx = nearest_pig.x - self.bird.x
            dy = nearest_pig.y - self.bird.y
            target_angle = math.degrees(math.atan2(dy, dx))
            
            # Update bird with target angle
            self.bird.update(target_angle)
        else:
            # If no pigs, just update normally
            self.bird.update()
        
        # Auto-shoot logic
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            self.create_bullet()
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            # Remove bullets that are off-screen
            if (bullet.x < 0 or bullet.x > SCREEN_WIDTH or
                bullet.y < 0 or bullet.y > SCREEN_HEIGHT):
                self.bullets.remove(bullet)
        
        # Update pigs
        for pig in self.pigs[:]:
            # Update pig movement toward bird
            pig.update()
            
            # Check if pig reached the bird
            distance = math.sqrt((pig.x - self.bird.x)**2 + (pig.y - self.bird.y)**2)
            if distance < (BIRD_WIDTH + PIG_WIDTH) // 4:  # Using half-width for more accurate collision
                # Game over if pig reaches bird
                self.next_state = STATE_GAME_OVER
                return
        
        # Check for collisions between bullets and pigs
        for bullet in self.bullets[:]:
            for pig in self.pigs[:]:
                # Distance-based collision for circular objects
                distance = math.sqrt((bullet.x - pig.x)**2 + (bullet.y - pig.y)**2)
                if distance < (BULLET_WIDTH + PIG_WIDTH) // 4:  # Using half-width for more accurate collision
                    # Collision detected
                    self.bullets.remove(bullet)
                    self.pigs.remove(pig)
                    
                    # Create explosion
                    explosion = Explosion(pig.x, pig.y, self.assets)
                    self.explosions.append(explosion)
                    
                    # Increase score
                    self.score += 10
                    
                    # Play sound
                    self.assets.play_sound('explosion')
                    break
        
        # Update explosions
        for explosion in self.explosions[:]:
            explosion.update()
            if not explosion.is_active:
                self.explosions.remove(explosion)
        
        # Check for game over condition (can be customized)
        if self.score >= 200:
            self.next_state = STATE_GAME_OVER
    
    def handle_input(self, event):
        """Handle user input"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Add a pig at the click position
                self.add_pig(event.pos[0], event.pos[1])
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.create_bullet()
            elif event.key == pygame.K_ESCAPE:
                self.next_state = STATE_GAME_OVER
                return True
        
        return False
    
    def draw(self, screen):
        """Draw the game state"""
        # Draw background
        screen.blit(self.background, (0, 0))
        
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(screen)
        
        # Draw pigs
        for pig in self.pigs:
            pig.draw(screen)
        
        # Draw bird (on top)
        self.bird.draw(screen)
        
        # Draw explosions
        for explosion in self.explosions:
            explosion.draw(screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        screen.blit(score_text, (20, 20)) 