import pygame
import os
import sys
import random
import math

# Add parent directory to path for direct execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    # Try importing with full package path first (when run through main launcher)
    from games.Pig_invaders.src.constants import (
        SCREEN_WIDTH, SCREEN_HEIGHT, STATE_MENU, STATE_CREDITS,
        WHITE, BLACK, GRAY, DARK_BLUE, LIGHT_BLUE, RED, YELLOW
    )
except ImportError:
    # Fall back to local import for direct execution
    from src.constants import (
        SCREEN_WIDTH, SCREEN_HEIGHT, STATE_MENU, STATE_CREDITS,
        WHITE, BLACK, GRAY, DARK_BLUE, LIGHT_BLUE, RED, YELLOW
    )

class Game:
    """Main game class"""
    
    def __init__(self, assets):
        """Initialize the game"""
        self.assets = assets
        self.next_state = None
        self.score = 0
        self.in_briefing = True  # Start with briefing
        self.assets.briefing.start()  # Explicitly start the briefing
        self.music_enabled = True  # Track music state
        
        # Create a font for displaying text
        self.font = pygame.font.Font(None, 36)
        
        # Load General Pig image
        self.general_pig = self.assets.get_image('general_pig_briefing')
        if self.general_pig:
            # Scale the image to fill the screen
            self.general_pig = pygame.transform.scale(self.general_pig, (SCREEN_WIDTH, SCREEN_HEIGHT))
            
        # Game state
        self.game_started = False
        
        # Player properties
        self.player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100]
        self.player_speed = 8  # Increased speed for smoother movement
        self.player_health = 100
        self.player_bullets = []
        self.shoot_cooldown = 0
        self.shoot_delay = 15  # Frames between shots
        
        # Enemy properties
        self.enemies = []
        self.enemy_bullets = []
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 60  # Frames between enemy spawns
        
        # Map properties
        self.map_scroll = 0
        self.scroll_speed = 2
        self.map_objects = []  # List of space objects (asteroids, stars, galaxies)
        self.generate_map_objects()
        # Create some background stars
        self.stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(100)]  # More stars
        
    def start_briefing(self):
        """Start the briefing sequence and its music"""
        self.assets.play_briefing_music(volume=0.3)
        
    def generate_map_objects(self):
        """Generate space objects (asteroids, stars, galaxies)"""
        for _ in range(15):  # Generate more objects for a busier space scene
            obj_type = random.choice(['asteroid', 'galaxy', 'nebula'])
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(-SCREEN_HEIGHT, 0)  # Start above screen
            
            if obj_type == 'asteroid':
                size = random.randint(20, 60)
                color = random.choice([GRAY, (139, 69, 19), (169, 169, 169)])  # Gray, brown, or dark gray
                self.map_objects.append({
                    'type': obj_type,
                    'rect': pygame.Rect(x, y, size, size),
                    'color': color,
                    'rotation': random.randint(0, 360)
                })
            elif obj_type == 'galaxy':
                size = random.randint(80, 150)
                color = random.choice([LIGHT_BLUE, (138, 43, 226), (75, 0, 130)])  # Blue and purple hues
                self.map_objects.append({
                    'type': obj_type,
                    'rect': pygame.Rect(x, y, size, size),
                    'color': color,
                    'spiral_points': [(random.randint(-size//2, size//2), random.randint(-size//2, size//2)) for _ in range(30)]  # More points
                })
            else:  # nebula
                width = random.randint(100, 200)
                height = random.randint(60, 120)
                color = random.choice([(255, 99, 71), LIGHT_BLUE, (50, 205, 50)])  # Red, blue, or green nebula
                self.map_objects.append({
                    'type': obj_type,
                    'rect': pygame.Rect(x, y, width, height),
                    'color': color,
                    'alpha': random.randint(50, 150)
                })

    def handle_input(self, event):
        """Handle user input in the game"""
        if self.in_briefing:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Advance dialog
                    if self.assets.briefing.next_message():
                        self.in_briefing = False  # Briefing complete
                        self.game_started = True
                        # Stop briefing music and start game music
                        self.assets.stop_music('briefing_music')
                        if self.music_enabled:
                            self.assets.play_background_music(volume=0.3)
            return False
        
        # Normal game input handling
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = STATE_MENU
                self.assets.play_sound('menu_select')
                self.assets.stop_all_music()
            elif event.key == pygame.K_m:
                if self.music_enabled:
                    self.assets.stop_all_music()
                else:
                    if self.in_briefing:
                        self.assets.play_briefing_music(volume=0.3)
                    else:
                        self.assets.play_background_music(volume=0.3)
                self.music_enabled = not self.music_enabled
            elif event.key == pygame.K_SPACE and self.shoot_cooldown <= 0:
                # Shoot
                self.player_bullets.append([self.player_pos[0], self.player_pos[1], 10])  # [x, y, speed]
                self.shoot_cooldown = self.shoot_delay
                self.assets.play_sound('shoot')
        
        return False
        
    def update(self):
        """Update game state"""
        if not self.game_started:
            return
            
        # Continuous movement with arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player_pos[0] > 0:
            self.player_pos[0] -= self.player_speed
        if keys[pygame.K_RIGHT] and self.player_pos[0] < SCREEN_WIDTH:
            self.player_pos[0] += self.player_speed
        if keys[pygame.K_UP] and self.player_pos[1] > 0:
            self.player_pos[1] -= self.player_speed
        if keys[pygame.K_DOWN] and self.player_pos[1] < SCREEN_HEIGHT:
            self.player_pos[1] += self.player_speed
            
        # Update shoot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        # Update map scroll
        self.map_scroll = (self.map_scroll + self.scroll_speed) % SCREEN_HEIGHT
        
        # Update map objects
        for obj in self.map_objects:
            obj['rect'].y += self.scroll_speed
            if obj['rect'].top > SCREEN_HEIGHT:
                # Reset object to top of screen
                obj['rect'].bottom = 0
                obj['rect'].x = random.randint(0, SCREEN_WIDTH)
                if obj['type'] == 'asteroid':
                    obj['rotation'] = random.randint(0, 360)  # New rotation when recycling
        
        # Update player bullets
        for bullet in self.player_bullets[:]:
            bullet[1] -= bullet[2]  # Move up
            if bullet[1] < 0:
                self.player_bullets.remove(bullet)
            else:
                # Check collision with enemies
                bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 10)
                for enemy in self.enemies[:]:
                    if bullet_rect.colliderect(enemy['rect']):
                        self.enemies.remove(enemy)
                        self.player_bullets.remove(bullet)
                        self.score += 100
                        self.assets.play_sound('explosion')
                        break
        
        # Update enemy bullets
        for bullet in self.enemy_bullets[:]:
            bullet[1] += bullet[2]  # Move down
            if bullet[1] > SCREEN_HEIGHT:
                self.enemy_bullets.remove(bullet)
            else:
                # Check collision with player
                bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 10)
                player_rect = pygame.Rect(self.player_pos[0] - 25, self.player_pos[1] - 25, 50, 50)
                if bullet_rect.colliderect(player_rect):
                    self.enemy_bullets.remove(bullet)
                    self.player_health -= 10
                    self.assets.play_sound('explosion')
                    if self.player_health <= 0:
                        self.next_state = STATE_MENU
                        self.assets.stop_all_music()
        
        # Spawn enemies
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_delay:
            self.enemy_spawn_timer = 0
            x = random.randint(0, SCREEN_WIDTH)
            self.enemies.append({
                'rect': pygame.Rect(x, -50, 40, 40),
                'speed': random.randint(2, 4),
                'shoot_timer': 0
            })
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy['rect'].y += enemy['speed']
            # Random horizontal movement
            enemy['rect'].x += random.randint(-2, 2)
            enemy['rect'].x = max(0, min(enemy['rect'].x, SCREEN_WIDTH - 40))
            
            # Enemy shooting
            enemy['shoot_timer'] += 1
            if enemy['shoot_timer'] >= 60:  # Shoot every 60 frames
                enemy['shoot_timer'] = 0
                self.enemy_bullets.append([
                    enemy['rect'].centerx,
                    enemy['rect'].bottom,
                    5  # Bullet speed
                ])
            
            if enemy['rect'].top > SCREEN_HEIGHT:
                self.enemies.remove(enemy)
        
    def draw(self, screen):
        """Draw the game"""
        if self.in_briefing:
            # Fill with black background first
            screen.fill(BLACK)
            
            # Draw General Pig if not showing intel photo
            if not self.assets.briefing.show_intel and self.general_pig:
                # Display at (0,0) to fill screen
                screen.blit(self.general_pig, (0, 0))
            
            # Draw the briefing dialog last to ensure it's on top
            self.assets.briefing.draw(screen)
            
            # Draw mute instructions during briefing
            mute_text = "Press M to toggle music"
            mute_surface = self.font.render(mute_text, True, WHITE)
            screen.blit(mute_surface, (10, SCREEN_HEIGHT - 40))
        else:
            # Draw background
            screen.fill(DARK_BLUE)  # Dark blue space background
            
            # Draw background stars with twinkling effect
            for star in self.stars:
                # Randomly make some stars twinkle
                brightness = random.randint(150, 255)
                pygame.draw.circle(screen, (brightness, brightness, brightness), star, random.choice([1, 2]))
            
            # Draw map objects
            for obj in self.map_objects:
                if obj['type'] == 'asteroid':
                    # Draw irregular asteroid shape
                    points = []
                    center = obj['rect'].center
                    radius = obj['rect'].width // 2
                    for angle in range(0, 360, 45):
                        rad = random.uniform(0.8, 1.2) * radius
                        angle_rad = math.radians(angle + obj['rotation'])
                        x = center[0] + rad * math.cos(angle_rad)
                        y = center[1] + rad * math.sin(angle_rad)
                        points.append((int(x), int(y)))
                    pygame.draw.polygon(screen, obj['color'], points)
                    # Add some crater details
                    for _ in range(3):
                        crater_pos = (random.randint(obj['rect'].left, obj['rect'].right),
                                    random.randint(obj['rect'].top, obj['rect'].bottom))
                        pygame.draw.circle(screen, (50, 50, 50), crater_pos, random.randint(3, 8))
                
                elif obj['type'] == 'galaxy':
                    # Draw spiral galaxy
                    center = obj['rect'].center
                    for point in obj['spiral_points']:
                        x = center[0] + point[0]
                        y = center[1] + point[1]
                        size = random.randint(2, 5)
                        pygame.draw.circle(screen, obj['color'], (int(x), int(y)), size)
                    # Add bright center
                    pygame.draw.circle(screen, WHITE, center, obj['rect'].width // 8)
                
                else:  # nebula
                    # Create a surface with alpha for the nebula
                    nebula_surface = pygame.Surface((obj['rect'].width, obj['rect'].height), pygame.SRCALPHA)
                    for _ in range(20):
                        cloud_rect = pygame.Rect(
                            random.randint(0, obj['rect'].width - 20),
                            random.randint(0, obj['rect'].height - 20),
                            random.randint(20, 40),
                            random.randint(20, 40)
                        )
                        color_with_alpha = (*obj['color'], obj['alpha'])
                        pygame.draw.ellipse(nebula_surface, color_with_alpha, cloud_rect)
                    screen.blit(nebula_surface, obj['rect'])
            
            # Draw player
            player_image = self.assets.get_image('player')
            screen.blit(player_image, (self.player_pos[0] - 25, self.player_pos[1] - 25))
            
            # Draw player bullets
            for bullet in self.player_bullets:
                pygame.draw.rect(screen, YELLOW, (bullet[0], bullet[1], 5, 10))
            
            # Draw enemies
            enemy_image = self.assets.get_image('enemy')
            for enemy in self.enemies:
                screen.blit(enemy_image, enemy['rect'])
            
            # Draw enemy bullets
            for bullet in self.enemy_bullets:
                pygame.draw.rect(screen, RED, (bullet[0], bullet[1], 5, 10))
            
            # Draw score
            score_text = f"Score: {self.score}"
            score_surface = self.font.render(score_text, True, WHITE)
            screen.blit(score_surface, (10, 10))
            
            # Draw health
            health_text = f"Health: {self.player_health}"
            health_surface = self.font.render(health_text, True, WHITE)
            screen.blit(health_surface, (10, 50))
            
            # Draw mute instructions
            mute_text = "Press M to toggle music"
            mute_surface = self.font.render(mute_text, True, WHITE)
            screen.blit(mute_surface, (10, SCREEN_HEIGHT - 40))
