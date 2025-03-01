import pygame
import sys
import os
import random
import math
import numpy as np  # Add numpy for sound generation
import wave  # Add wave for saving sound files
from enum import Enum

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize the sound mixer

# Game constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)  # Sky color
BROWN = (139, 69, 19)  # Tree trunk color
DARK_BROWN = (101, 67, 33)  # Darker wood color
LIGHT_BROWN = (222, 184, 135)  # Light wood color
METAL_GRAY = (169, 169, 169)  # Metal color for sledge runners
GREEN = (0, 100, 0)  # Tree top color
PIG_GREEN = (144, 238, 144)  # Light green for Angry Birds pig
PIG_NOSE = (230, 180, 180)  # Pinkish for pig nose
SLEDGE_BROWN = (210, 105, 30)  # Sledge color
FART_COLOR = (200, 200, 100)  # Fart effect color
BIRD_COLOR = (255, 0, 0)  # Bird color
HAT_RED = (220, 20, 60)  # Red for winter hat

# Physics constants
GRAVITY = 0.5
JUMP_POWER = -12
FART_POWER = -0.3  # Reduces fall speed
FART_BOOST = 0.2   # Horizontal speed boost from farting
ROTATION_SPEED = 2
UPHILL_SPEED = 1

# Asset paths - For future implementation with real images
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')

# Create sounds directory if it doesn't exist
os.makedirs(SOUNDS_DIR, exist_ok=True)

# Sound variables
FART_SOUND = None
JUMP_SOUND = None
SLEDGE_SOUND = None
COLLISION_SOUND = None

def load_sound(filename):
    """Load a sound file"""
    filepath = os.path.join(SOUNDS_DIR, filename)
    
    if os.path.exists(filepath):
        try:
            return pygame.mixer.Sound(filepath)
        except:
            print(f"Error loading sound: {filepath}")
            return None
    else:
        print(f"Sound file not found: {filepath}")
        return None

def load_sounds():
    """Load all sound files"""
    global FART_SOUND, JUMP_SOUND, SLEDGE_SOUND, COLLISION_SOUND
    
    # Load the sounds
    FART_SOUND = load_sound("fart.wav")
    JUMP_SOUND = load_sound("jump.wav")
    SLEDGE_SOUND = load_sound("sledge.wav")
    COLLISION_SOUND = load_sound("collision.wav")
    
    if not all([FART_SOUND, JUMP_SOUND, SLEDGE_SOUND, COLLISION_SOUND]):
        print("Some sound files are missing. Run generate_sounds.py to create them.")

# Game state
class GameState:
    PLAYING = 0
    GAME_OVER = 1
    PAUSED = 2

