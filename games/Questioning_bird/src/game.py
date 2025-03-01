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
        PIG_WIDTH, PIG_HEIGHT, BIRD_RADIUS, PIG_RADIUS, BULLET_RADIUS,
        MAX_PIGS, MAX_BULLETS, BULLET_SPEED, PIG_MIN_SPEED, PIG_MAX_SPEED,
        EXPLOSION_DURATION, STATE_GAME_OVER, BIRD_QUESTIONS, MENU
    )
    from games.Questioning_bird.src.entities.bird import Bird
    from games.Questioning_bird.src.entities.pig import Pig
    from games.Questioning_bird.src.entities.bullet import Bullet
    from games.Questioning_bird.src.entities.special_bullet import SpecialBullet
    from games.Questioning_bird.src.entities.explosion import Explosion
    from games.Questioning_bird.src.ui.dialog import DialogPopup
except ImportError:
    # Fall back to local import for direct execution
    from constants import (
        SCREEN_WIDTH, SCREEN_HEIGHT, BIRD_WIDTH, BIRD_HEIGHT,
        PIG_WIDTH, PIG_HEIGHT, BIRD_RADIUS, PIG_RADIUS, BULLET_RADIUS,
        MAX_PIGS, MAX_BULLETS, BULLET_SPEED, PIG_MIN_SPEED, PIG_MAX_SPEED,
        EXPLOSION_DURATION, STATE_GAME_OVER, BIRD_QUESTIONS, MENU
    )
    from entities.bird import Bird
    from entities.pig import Pig
    from entities.bullet import Bullet
    from entities.special_bullet import SpecialBullet
    from entities.explosion import Explosion
    from ui.dialog import DialogPopup

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
        
        # Load background from file
        self.background = self.load_background()
        
        # Auto-shoot timer
        self.shoot_timer = 0
        self.shoot_delay = 45  # frames between shots
        
        # Dialog popup
        self.dialog = None
        self.game_paused = False
        
        # Game outcome
        self.victory = False
        
        # Special bullet for angry bird attack
        self.special_bullet = None
        self.screen_flash_alpha = 0
        
        # Background music
        self.start_background_music()
        
    def start_background_music(self):
        """Start playing background music if available"""
        try:
            # Initialize pygame mixer if not already initialized
            if not pygame.mixer.get_init():
                pygame.mixer.init()
                
            # Check if background music file exists
            assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
            music_path = os.path.join(assets_dir, "background_music.wav")
            
            if os.path.exists(music_path):
                print("Loading background music...")
                # Load and play the music
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(0.4)  # Set volume to 40%
                pygame.mixer.music.play(-1)  # -1 means loop indefinitely
                print("Background music started")
            else:
                print(f"Background music file not found: {music_path}")
        except Exception as e:
            print(f"Error starting background music: {e}")
        
    def load_background(self):
        """Load the background image from file"""
        try:
            # Get the assets directory path
            assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
            
            # Try to load the AI-enhanced background image first
            ai_bg_path = os.path.join(assets_dir, "background_ai.png")
            if os.path.exists(ai_bg_path):
                print("Loading AI-enhanced background")
                return pygame.image.load(ai_bg_path).convert()
                
            # Fall back to the original background image
            bg_path = os.path.join(assets_dir, "background.png")
            if os.path.exists(bg_path):
                print("Loading original background")
                return pygame.image.load(bg_path).convert()
            else:
                print(f"No background images found in {assets_dir}, using fallback")
                return self.create_background()
        except Exception as e:
            print(f"Error loading background: {e}, using fallback")
            return self.create_background()
        
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
            self.assets.play_sound('shoot', volume=0.4)  # Lower volume for frequent shooting
    
    def add_pig(self, x, y):
        """Add a new pig at the specified position, moving toward the bird"""
        if len(self.pigs) < MAX_PIGS:
            # Random speed between min and max
            speed = random.uniform(PIG_MIN_SPEED, PIG_MAX_SPEED)
            pig = Pig(x, y, self.bird.x, self.bird.y, speed, self.assets)
            self.pigs.append(pig)
            
    def update(self):
        """Update the game state"""
        # If game is paused due to dialog, only update dialog
        if self.game_paused:
            return
            
        # Check if bird is ready to attack player
        if self.bird.is_ready_to_attack() and self.special_bullet is None:
            # Create special bullet
            print("Bird is ready to attack! Creating special bullet.")
            x, y = self.bird.get_attack_position()
            self.special_bullet = SpecialBullet(x, y, self.assets)
            # Play sound if available
            self.assets.play_sound('special_attack', volume=1.0)
            
            # Fade out background music during special attack
            try:
                pygame.mixer.music.fadeout(2000)  # Fade out over 2 seconds
            except:
                pass
            
        # Update special bullet if it exists
        if self.special_bullet:
            print(f"Updating special bullet. Phase: {self.special_bullet.phase}, Size: {self.special_bullet.current_size}")
            self.special_bullet.update()
            
            # Check if special bullet is done (reached max size)
            if self.special_bullet.is_done():
                print("Special bullet reached maximum size! Game over.")
                # Flash the screen white
                self.screen_flash_alpha = 255
                # Play game over sound
                self.assets.play_sound('game_over', volume=1.0)
                # End the game with defeat
                self.victory = False
                self.next_state = STATE_GAME_OVER
                self.special_bullet = None
                return
        
        # Decrease screen flash
        if self.screen_flash_alpha > 0:
            self.screen_flash_alpha -= 5
            
        # Check if we should show a dialog
        if self.dialog is None and self.bird.should_show_dialog() and not self.bird.is_angry:
            # Select a random question
            question = random.choice(BIRD_QUESTIONS)
            self.dialog = DialogPopup(question, self.assets)
            self.game_paused = True
            
            # Lower background music volume during dialog
            try:
                pygame.mixer.music.set_volume(0.2)
            except:
                pass
            
        # Auto-target nearest pig instead of following mouse
        if self.pigs and not self.bird.is_angry:
            # Find the nearest pig
            nearest_pig = None
            min_distance = float('inf')
            
            for pig in self.pigs:
                distance = math.sqrt((pig.x - self.bird.x)**2 + (pig.y - self.bird.y)**2)
                if distance < min_distance:
                    min_distance = distance
                    nearest_pig = pig
            
            if nearest_pig:
                # Calculate angle to the nearest pig
                dx = nearest_pig.x - self.bird.x
                dy = nearest_pig.y - self.bird.y
                target_angle = math.degrees(math.atan2(dy, dx))
                self.bird.update(target_angle)
            else:
                # No pigs to target, just update without changing angle
                self.bird.update()
        else:
            # No pigs or bird is angry, just update
            self.bird.update()
        
        # Auto-shoot logic
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_delay and self.pigs:
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
                # VICTORY if pig reaches bird (reversed from original)
                self.victory = True
                self.next_state = STATE_GAME_OVER
                # Play game over sound with victory
                self.assets.play_sound('game_over', volume=0.7)
                return
            
            # Check for collisions with bullets
            for bullet in self.bullets[:]:
                bullet_distance = math.sqrt((bullet.x - pig.x)**2 + (bullet.y - pig.y)**2)
                if bullet_distance < (BULLET_RADIUS + PIG_RADIUS):
                    # Create explosion
                    self.explosions.append(Explosion(pig.x, pig.y, self.assets))
                    # Remove pig and bullet
                    if pig in self.pigs:
                        self.pigs.remove(pig)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    # Increase score
                    self.score += 10
                    # Play explosion sound
                    self.assets.play_sound('explosion', volume=0.6)
                    break
        
        # Update explosions
        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.frame >= EXPLOSION_DURATION:
                self.explosions.remove(explosion)
        
        # Check for game over condition - LOSE if score reaches 10,000 (reversed from original)
        if self.score >= 10000:
            self.victory = False
            self.next_state = STATE_GAME_OVER
            # Play game over sound
            self.assets.play_sound('game_over', volume=1.0)
    
    def handle_input(self, event):
        """Handle user input events"""
        # If dialog is active, handle dialog input first
        if self.dialog and self.dialog.active:
            option_index = self.dialog.handle_input(event)
            if option_index is not None:
                # Get the current question data
                question_data = None
                for q in BIRD_QUESTIONS:
                    if q["question"] == self.dialog.question:
                        question_data = q
                        break
                
                # Set bird's response based on player's choice
                self.bird.set_response(option_index, question_data)
                self.dialog = None
                self.game_paused = False
                
                # Restore background music volume after dialog
                try:
                    pygame.mixer.music.set_volume(0.4)
                except:
                    pass
            return
            
        # If special bullet is active, don't allow other inputs
        if self.special_bullet:
            return
            
        # Regular game input
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Add a pig at the clicked position
                self.add_pig(event.pos[0], event.pos[1])
                # Play a menu select sound when adding a pig
                self.assets.play_sound('menu_select', volume=0.4)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Return to menu
                self.next_state = MENU
                # Play menu select sound
                self.assets.play_sound('menu_select', volume=0.5)
                return
            elif event.key == pygame.K_a:
                # Debug: Directly trigger angry state with 'A' key
                print("DEBUG: Manually triggering angry state!")
                self.bird.become_angry()
                return
            elif event.key == pygame.K_q:
                # Debug: Directly trigger a dialog popup with 'Q' key
                print("DEBUG: Manually triggering a dialog popup!")
                question = random.choice(BIRD_QUESTIONS)
                self.dialog = DialogPopup(question, self.assets)
                self.game_paused = True
                # Lower background music volume during dialog
                try:
                    pygame.mixer.music.set_volume(0.2)
                except:
                    pass
                return
            elif event.key == pygame.K_m:
                # Toggle music on/off
                try:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                        print("Music paused")
                    else:
                        pygame.mixer.music.unpause()
                        print("Music resumed")
                except:
                    pass
                return
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                # Increase music volume
                try:
                    current_volume = pygame.mixer.music.get_volume()
                    new_volume = min(1.0, current_volume + 0.1)
                    pygame.mixer.music.set_volume(new_volume)
                    print(f"Music volume: {new_volume:.1f}")
                except:
                    pass
                return
            elif event.key == pygame.K_MINUS:
                # Decrease music volume
                try:
                    current_volume = pygame.mixer.music.get_volume()
                    new_volume = max(0.0, current_volume - 0.1)
                    pygame.mixer.music.set_volume(new_volume)
                    print(f"Music volume: {new_volume:.1f}")
                except:
                    pass
                return
        
        return False
    
    def draw(self, screen):
        """Draw the game on the screen"""
        # Draw background
        screen.blit(self.background, (0, 0))
        
        # Draw all game entities
        for explosion in self.explosions:
            explosion.draw(screen)
            
        for pig in self.pigs:
            pig.draw(screen)
            
        for bullet in self.bullets:
            bullet.draw(screen)
            
        # Draw special bullet if it exists
        if self.special_bullet:
            self.special_bullet.draw(screen)
            
        self.bird.draw(screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        # Draw controls hints
        controls_text = self.font.render("M: Toggle Music | +/-: Volume | Q: Question | A: Angry", True, (255, 255, 255))
        controls_rect = controls_text.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10))
        screen.blit(controls_text, controls_rect)
        
        # Draw dialog if active
        if self.dialog and self.dialog.active:
            # Draw semi-transparent overlay to focus on dialog
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # Semi-transparent black
            screen.blit(overlay, (0, 0))
            
            self.dialog.draw(screen)
            
        # Draw screen flash effect if active
        if self.screen_flash_alpha > 0:
            flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            flash_surface.fill((255, 255, 255, self.screen_flash_alpha))
            screen.blit(flash_surface, (0, 0)) 