class Player:
    def __init__(self, x, y):
        """Initialize the player (pig on sledge)"""
        self.x = x
        self.y = y
        self.width = 80
        self.height = 60
        self.velocity_y = 0
        self.velocity_x = 5  # Initial horizontal speed
        self.base_velocity_x = 5  # Save initial speed for reference
        self.rotation = 0
        self.on_ground = False
        self.farting = False
        self.was_on_ground = False  # Track previous frame's ground state
        self.uphill = False
        self.fart_timer = 0  # Track how long the pig has been farting
        self.sledge_sound_playing = False  # Track if sledge sound is playing
        
        # Create temporary surfaces for pig and sledge with transparency
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.sledge_image = pygame.Surface((100, 40), pygame.SRCALPHA)  # Made taller for better detail
        
        # Draw the Angry Birds style pig
        self.draw_angry_birds_pig()
        
        # Draw the sledge
        self.draw_sledge()
        
    def draw_sledge(self):
        """Draw a more realistic sledge"""
        width, height = self.sledge_image.get_size()
        
        # Clear surface
        self.sledge_image.fill((0, 0, 0, 0))  # Transparent background
        
        # Draw wooden base (top part)
        wood_height = height // 2
        pygame.draw.rect(self.sledge_image, DARK_BROWN,
                        [0, 0, width, wood_height], 0, 3)
        
        # Draw wooden slats
        slat_count = 5
        slat_width = width // (slat_count * 2)
        for i in range(slat_count):
            x_pos = i * (width // slat_count) + (width // (slat_count * 2)) - (slat_width // 2)
            pygame.draw.rect(self.sledge_image, LIGHT_BROWN,
                            [x_pos, 2, slat_width, wood_height - 4], 0, 2)
        
        # Draw metal runners (bottom part - two curved lines)
        runner_height = height - wood_height
        left_x = 10
        right_x = width - 10
        
        # Left runner (curved metal skate)
        pygame.draw.arc(self.sledge_image, METAL_GRAY,
                       [left_x - 10, wood_height - 5, 20, runner_height * 2],
                       math.pi, math.pi * 1.5, 3)
        pygame.draw.line(self.sledge_image, METAL_GRAY,
                        (left_x, wood_height + runner_height // 2),
                        (left_x, height), 3)
        
        # Right runner (curved metal skate)
        pygame.draw.arc(self.sledge_image, METAL_GRAY,
                       [right_x - 10, wood_height - 5, 20, runner_height * 2],
                       math.pi, math.pi * 1.5, 3)
        pygame.draw.line(self.sledge_image, METAL_GRAY,
                        (right_x, wood_height + runner_height // 2),
                        (right_x, height), 3)
        
        # Horizontal metal connector
        pygame.draw.line(self.sledge_image, METAL_GRAY,
                        (left_x, height - 3),
                        (right_x, height - 3), 2)
        
        # Add a small steering handle
        handle_x = width // 4
        pygame.draw.rect(self.sledge_image, DARK_BROWN,
                        [handle_x, wood_height // 4, 5, -wood_height // 2], 0, 1)
        pygame.draw.rect(self.sledge_image, DARK_BROWN,
                        [handle_x - 10, wood_height // 4 - wood_height // 2, 25, 5], 0, 1)
        
    def draw_angry_birds_pig(self):
        """Draw a pig in Angry Birds style"""
        # Clear the surface
        self.image.fill((0, 0, 0, 0))  # Transparent background
        
        # Draw the main body (circle)
        center_x, center_y = self.width // 2, self.height // 2
        radius = min(self.width, self.height) // 2 - 5
        pygame.draw.circle(self.image, PIG_GREEN, (center_x, center_y), radius)
        
        # Draw the ears (two small circles on top)
        ear_radius = radius // 4
        ear_offset = radius // 2
        pygame.draw.circle(self.image, PIG_GREEN, (center_x - ear_offset, center_y - ear_offset), ear_radius)
        pygame.draw.circle(self.image, PIG_GREEN, (center_x + ear_offset, center_y - ear_offset), ear_radius)
        
        # Draw a winter hat (since we're in a snow theme)
        hat_width = radius * 1.5
        hat_height = radius * 0.8
        hat_y = center_y - radius - hat_height // 2
        
        # Hat base
        pygame.draw.ellipse(self.image, HAT_RED, 
                           [center_x - hat_width//2, hat_y, hat_width, hat_height])
        
        # Hat pom-pom
        pygame.draw.circle(self.image, WHITE, 
                          (center_x, hat_y - hat_height//4), hat_height//2)
        
        # Hat rim
        pygame.draw.rect(self.image, WHITE, 
                        [center_x - hat_width//2, hat_y + hat_height//2, 
                         hat_width, hat_height//4])
        
        # Draw the eyes (two white circles with black pupils)
        eye_radius = radius // 3
        eye_spacing = radius // 2
        eye_y = center_y - radius // 4
        
        # White parts
        pygame.draw.circle(self.image, WHITE, (center_x - eye_spacing, eye_y), eye_radius)
        pygame.draw.circle(self.image, WHITE, (center_x + eye_spacing, eye_y), eye_radius)
        
        # Black pupils
        pupil_radius = eye_radius // 2
        pygame.draw.circle(self.image, BLACK, (center_x - eye_spacing, eye_y), pupil_radius)
        pygame.draw.circle(self.image, BLACK, (center_x + eye_spacing, eye_y), pupil_radius)
        
        # Draw the snout (large circle on bottom half)
        snout_radius = radius // 2
        snout_y = center_y + radius // 3
        pygame.draw.circle(self.image, PIG_GREEN, (center_x, snout_y), snout_radius)
        
        # Draw nostrils (two small dark circles on snout)
        nostril_radius = snout_radius // 4
        nostril_spacing = snout_radius // 2
        nostril_y = snout_y + snout_radius // 3
        pygame.draw.circle(self.image, BLACK, (center_x - nostril_spacing, nostril_y), nostril_radius)
        pygame.draw.circle(self.image, BLACK, (center_x + nostril_spacing, nostril_y), nostril_radius)
        
        # Draw eyebrows (slight arcs above eyes)
        eyebrow_width = eye_radius * 1.2
        eyebrow_height = eye_radius // 2
        eyebrow_y = eye_y - eye_radius - 2
        
        # Left eyebrow
        pygame.draw.arc(self.image, BLACK, 
                        [center_x - eye_spacing - eyebrow_width//2, 
                         eyebrow_y, 
                         eyebrow_width, eyebrow_height], 
                        0, math.pi, 2)
        
        # Right eyebrow
        pygame.draw.arc(self.image, BLACK, 
                        [center_x + eye_spacing - eyebrow_width//2, 
                         eyebrow_y, 
                         eyebrow_width, eyebrow_height], 
                        0, math.pi, 2)
        
    def jump(self):
        """Make the pig jump if on the ground"""
        if self.on_ground:
            self.velocity_y = JUMP_POWER
            self.on_ground = False
            
            # Play jump sound only if we're actually jumping (not just a small hop)
            # This prevents constant jump sounds when sledge is just slightly off the ground
            if JUMP_SOUND and abs(self.velocity_y) > JUMP_POWER / 2:
                JUMP_SOUND.play()
    
    def fart(self):
        """Activate farting to reduce fall speed and boost horizontal speed"""
        if not self.on_ground:
            # Only play the fart sound when starting to fart
            if not self.farting and FART_SOUND:
                FART_SOUND.play()
                
            self.farting = True
            self.velocity_y += FART_POWER  # Reduce falling speed
            self.velocity_x += FART_BOOST  # Boost horizontal speed
            self.fart_timer += 1  # Increment fart timer
        
    def stop_fart(self):
        """Stop farting and reset effects"""
        if self.farting:
            self.farting = False
            self.fart_timer = 0
    
    def rotate(self, direction):
        """Rotate the sledge in the specified direction"""
        # Reverse direction for more intuitive controls
        # A = turn left (rotate negative), D = turn right (rotate positive)
        self.rotation -= direction * ROTATION_SPEED
        # Cap rotation to prevent excessive spinning
        self.rotation = max(-45, min(45, self.rotation))
    
    def move_uphill(self):
        """Move slowly uphill when on uphill sections"""
        if self.uphill and self.on_ground:
            self.x += UPHILL_SPEED
    
    def update(self, terrain):
        """Update the player's position and state"""
        # Store previous ground state
        self.was_on_ground = self.on_ground
        
        # Apply gravity if not on ground
        if not self.on_ground:
            self.velocity_y += GRAVITY
        
        # Update vertical position
        self.y += self.velocity_y
        
        # Get current ground height at player position
        try:
            ground_level = terrain.get_height(self.x)
        except Exception:
            # Fallback if terrain height calculation fails
            ground_level = SCREEN_HEIGHT - 200
        
        # Check for collision with ground
        if self.y >= ground_level - self.height:
            self.y = ground_level - self.height
            
            # Only consider it a landing if we were significantly above the ground
            significant_landing = not self.on_ground and self.velocity_y > 3
            
            self.on_ground = True
            self.velocity_y = 0
            
            # If we just landed from a significant height, play a landing sound
            if significant_landing:
                # For now we reuse the jump sound as a landing sound
                if JUMP_SOUND:
                    JUMP_SOUND.set_volume(0.3)  # Quieter than jump
                    JUMP_SOUND.play()
                    JUMP_SOUND.set_volume(1.0)  # Reset volume for future jumps
            
            # Reset horizontal speed when landing
            if self.velocity_x > self.base_velocity_x:
                self.velocity_x = max(self.base_velocity_x, self.velocity_x * 0.95)
        else:
            self.on_ground = False
        
        # Handle sledge sound
        if self.on_ground:
            # Play continuous sledge sound when on ground
            if SLEDGE_SOUND and not self.sledge_sound_playing:
                SLEDGE_SOUND.play(-1)  # -1 means loop indefinitely
                self.sledge_sound_playing = True
                # Volume based on speed
                volume = min(1.0, self.velocity_x / 15.0)
                SLEDGE_SOUND.set_volume(volume)
        else:
            # Stop sledge sound when in air
            if SLEDGE_SOUND and self.sledge_sound_playing:
                SLEDGE_SOUND.stop()
                self.sledge_sound_playing = False
                
        # If sledge sound is playing, adjust volume based on speed
        if self.sledge_sound_playing and SLEDGE_SOUND:
            volume = min(1.0, self.velocity_x / 15.0)
            SLEDGE_SOUND.set_volume(volume)
        
        # Apply rotation effects on velocity
        # Tilting forward increases speed, tilting backward decreases it
        rotation_effect = self.rotation / 100.0  # Small effect based on rotation
        self.velocity_x += rotation_effect
        
        # Ensure minimum speed
        self.velocity_x = max(3, self.velocity_x)
        
        # If farting, continue to boost speed but with diminishing returns
        if self.farting:
            # Fart effectiveness decreases over time
            fart_effectiveness = max(0, 1.0 - (self.fart_timer / 60.0))
            if fart_effectiveness > 0:
                self.velocity_x += FART_BOOST * fart_effectiveness
            
            # Increment the fart timer
            self.fart_timer += 1
        
        # Update horizontal position (always moving forward)
        self.x += self.velocity_x
    
    def draw(self, screen, camera_x):
        """Draw the player (pig on sledge) on the screen"""
        try:
            # Calculate the rotated sledge
            rotated_sledge = pygame.transform.rotate(self.sledge_image, self.rotation)
            sledge_rect = rotated_sledge.get_rect(center=(self.x - camera_x, self.y + self.height - 10))
            
            # Draw the sledge first (behind the pig)
            screen.blit(rotated_sledge, sledge_rect)
            
            # Draw the pig on top of the sledge
            pig_rect = self.image.get_rect(center=(self.x - camera_x, self.y))
            screen.blit(self.image, pig_rect)
            
            # Draw fart effect if farting
            if self.farting:
                # Draw multiple fart particles for better effect
                for i in range(5):
                    fart_size = random.randint(10, 30)
                    offset_x = random.randint(-10, 10) - 40
                    offset_y = random.randint(-10, 10) + 20
                    
                    # Create fart cloud with transparency
                    fart_image = pygame.Surface((fart_size, fart_size), pygame.SRCALPHA)
                    # Green-yellow gas cloud with gradient opacity
                    opacity = random.randint(100, 200)
                    pygame.draw.circle(fart_image, (*FART_COLOR, opacity), (fart_size//2, fart_size//2), fart_size//2)
                    fart_rect = fart_image.get_rect(center=(self.x - camera_x + offset_x, self.y + offset_y))
                    screen.blit(fart_image, fart_rect)
            
            # Draw speed indicator
            speed_text = pygame.font.Font(None, 24).render(f"Speed: {int(self.velocity_x * 10)}", True, BLACK)
            screen.blit(speed_text, (self.x - camera_x - 30, self.y - 40))
        except Exception as e:
            print(f"Error drawing player: {e}")

class Bird:
    def __init__(self, x, y):
        """Initialize a bird obstacle"""
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        
        # Create a simple bird shape
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BIRD_COLOR, (self.width//2, self.height//2), self.width//2)
        pygame.draw.circle(self.image, BLACK, (self.width//2 - 10, self.height//2 - 5), 5)  # Eye
        pygame.draw.polygon(self.image, (255, 165, 0), [(self.width//2 + 15, self.height//2), 
                                                  (self.width//2 + 30, self.height//2), 
                                                  (self.width//2 + 15, self.height//2 + 5)])  # Beak
        
        # Add some animation
        self.animation_offset = 0
        self.animation_speed = random.uniform(0.05, 0.1)
    
    def update(self):
        """Update bird animation"""
        self.animation_offset += self.animation_speed
        if self.animation_offset > 2*math.pi:
            self.animation_offset = 0
    
    def draw(self, screen, camera_x):
        """Draw the bird on the screen"""
        try:
            # Apply a slight bouncing animation
            y_offset = math.sin(self.animation_offset) * 5
            
            bird_rect = self.image.get_rect(center=(self.x - camera_x, self.y + y_offset))
            screen.blit(self.image, bird_rect)
        except Exception as e:
            print(f"Error drawing bird: {e}")
    
    def check_collision(self, player):
        """Check if the bird collides with the player"""
        # Use a slightly smaller collision box for better gameplay
        collision_margin = 10
        collision = (
            self.x < player.x + player.width - collision_margin and
            self.x + self.width - collision_margin > player.x and
            self.y < player.y + player.height - collision_margin and
            self.y + self.height - collision_margin > player.y
        )
        
        # Play collision sound if collision detected
        if collision and COLLISION_SOUND:
            COLLISION_SOUND.play()
            
        return collision

class Terrain:
    def __init__(self, length):
        """Initialize the terrain with the specified length"""
        self.length = length
        self.segments = []
        self.generate_terrain()
        
    def generate_terrain(self):
        """Generate the terrain segments"""
        # Start with a flat area
        current_height = SCREEN_HEIGHT - 200
        segment_width = 50
        
        # Generate segments from left to right
        for x in range(0, self.length, segment_width):
            # First 1000 pixels are relatively flat for an easy start
            if x < 1000:
                next_height = current_height + random.randint(-5, 5)
            else:
                # Create occasional ramps and hills
                if random.random() < 0.1:
                    # Create a ramp or hill
                    if random.random() < 0.6:  # 60% chance of ramp, 40% chance of hill
                        # Ramp down
                        next_height = current_height + random.randint(50, 100)
                    else:
                        # Hill (up then down)
                        next_height = current_height - random.randint(30, 70)
                else:
                    # Regular flat or slight variation
                    next_height = current_height + random.randint(-10, 10)
            
            # Ensure height stays within reasonable bounds
            next_height = min(SCREEN_HEIGHT - 100, max(SCREEN_HEIGHT - 400, next_height))
            
            # Add the segment
            self.segments.append((x, current_height, x + segment_width, next_height))
            current_height = next_height
    
    def get_height(self, x):
        """Get the height of the terrain at position x"""
        if x < 0:
            return SCREEN_HEIGHT - 200  # Default height at the start
        
        # Find the segment that contains position x
        for segment in self.segments:
            start_x, start_y, end_x, end_y = segment
            if start_x <= x < end_x:
                # Linear interpolation to find exact height
                t = (x - start_x) / (end_x - start_x)
                return start_y + t * (end_y - start_y)
        
        # If x is beyond the generated terrain
        return SCREEN_HEIGHT - 200
    
    def draw(self, screen, camera_x):
        """Draw the terrain on the screen"""
        try:
            # Only draw segments that are visible on screen
            visible_segments = [s for s in self.segments 
                               if s[0] - camera_x < SCREEN_WIDTH and s[2] - camera_x > 0]
            
            # Draw the terrain lines
            for segment in visible_segments:
                start_x, start_y, end_x, end_y = segment
                pygame.draw.line(screen, WHITE, 
                                (start_x - camera_x, start_y), 
                                (end_x - camera_x, end_y), 
                                3)
            
            # Fill the area below the terrain
            for segment in visible_segments:
                start_x, start_y, end_x, end_y = segment
                points = [
                    (start_x - camera_x, start_y),
                    (end_x - camera_x, end_y),
                    (end_x - camera_x, SCREEN_HEIGHT),
                    (start_x - camera_x, SCREEN_HEIGHT)
                ]
                pygame.draw.polygon(screen, WHITE, points)
            
            # Draw some trees and obstacles (only on visible segments)
            for segment in visible_segments:
                start_x, start_y, end_x, end_y = segment
                
                # Use deterministic randomness based on segment position
                # so trees stay in the same place when revisited
                rand_seed = int(start_x / 100)
                random.seed(rand_seed)
                
                if random.random() < 0.05:  # 5% chance to place a tree
                    tree_x = (start_x + end_x) / 2
                    tree_y = (start_y + end_y) / 2
                    tree_height = random.randint(50, 100)
                    
                    # Draw trunk
                    pygame.draw.rect(screen, BROWN, 
                                    (tree_x - camera_x - 5, tree_y - tree_height, 10, tree_height))
                    
                    # Draw tree top (circle)
                    pygame.draw.circle(screen, GREEN, 
                                      (int(tree_x - camera_x), int(tree_y - tree_height)), 20)
                
                # Reset the random seed
                random.seed()
        except Exception as e:
            print(f"Error drawing terrain: {e}")

def draw_snowflakes(screen):
    """Draw animated snowflakes on the screen"""
    for _ in range(50):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        size = random.randint(1, 3)
        pygame.draw.circle(screen, WHITE, (x, y), size)

def draw_quit_button(screen, font):
    """Draw a quit button in the corner of the screen"""
    quit_text = font.render("ESC: Main Menu", True, BLACK)
    quit_bg = pygame.Surface((quit_text.get_width() + 20, quit_text.get_height() + 10))
    quit_bg.fill(WHITE)
    quit_bg.set_alpha(180)  # Semi-transparent background
    
    screen.blit(quit_bg, (SCREEN_WIDTH - quit_text.get_width() - 30, 20))
    screen.blit(quit_text, (SCREEN_WIDTH - quit_text.get_width() - 20, 25))

def run_game():
    """Main game function"""
    # Set up the game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snowy Run")
    clock = pygame.time.Clock()
    
    # Load sounds
    load_sounds()
    
    # Create game objects
    terrain_length = 50000  # Long terrain
    terrain = Terrain(terrain_length)
    player = Player(200, SCREEN_HEIGHT - 300)
    
    # Create birds
    birds = []
    for i in range(50):  # Create 50 birds
        bird_x = random.randint(1000, terrain_length - 1000)  # No birds at the very beginning
        bird_y = terrain.get_height(bird_x) - 20  # Birds on the ground
        birds.append(Bird(bird_x, bird_y))
    
    # Camera position (follows the player)
    camera_x = 0
    
    # Game state
    game_state = GameState.PLAYING
    score = 0
    font = pygame.font.Font(None, 36)
    
    # Main game loop
    running = True
    return_to_menu = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle key events
            if event.type == pygame.KEYDOWN:
                # ESC key to quit to main menu
                if event.key == pygame.K_ESCAPE:
                    # Stop all sounds before returning to menu
                    if SLEDGE_SOUND and player.sledge_sound_playing:
                        SLEDGE_SOUND.stop()
                    
                    return_to_menu = True
                    running = False
                
                if game_state == GameState.PLAYING:
                    if event.key == pygame.K_SPACE:
                        player.jump()
                    if event.key == pygame.K_f:
                        player.fart()
                    if event.key == pygame.K_UP:
                        player.uphill = True
                elif game_state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        # Stop all sounds before restarting
                        if SLEDGE_SOUND and player.sledge_sound_playing:
                            SLEDGE_SOUND.stop()
                        
                        # Reset the game
                        player = Player(200, SCREEN_HEIGHT - 300)
                        camera_x = 0
                        game_state = GameState.PLAYING
                        score = 0
            
            if event.type == pygame.KEYUP:
                if game_state == GameState.PLAYING:
                    if event.key == pygame.K_f:
                        player.stop_fart()
                    if event.key == pygame.K_UP:
                        player.uphill = False
        
        if game_state == GameState.PLAYING:
            # Get keys for continuous input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                player.rotate(-1)  # A = rotate left (negative)
            if keys[pygame.K_d]:
                player.rotate(1)   # D = rotate right (positive)
            
            # Update player
            player.update(terrain)
            player.move_uphill()
            
            # Update birds
            for bird in birds:
                bird.update()
            
            # Update camera to follow player
            camera_x = player.x - SCREEN_WIDTH // 3
            
            # Check for collisions with birds
            for bird in birds:
                if bird.check_collision(player):
                    # Stop sledge sound if it's playing
                    if SLEDGE_SOUND and player.sledge_sound_playing:
                        SLEDGE_SOUND.stop()
                        player.sledge_sound_playing = False
                    
                    game_state = GameState.GAME_OVER
            
            # Update score (based on distance traveled)
            score = int(player.x / 10)
        
        # Drawing
        try:
            # Background
            screen.fill(BLUE)  # Clear screen with sky color
            
            # Draw animated snowflakes
            draw_snowflakes(screen)
            
            # Draw terrain
            terrain.draw(screen, camera_x)
            
            # Draw birds (only draw visible birds)
            visible_birds = [b for b in birds if 0 <= b.x - camera_x <= SCREEN_WIDTH]
            for bird in visible_birds:
                bird.draw(screen, camera_x)
            
            # Draw player
            player.draw(screen, camera_x)
            
            # Draw score
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (20, 20))
            
            # Draw quit button
            draw_quit_button(screen, font)
            
            # Draw game controls help
            if player.x < 1000:  # Only show at the beginning
                controls_text = [
                    "SPACE: Jump",
                    "F: Fart in air",
                    "A/D: Rotate sledge",
                    "UP: Move uphill"
                ]
                
                for i, text in enumerate(controls_text):
                    help_text = font.render(text, True, BLACK)
                    screen.blit(help_text, (SCREEN_WIDTH - 200, 80 + i * 30))
            
            # Draw game over message
            if game_state == GameState.GAME_OVER:
                # Semi-transparent overlay
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 128))  # Black with alpha
                screen.blit(overlay, (0, 0))
                
                # Game over text
                game_over_text = font.render("Game Over! Press SPACE to restart", True, WHITE)
                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))
                
                # Display final score
                final_score_text = font.render(f"Final Score: {score}", True, WHITE)
                screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40))
                
                # Menu option
                menu_text = font.render("Press ESC to return to Main Menu", True, WHITE)
                screen.blit(menu_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 80))
            
            # Update the display
            pygame.display.flip()
            
        except Exception as e:
            print(f"Error in rendering: {e}")
            
        # Cap the frame rate
        clock.tick(FPS)
    
    # Stop all sounds before exiting
    if SLEDGE_SOUND and player.sledge_sound_playing:
        SLEDGE_SOUND.stop()
    
    # Properly return depending on exit condition
    if return_to_menu:
        # Don't quit pygame here to return to menu
        return True
    else:
        # Quit pygame if we're exiting the game completely
        pygame.quit()
        return False

if __name__ == "__main__":
    try:
        run_game()
    except Exception as e:
        print(f"Game crashed: {e}")
        pygame.quit() 