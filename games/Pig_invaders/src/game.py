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
        self.is_game_over = False  # New game over state
        self.game_over_alpha = 0  # For fade in effect
        self.assets.briefing.start()  # Explicitly start the briefing
        self.music_enabled = True  # Track music state
        self.use_mouse_control = True  # Enable mouse control by default
        
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
        self.player_speed = 5
        self.player_health = 100
        self.player_rect = pygame.Rect(0, 0, 50, 50)  # Will be updated in draw
        self.player_invincible = False
        self.player_invincible_timer = 0
        self.shooting_cooldown = 0  # Cooldown timer for continuous shooting
        self.is_shooting = False  # Flag to track if spacebar is held down
        self.player_bullets = []
        self.shoot_cooldown = 0
        self.shoot_delay = 15
        self.player_size = (64, 64)
        self.has_missiles = False  # Track if player has missile power-up
        self.missile_shots = 0  # Count of missiles shot
        self.max_missiles = 5  # Maximum number of missiles per power-up
        
        # Fire exhaust effect properties
        self.exhaust_particles = []
        self.exhaust_timer = 0
        self.exhaust_colors = [(255, 165, 0), (255, 140, 0), (255, 69, 0), (255, 0, 0)]  # Orange to red gradient
        self.exhaust_max_particles = 20
        
        # Power-up properties
        self.power_up = None
        self.power_up_timer = 300  # Start spawning after 5 seconds (60 FPS * 5)
        self.power_up_size = 30
        
        # Missile properties
        self.missiles = []  # List to track heat-seeking missiles
        self.explosions = []  # List to track explosion effects
        
        # Enemy properties
        self.enemies = []
        self.enemy_bullets = []
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 60  # Frames between enemy spawns
        self.enemy_behaviors = ['chase', 'zigzag', 'circle', 'ambush']  # Different movement patterns
        
        # Map properties
        self.map_scroll = 0
        self.scroll_speed = 2
        self.map_objects = []  # List of space objects (asteroids, stars, galaxies)
        self.generate_map_objects()
        
        # Create stable background stars with fixed properties
        self.stars = []
        for _ in range(100):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.choice([1, 1, 2]),  # More small stars than large
                'brightness': random.randint(150, 255),
                'twinkle_speed': random.uniform(0.02, 0.1),
                'twinkle_offset': random.uniform(0, 2 * math.pi),
                'base_brightness': random.randint(150, 255)
            })
        
        # Health pack properties
        self.health_pack = None
        self.health_pack_timer = 600  # Start spawning after 10 seconds (60 FPS * 10)
        self.health_pack_size = 30
        self.health_recovery = 50  # Amount of health recovered

    def start_briefing(self):
        """Start the briefing sequence and its music"""
        self.assets.play_briefing_music(volume=0.3)
        
    def generate_map_objects(self):
        """Generate space objects with pre-calculated properties to avoid flickering"""
        for _ in range(15):
            obj_type = random.choice(['asteroid', 'galaxy', 'nebula'])
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(-SCREEN_HEIGHT, 0)
            
            if obj_type == 'asteroid':
                size = random.randint(20, 60)
                color = random.choice([GRAY, (139, 69, 19), (169, 169, 169)])
                
                # Pre-calculate asteroid points
                points = []
                center = (x + size//2, y + size//2)
                for angle in range(0, 360, 45):
                    rad = random.uniform(0.8, 1.2) * (size//2)
                    angle_rad = math.radians(angle)
                    point_x = center[0] + rad * math.cos(angle_rad)
                    point_y = center[1] + rad * math.sin(angle_rad)
                    points.append((int(point_x), int(point_y)))
                
                # Pre-calculate craters
                craters = []
                for _ in range(3):
                    craters.append({
                        'x': random.randint(0, size),
                        'y': random.randint(0, size),
                        'size': random.randint(3, 8)
                    })
                
                self.map_objects.append({
                    'type': obj_type,
                    'rect': pygame.Rect(x, y, size, size),
                    'color': color,
                    'points': points,
                    'craters': craters
                })
                
            elif obj_type == 'galaxy':
                size = random.randint(80, 150)
                color = random.choice([LIGHT_BLUE, (138, 43, 226), (75, 0, 130)])
                
                # Pre-calculate spiral points
                spiral_points = []
                for _ in range(30):
                    spiral_points.append({
                        'x': random.randint(-size//2, size//2),
                        'y': random.randint(-size//2, size//2),
                        'size': random.randint(2, 5)
                    })
                
                self.map_objects.append({
                    'type': obj_type,
                    'rect': pygame.Rect(x, y, size, size),
                    'color': color,
                    'spiral_points': spiral_points
                })
                
            else:  # nebula
                width = random.randint(100, 200)
                height = random.randint(60, 120)
                color = random.choice([(255, 99, 71), LIGHT_BLUE, (50, 205, 50)])
                
                # Pre-render nebula surface
                surface = pygame.Surface((width, height), pygame.SRCALPHA)
                alpha = random.randint(50, 150)
                
                # Create a more stable nebula pattern
                for _ in range(20):
                    cloud_rect = pygame.Rect(
                        random.randint(0, width - 20),
                        random.randint(0, height - 20),
                        random.randint(20, 40),
                        random.randint(20, 40)
                    )
                    pygame.draw.ellipse(surface, (*color, alpha), cloud_rect)
                
                self.map_objects.append({
                    'type': obj_type,
                    'rect': pygame.Rect(x, y, width, height),
                    'color': color,
                    'surface': surface
                })

    def create_explosion(self, x, y, size=30, color=YELLOW):
        """Create a new explosion effect"""
        self.explosions.append({
            'x': x,
            'y': y,
            'radius': 5,
            'max_radius': size,
            'alpha': 255,
            'color': color,
            'particles': [
                {
                    'x': x,
                    'y': y,
                    'dx': math.cos(angle) * random.uniform(2, 5),
                    'dy': math.sin(angle) * random.uniform(2, 5),
                    'life': 255,
                    'size': random.randint(2, 4)
                }
                for angle in [math.pi * 2 * i / 12 for i in range(12)]
            ]
        })

    def update_explosions(self):
        """Update explosion effects"""
        for explosion in self.explosions[:]:
            # Update main explosion
            explosion['radius'] += 2
            explosion['alpha'] = int(255 * (1 - explosion['radius'] / explosion['max_radius']))
            
            # Update particles
            for particle in explosion['particles']:
                particle['x'] += particle['dx']
                particle['y'] += particle['dy']
                particle['life'] -= 10
                particle['dy'] += 0.2  # Gravity effect
            
            # Remove finished explosions
            if explosion['radius'] >= explosion['max_radius']:
                self.explosions.remove(explosion)

    def handle_input(self, event):
        """Handle user input events."""
        # Handle briefing input
        if self.in_briefing:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Skip to the next message or end briefing
                    if self.assets.briefing.next_message():
                        # Briefing is complete, start the game
                        self.in_briefing = False
                        self.game_started = True
                        # Stop briefing music and start game music
                        self.assets.stop_music('briefing_music')
                        if self.music_enabled:
                            self.assets.play_background_music(volume=0.3)
                elif event.key == pygame.K_ESCAPE:
                    # Skip the entire briefing
                    self.in_briefing = False
                    self.game_started = True
                    # Stop briefing music and start game music
                    self.assets.stop_music('briefing_music')
                    if self.music_enabled:
                        self.assets.play_background_music(volume=0.3)
                elif event.key == pygame.K_m:
                    # Toggle music
                    if self.music_enabled:
                        self.assets.stop_all_music()
                    else:
                        self.assets.play_briefing_music(volume=0.3)
                    self.music_enabled = not self.music_enabled
            return
            
        if self.is_game_over:
            # Only handle ESC key when game is over
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.next_state = STATE_MENU
                self.assets.play_sound('menu_select')
                self.assets.stop_all_music()
            return
            
        # Handle mouse input for shooting
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.is_shooting = True
            elif event.button == 3:  # Right mouse button (mouse button 2)
                self.fire_missile()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                self.is_shooting = False
                
        # Toggle between mouse and keyboard control with 'C' key
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            self.use_mouse_control = not self.use_mouse_control
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.is_shooting = True
            elif event.key == pygame.K_s:  # S key for missiles in keyboard mode
                self.fire_missile()
            elif event.key == pygame.K_m:
                # Toggle music
                if self.music_enabled:
                    self.assets.stop_all_music()
                else:
                    if self.in_briefing:
                        self.assets.play_briefing_music(volume=0.3)
                    else:
                        self.assets.play_background_music(volume=0.3)
                self.music_enabled = not self.music_enabled
            elif event.key == pygame.K_ESCAPE:
                self.next_state = STATE_MENU
                self.assets.play_sound('menu_select')
                self.assets.stop_all_music()
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.is_shooting = False
        
        return False
        
    def spawn_enemy(self):
        """Spawn a new enemy with random behavior"""
        x = random.randint(0, SCREEN_WIDTH)
        behavior = random.choice(self.enemy_behaviors)
        
        enemy = {
            'rect': pygame.Rect(x, -50, 40, 40),
            'speed': random.randint(1, 3),  # Reduced from (2, 4) to (1, 3)
            'shoot_timer': 0,
            'behavior': behavior,
            'behavior_timer': 0,
            'behavior_duration': random.randint(180, 300),  # Increased duration for more predictable patterns
            'angle': 0,  # For circular motion
            'center_x': x,  # Original spawn point for circular motion
            'center_y': 100,  # Height for circular motion
            'target_x': x,  # For ambush behavior
            'target_y': -50,
            'direction_timer': 0
        }
        
        if behavior == 'ambush':
            # Start from a random edge
            if random.choice([True, False]):
                enemy['rect'].x = random.choice([-40, SCREEN_WIDTH + 40])
                enemy['rect'].y = random.randint(0, SCREEN_HEIGHT // 2)
            else:
                enemy['rect'].x = random.randint(0, SCREEN_WIDTH)
                enemy['rect'].y = -40
        
        self.enemies.append(enemy)

    def update_enemy_behavior(self, enemy):
        """Update enemy movement based on its behavior pattern"""
        enemy['behavior_timer'] += 1
        if enemy['behavior_timer'] >= enemy['behavior_duration']:
            enemy['behavior_timer'] = 0
            enemy['behavior'] = random.choice(self.enemy_behaviors)
            
        if enemy['behavior'] == 'chase':
            # Move towards player with slight randomness
            dx = self.player_pos[0] - enemy['rect'].centerx
            dy = self.player_pos[1] - enemy['rect'].centery
            dist = max(1, (dx * dx + dy * dy) ** 0.5)
            enemy['rect'].x += (dx / dist) * enemy['speed'] * 0.8  # Reduced chase speed
            enemy['rect'].y += (dy / dist) * enemy['speed'] * 0.8  # Reduced chase speed
            
        elif enemy['behavior'] == 'zigzag':
            # Move in a zigzag pattern
            enemy['direction_timer'] += 1
            if enemy['direction_timer'] >= 60:  # Increased from 30 to 60 frames for slower direction changes
                enemy['direction_timer'] = 0
                enemy['target_x'] = random.randint(max(0, enemy['rect'].x - 200), 
                                                 min(SCREEN_WIDTH, enemy['rect'].x + 200))  # Limited horizontal range
            
            dx = enemy['target_x'] - enemy['rect'].centerx
            enemy['rect'].x += (dx / 60) * enemy['speed'] * 0.5  # Reduced horizontal speed
            enemy['rect'].y += enemy['speed'] * 0.3  # Reduced vertical speed
            
        elif enemy['behavior'] == 'circle':
            # Move in a circular pattern
            enemy['angle'] += 0.03  # Reduced from 0.05 to 0.03
            radius = 80  # Reduced from 100 to 80
            enemy['rect'].x = enemy['center_x'] + math.cos(enemy['angle']) * radius
            enemy['rect'].y = enemy['center_y'] + math.sin(enemy['angle']) * radius + enemy['speed'] * 0.3
            enemy['center_y'] += enemy['speed'] * 0.3  # Reduced vertical speed
            
        else:  # 'ambush'
            # Move quickly to ambush position, then charge at player
            if enemy['behavior_timer'] < 60:  # Setup phase
                if enemy['rect'].y < 100:
                    enemy['rect'].y += enemy['speed']
            else:  # Attack phase
                dx = self.player_pos[0] - enemy['rect'].centerx
                dy = self.player_pos[1] - enemy['rect'].centery
                dist = max(1, (dx * dx + dy * dy) ** 0.5)
                enemy['rect'].x += (dx / dist) * enemy['speed'] * 1.5  # Reduced from 2x to 1.5x
                enemy['rect'].y += (dy / dist) * enemy['speed'] * 1.5  # Reduced from 2x to 1.5x
        
        # Keep enemies within screen bounds with some margin
        enemy['rect'].x = max(-20, min(SCREEN_WIDTH - 20, enemy['rect'].x))
        enemy['rect'].y = max(-20, min(SCREEN_HEIGHT + 20, enemy['rect'].y))

    def update_enemy_shooting(self, enemy):
        """Update enemy shooting behavior based on its pattern"""
        enemy['shoot_timer'] += 1
        shoot_delay = 60  # Default shoot delay
        
        if enemy['behavior'] == 'chase':
            shoot_delay = 45  # Shoot more frequently when chasing
        elif enemy['behavior'] == 'ambush':
            shoot_delay = 30  # Shoot very frequently during ambush
        
        if enemy['shoot_timer'] >= shoot_delay:
            enemy['shoot_timer'] = 0
            
            if enemy['behavior'] == 'chase' or enemy['behavior'] == 'ambush':
                # Aimed shot
                dx = self.player_pos[0] - enemy['rect'].centerx
                dy = self.player_pos[1] - enemy['rect'].centery
                dist = max(1, (dx * dx + dy * dy) ** 0.5)
                bullet_speed = 7
                self.enemy_bullets.append([
                    enemy['rect'].centerx,
                    enemy['rect'].bottom,
                    (dx / dist) * bullet_speed,  # x velocity
                    (dy / dist) * bullet_speed   # y velocity
                ])
            else:
                # Normal downward shot
                self.enemy_bullets.append([
                    enemy['rect'].centerx,
                    enemy['rect'].bottom,
                    0,  # x velocity
                    5   # y velocity
                ])

    def spawn_power_up(self):
        """Spawn a missile power-up at a random location"""
        x = random.randint(self.power_up_size, SCREEN_WIDTH - self.power_up_size)
        y = random.randint(self.power_up_size, SCREEN_HEIGHT // 2)
        self.power_up = {
            'rect': pygame.Rect(x, y, self.power_up_size, self.power_up_size),
            'angle': 0,  # For rotation animation
            'glow_offset': 0  # For glow effect
        }

    def spawn_health_pack(self):
        """Spawn a health pack at a random location"""
        x = random.randint(self.health_pack_size, SCREEN_WIDTH - self.health_pack_size)
        y = random.randint(self.health_pack_size, SCREEN_HEIGHT // 2)
        self.health_pack = {
            'rect': pygame.Rect(x, y, self.health_pack_size, self.health_pack_size),
            'blink_offset': 0,  # For blinking effect
            'rotation': 0  # For gentle rotation
        }

    def update_missiles(self):
        """Update missile positions and check for collisions."""
        targeted_enemy_ids = set()
        
        for missile in self.missiles[:]:
            # Check if current target is still valid (exists and on screen)
            target_valid = False
            if missile['target'] and missile['target'] in self.enemies:
                enemy_rect = missile['target']['rect']
                # Check if target is visible on screen with some margin
                if (0 <= enemy_rect.right <= SCREEN_WIDTH and 
                    0 <= enemy_rect.bottom <= SCREEN_HEIGHT):
                    target_valid = True
                    targeted_enemy_ids.add(id(missile['target']))
            
            # Find a new target if current one is invalid
            if not target_valid:
                missile['target'] = None
                best_target = None
                closest_dist = float('inf')
                
                # First try to find untargeted enemies
                for enemy in self.enemies:
                    # Only consider enemies fully on screen
                    if not (0 <= enemy['rect'].right <= SCREEN_WIDTH and 
                            0 <= enemy['rect'].bottom <= SCREEN_HEIGHT):
                        continue
                        
                    # Skip already targeted enemies on first pass
                    if id(enemy) in targeted_enemy_ids:
                        continue
                        
                    dx = enemy['rect'].centerx - missile['pos'][0]
                    dy = enemy['rect'].centery - missile['pos'][1]
                    dist = (dx * dx + dy * dy) ** 0.5
                    
                    if dist < closest_dist:
                        closest_dist = dist
                        best_target = enemy
                
                # If no untargeted enemies, consider all visible enemies
                if not best_target:
                    for enemy in self.enemies:
                        # Only consider enemies fully on screen
                        if not (0 <= enemy['rect'].right <= SCREEN_WIDTH and 
                                0 <= enemy['rect'].bottom <= SCREEN_HEIGHT):
                            continue
                            
                        dx = enemy['rect'].centerx - missile['pos'][0]
                        dy = enemy['rect'].centery - missile['pos'][1]
                        dist = (dx * dx + dy * dy) ** 0.5
                        
                        if dist < closest_dist:
                            closest_dist = dist
                            best_target = enemy
                
                missile['target'] = best_target
                if missile['target']:
                    targeted_enemy_ids.add(id(missile['target']))
                    missile['no_target_timer'] = 0
            
            # Handle behavior when no target is available
            if not missile['target']:
                missile['no_target_timer'] = missile.get('no_target_timer', 0) + 1
                
                # Self-destruct after 1 second with no target
                if missile['no_target_timer'] > 60:
                    self.create_explosion(
                        missile['pos'][0],
                        missile['pos'][1],
                        size=30,
                        color=(255, 215, 0)  # Golden yellow
                    )
                    if missile in self.missiles:  # Safety check
                        self.missiles.remove(missile)
                    continue
                
                # When no target, curve upward
                missile['velocity'][0] *= 0.95  # Gradually reduce horizontal velocity
                missile['velocity'][1] = -missile['speed'] * 0.8  # Move upward
            else:
                # Target tracking behavior
                dx = missile['target']['rect'].centerx - missile['pos'][0]
                dy = missile['target']['rect'].centery - missile['pos'][1]
                dist = max(1, (dx * dx + dy * dy) ** 0.5)
                
                # Calculate desired direction
                desired_dx = dx / dist
                desired_dy = dy / dist
                
                # Adjust velocity toward target with limited turning
                turn_rate = 0.15
                missile['velocity'][0] += (desired_dx * missile['speed'] - missile['velocity'][0]) * turn_rate
                missile['velocity'][1] += (desired_dy * missile['speed'] - missile['velocity'][1]) * turn_rate
                
                # Update angle for drawing
                missile['angle'] = math.atan2(missile['velocity'][0], -missile['velocity'][1])
            
            # Update position
            missile['pos'][0] += missile['velocity'][0]
            missile['pos'][1] += missile['velocity'][1]
            
            # Keep missiles within screen bounds
            screen_margin = 20
            if missile['pos'][0] < screen_margin:
                missile['pos'][0] = screen_margin
                missile['velocity'][0] = abs(missile['velocity'][0]) * 0.5  # Bounce
            elif missile['pos'][0] > SCREEN_WIDTH - screen_margin:
                missile['pos'][0] = SCREEN_WIDTH - screen_margin
                missile['velocity'][0] = -abs(missile['velocity'][0]) * 0.5  # Bounce
                
            if missile['pos'][1] < screen_margin:
                missile['pos'][1] = screen_margin
                missile['velocity'][1] = abs(missile['velocity'][1]) * 0.5  # Bounce
            elif missile['pos'][1] > SCREEN_HEIGHT - screen_margin:
                missile['pos'][1] = SCREEN_HEIGHT - screen_margin
                missile['velocity'][1] = -abs(missile['velocity'][1]) * 0.5  # Bounce
            
            # Normalize velocity to maintain consistent speed
            current_speed = (missile['velocity'][0]**2 + missile['velocity'][1]**2) ** 0.5
            if current_speed > missile['speed']:
                missile['velocity'][0] *= missile['speed'] / current_speed
                missile['velocity'][1] *= missile['speed'] / current_speed
            
            # Check for collisions with enemies with larger hit area
            missile_rect = pygame.Rect(
                missile['pos'][0] - 15,
                missile['pos'][1] - 15,
                30, 30
            )
            
            for enemy in self.enemies[:]:
                if missile_rect.colliderect(enemy['rect']):
                    # Create explosion at enemy position
                    self.create_explosion(
                        enemy['rect'].centerx,
                        enemy['rect'].centery,
                        size=40
                    )
                    
                    # Remove enemy and missile
                    self.enemies.remove(enemy)
                    if missile in self.missiles:
                        self.missiles.remove(missile)
                    
                    # Play explosion sound
                    self.assets.play_sound('explosion')
                    
                    # Add score
                    self.score += 100
                    break

    def update_exhaust_effect(self):
        """Update the fire exhaust particles behind the spaceship"""
        # Add new particles at a controlled rate
        self.exhaust_timer += 1
        if self.exhaust_timer >= 2:  # Add particles every 2 frames
            self.exhaust_timer = 0
            
            # Add 1-3 new particles
            for _ in range(random.randint(1, 3)):
                # Calculate position at the bottom center of the spaceship
                x = self.player_pos[0] + random.randint(-5, 5)  # Add some randomness
                y = self.player_pos[1] + self.player_size[1]//2 - 5
                
                # Create new particle
                self.exhaust_particles.append({
                    'x': x,
                    'y': y,
                    'dx': random.uniform(-0.5, 0.5),  # Horizontal spread
                    'dy': random.uniform(2, 4),       # Downward speed
                    'size': random.uniform(3, 6),     # Particle size
                    'alpha': 255,                     # Start fully opaque
                    'color': random.choice(self.exhaust_colors)  # Random fire color
                })
        
        # Update existing particles
        for particle in self.exhaust_particles[:]:
            # Move particle
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            
            # Fade out
            particle['alpha'] -= 8
            
            # Slowly decrease size
            particle['size'] -= 0.1
            
            # Remove faded particles
            if particle['alpha'] <= 0 or particle['size'] <= 0:
                self.exhaust_particles.remove(particle)
        
        # Limit number of particles for performance
        while len(self.exhaust_particles) > self.exhaust_max_particles:
            self.exhaust_particles.pop(0)

    def update(self):
        """Update game state for the current frame."""
        # Skip all game updates during briefing or if game hasn't started
        if self.in_briefing or not self.game_started:
            return
            
        if self.is_game_over:
            # When game is over, just update the fade-in effect
            self.game_over_alpha = min(180, self.game_over_alpha + 3)
            return
        
        # Handle continuous shooting when spacebar is held down
        if self.is_shooting and self.shooting_cooldown <= 0:
            # Create a bullet
            self.player_bullets.append([self.player_pos[0], self.player_pos[1] - 20, 10])
            
            # Play shooting sound
            self.assets.play_sound('shoot')
            
            # Set cooldown (lower value = faster firing rate)
            self.shooting_cooldown = 5  # Reduced from 10 to 5 for faster firing rate
        
        # Update shooting cooldown
        if self.shooting_cooldown > 0:
            self.shooting_cooldown -= 1
            
        # Update player position based on input method
        if self.use_mouse_control:
            # Get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Calculate smooth movement toward mouse position
            move_speed = self.player_speed
            
            # Limit how far the ship can move in a single frame
            max_move = self.player_speed
            
            # Calculate direction to mouse
            dx = mouse_x - self.player_pos[0]
            dy = mouse_y - self.player_pos[1]
            
            # Apply movement with limits
            if abs(dx) > 5:  # Small deadzone to prevent jitter
                self.player_pos[0] += max(min(dx, max_move), -max_move)
            if abs(dy) > 5:  # Small deadzone to prevent jitter
                self.player_pos[1] += max(min(dy, max_move), -max_move)
                
            # Ensure player stays within screen bounds
            self.player_pos[0] = max(self.player_size[0]//2, min(SCREEN_WIDTH - self.player_size[0]//2, self.player_pos[0]))
            self.player_pos[1] = max(self.player_size[1]//2, min(SCREEN_HEIGHT - self.player_size[1]//2, self.player_pos[1]))
        else:
            # Keyboard controls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.player_pos[0] > self.player_size[0]//2:
                self.player_pos[0] -= self.player_speed
            if keys[pygame.K_RIGHT] and self.player_pos[0] < SCREEN_WIDTH - self.player_size[0]//2:
                self.player_pos[0] += self.player_speed
            if keys[pygame.K_UP] and self.player_pos[1] > self.player_size[1]//2:
                self.player_pos[1] -= self.player_speed
            if keys[pygame.K_DOWN] and self.player_pos[1] < SCREEN_HEIGHT - self.player_size[1]//2:
                self.player_pos[1] += self.player_speed
        
        # Update fire exhaust effect
        self.update_exhaust_effect()
        
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
        
        # Spawn enemies
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_delay:
            self.enemy_spawn_timer = 0
            self.spawn_enemy()
        
        # Update enemies
        for enemy in self.enemies[:]:
            self.update_enemy_behavior(enemy)
            self.update_enemy_shooting(enemy)
            
            # Check collision with player
            player_rect = pygame.Rect(
                self.player_pos[0] - self.player_size[0]//2,
                self.player_pos[1] - self.player_size[1]//2,
                self.player_size[0],
                self.player_size[1]
            )
            if player_rect.colliderect(enemy['rect']):
                # Create explosion at collision point
                self.create_explosion(
                    enemy['rect'].centerx,
                    enemy['rect'].centery,
                    size=50,  # Larger explosion for direct collision
                    color=RED
                )
                self.enemies.remove(enemy)
                self.player_health -= 10
                self.assets.play_sound('explosion')
                if self.player_health <= 0:
                    self.is_game_over = True
                    self.player_health = 0
                    if self.music_enabled:
                        self.assets.stop_all_music()
                break
            
            # Remove enemies that are far off screen
            if (enemy['rect'].top > SCREEN_HEIGHT + 50 or 
                enemy['rect'].bottom < -50 or 
                enemy['rect'].left > SCREEN_WIDTH + 50 or 
                enemy['rect'].right < -50):
                self.enemies.remove(enemy)
        
        # Update enemy bullets with new velocity system
        for bullet in self.enemy_bullets[:]:
            bullet[0] += bullet[2]  # Update x position with x velocity
            bullet[1] += bullet[3]  # Update y position with y velocity
            
            # Remove bullets that are off screen
            if (bullet[1] > SCREEN_HEIGHT or bullet[1] < 0 or 
                bullet[0] > SCREEN_WIDTH or bullet[0] < 0):
                self.enemy_bullets.remove(bullet)
            else:
                # Check collision with player
                bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 5)
                player_rect = pygame.Rect(
                    self.player_pos[0] - self.player_size[0]//2,
                    self.player_pos[1] - self.player_size[1]//2,
                    self.player_size[0],
                    self.player_size[1]
                )
                if bullet_rect.colliderect(player_rect):
                    self.enemy_bullets.remove(bullet)
                    self.player_health -= 10
                    self.assets.play_sound('explosion')
                    if self.player_health <= 0:
                        self.is_game_over = True
                        self.player_health = 0
                        if self.music_enabled:
                            self.assets.stop_all_music()
        
        # Update power-up timer and spawning
        if not self.power_up and not self.has_missiles:
            self.power_up_timer -= 1
            if self.power_up_timer <= 0:
                self.spawn_power_up()
                self.power_up_timer = 300  # Reset timer
        
        # Check power-up collection
        if self.power_up:
            player_rect = pygame.Rect(
                self.player_pos[0] - self.player_size[0]//2,
                self.player_pos[1] - self.player_size[1]//2,
                self.player_size[0],
                self.player_size[1]
            )
            if player_rect.colliderect(self.power_up['rect']):
                self.has_missiles = True
                self.missile_shots = 0
                self.power_up = None
                self.assets.play_sound('explosion')  # Use explosion sound for power-up
        
        # Update health pack timer and spawning
        if not self.health_pack and self.player_health < 100:  # Only spawn if player isn't at full health
            self.health_pack_timer -= 1
            if self.health_pack_timer <= 0:
                self.spawn_health_pack()
                self.health_pack_timer = 600  # Reset timer
        
        # Check health pack collection
        if self.health_pack:
            player_rect = pygame.Rect(
                self.player_pos[0] - self.player_size[0]//2,
                self.player_pos[1] - self.player_size[1]//2,
                self.player_size[0],
                self.player_size[1]
            )
            if player_rect.colliderect(self.health_pack['rect']):
                self.player_health = min(100, self.player_health + self.health_recovery)
                self.health_pack = None
                self.assets.play_sound('explosion')  # Use explosion sound for pickup
        
        # Update explosions
        self.update_explosions()
        
        # Update missiles
        self.update_missiles()

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
            
            # Draw instructions during briefing
            mute_text = "Press M to toggle music"
            mute_surface = self.font.render(mute_text, True, WHITE)
            screen.blit(mute_surface, (10, SCREEN_HEIGHT - 40))
            
            space_text = "Press SPACE to continue | Press ESC to skip briefing"
            space_surface = self.font.render(space_text, True, WHITE)
            space_rect = space_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
            screen.blit(space_surface, space_rect)
        else:
            # Draw background
            screen.fill(DARK_BLUE)  # Dark blue space background
            
            # Draw background stars with smooth twinkling
            for star in self.stars:
                # Calculate twinkling effect using sine wave
                brightness_offset = math.sin(star['twinkle_offset'] + pygame.time.get_ticks() * star['twinkle_speed']) * 25
                brightness = min(255, max(100, star['base_brightness'] + brightness_offset))
                pygame.draw.circle(screen, (brightness, brightness, brightness), 
                                (int(star['x']), int(star['y'])), star['size'])
            
            # Draw map objects with stable rendering
            for obj in self.map_objects:
                if obj['type'] == 'asteroid':
                    # Use pre-calculated points for asteroid shape
                    pygame.draw.polygon(screen, obj['color'], obj['points'])
                    # Draw pre-calculated craters
                    for crater in obj['craters']:
                        pygame.draw.circle(screen, (50, 50, 50), 
                                        (crater['x'] + obj['rect'].x, crater['y'] + obj['rect'].y), 
                                        crater['size'])
                
                elif obj['type'] == 'galaxy':
                    # Draw pre-calculated spiral points
                    for point in obj['spiral_points']:
                        x = point['x'] + obj['rect'].x
                        y = point['y'] + obj['rect'].y
                        pygame.draw.circle(screen, obj['color'], (int(x), int(y)), point['size'])
                    # Add stable bright center
                    pygame.draw.circle(screen, WHITE, obj['rect'].center, obj['rect'].width // 8)
                
                else:  # nebula
                    # Use pre-rendered nebula surface
                    screen.blit(obj['surface'], obj['rect'])
                    
            # Draw fire exhaust effect behind the player
            for particle in self.exhaust_particles:
                # Create a surface for the particle with alpha channel
                particle_surface = pygame.Surface((int(particle['size'] * 2), int(particle['size'] * 2)), pygame.SRCALPHA)
                # Draw the particle with its current alpha value
                pygame.draw.circle(
                    particle_surface, 
                    (*particle['color'], int(particle['alpha'])), 
                    (int(particle['size']), int(particle['size'])), 
                    int(particle['size'])
                )
                # Draw the particle at its position
                screen.blit(
                    particle_surface, 
                    (int(particle['x'] - particle['size']), int(particle['y'] - particle['size']))
                )

            # Draw player
            player_image = self.assets.get_image('player')
            # Scale the spaceship image to the desired size
            player_image = pygame.transform.scale(player_image, self.player_size)
            # Center the image on the player position
            player_rect = player_image.get_rect(center=(self.player_pos[0], self.player_pos[1]))
            screen.blit(player_image, player_rect)
            
            # Draw player bullets with anti-aliasing
            for bullet in self.player_bullets:
                # Draw a glowing effect for bullets
                glow_radius = 8
                for r in range(glow_radius, 0, -2):
                    alpha = int(100 * (r / glow_radius))
                    glow_surface = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
                    pygame.draw.circle(glow_surface, (*YELLOW, alpha), (r, r), r)
                    screen.blit(glow_surface, (bullet[0] - r + 2, bullet[1] - r + 5))
                # Draw the main bullet
                pygame.draw.rect(screen, YELLOW, (bullet[0], bullet[1], 5, 10))
            
            # Draw enemies
            enemy_image = self.assets.get_image('enemy')
            for enemy in self.enemies:
                screen.blit(enemy_image, enemy['rect'])
            
            # Draw enemy bullets with red glow
            for bullet in self.enemy_bullets:
                # Draw a glowing effect for enemy bullets
                glow_radius = 6
                for r in range(glow_radius, 0, -2):
                    alpha = int(80 * (r / glow_radius))
                    glow_surface = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
                    pygame.draw.circle(glow_surface, (*RED, alpha), (r, r), r)
                    screen.blit(glow_surface, (bullet[0] - r + 2, bullet[1] - r + 5))
                # Draw the main bullet
                pygame.draw.rect(screen, RED, (bullet[0], bullet[1], 5, 10))
            
            # Draw score
            score_text = f"Score: {self.score}"
            score_surface = self.font.render(score_text, True, WHITE)
            screen.blit(score_surface, (10, 10))
            
            # Draw health
            health_text = f"Health: {self.player_health}"
            health_surface = self.font.render(health_text, True, WHITE)
            screen.blit(health_surface, (10, 50))
            
            # Draw music toggle reminder
            mute_text = "Press M to toggle music"
            mute_surface = self.font.render(mute_text, True, WHITE)
            screen.blit(mute_surface, (10, SCREEN_HEIGHT - 40))
            
            # Draw power-up if active
            if self.power_up:
                # Draw glowing effect
                self.power_up['angle'] += 0.05
                self.power_up['glow_offset'] = (self.power_up['glow_offset'] + 0.1) % (2 * math.pi)
                
                glow_radius = 20 + math.sin(self.power_up['glow_offset']) * 5
                for r in range(int(glow_radius), 0, -2):
                    alpha = int(100 * (r / glow_radius))
                    glow_surface = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
                    pygame.draw.circle(glow_surface, (255, 215, 0, alpha), (r, r), r)
                    screen.blit(glow_surface, (
                        self.power_up['rect'].centerx - r,
                        self.power_up['rect'].centery - r
                    ))
                
                # Draw missile icon
                missile_points = [
                    (self.power_up['rect'].centerx, self.power_up['rect'].top),
                    (self.power_up['rect'].right, self.power_up['rect'].bottom),
                    (self.power_up['rect'].centerx, self.power_up['rect'].centery + 5),
                    (self.power_up['rect'].left, self.power_up['rect'].bottom)
                ]
                pygame.draw.polygon(screen, (255, 215, 0), missile_points)
            
            # Draw explosions
            for explosion in self.explosions:
                # Draw main explosion
                explosion_surface = pygame.Surface((explosion['radius']*2, explosion['radius']*2), pygame.SRCALPHA)
                pygame.draw.circle(
                    explosion_surface,
                    (*explosion['color'], explosion['alpha']),
                    (explosion['radius'], explosion['radius']),
                    explosion['radius']
                )
                screen.blit(explosion_surface, (
                    explosion['x'] - explosion['radius'],
                    explosion['y'] - explosion['radius']
                ))
                
                # Draw particles
                for particle in explosion['particles']:
                    if particle['life'] > 0:
                        pygame.draw.circle(
                            screen,
                            (*explosion['color'], particle['life']),
                            (int(particle['x']), int(particle['y'])),
                            particle['size']
                        )
            
            # Draw missiles with trail effect
            for missile in self.missiles:
                # Draw missile trail
                trail_length = 20
                for i in range(trail_length):
                    alpha = int(200 * (1 - i/trail_length))
                    trail_pos = [
                        int(missile['pos'][0] - i * missile['velocity'][0] * 0.5),
                        int(missile['pos'][1] - i * missile['velocity'][1] * 0.5)
                    ]
                    trail_surface = pygame.Surface((6, 6), pygame.SRCALPHA)
                    pygame.draw.circle(trail_surface, (255, 200, 0, alpha), (3, 3), 3)
                    screen.blit(trail_surface, (trail_pos[0] - 3, trail_pos[1] - 3))
                
                # Draw missile body
                missile_surface = pygame.Surface((12, 20), pygame.SRCALPHA)
                missile_color = (255, 215, 0)  # Golden yellow
                # Draw missile body
                pygame.draw.polygon(missile_surface, missile_color, [(6, 0), (12, 20), (6, 15), (0, 20)])
                # Rotate missile based on its angle
                rotated_missile = pygame.transform.rotate(missile_surface, math.degrees(missile['angle']))
                screen.blit(rotated_missile, (
                    missile['pos'][0] - rotated_missile.get_width()//2,
                    missile['pos'][1] - rotated_missile.get_height()//2
                ))
            
            # Draw control mode indicator
            control_text = "Control: Mouse (Press C to toggle)" if self.use_mouse_control else "Control: Keyboard (Press C to toggle)"
            control_surface = self.font.render(control_text, True, WHITE)
            # Update position to bottom right
            control_rect = control_surface.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 10))
            screen.blit(control_surface, control_rect)
            
            # Draw missile control instructions
            if self.has_missiles:
                if self.use_mouse_control:
                    missile_text = f"Missiles: {self.max_missiles - self.missile_shots} (Right-click to fire)"
                else:
                    missile_text = f"Missiles: {self.max_missiles - self.missile_shots} (Press S to fire)"
                missile_surface = self.font.render(missile_text, True, (255, 215, 0))  # Golden yellow
                # Update position to bottom right
                missile_rect = missile_surface.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 50))
                screen.blit(missile_surface, missile_rect)
            
            # Draw health pack if active
            if self.health_pack:
                # Update animation values
                self.health_pack['blink_offset'] = (self.health_pack['blink_offset'] + 0.1) % (2 * math.pi)
                self.health_pack['rotation'] = (self.health_pack['rotation'] + 0.5) % 360
                
                # Calculate blink alpha
                blink_alpha = int(200 + math.sin(self.health_pack['blink_offset']) * 55)  # Oscillate between 145 and 255
                
                # Draw glowing red background
                glow_radius = self.health_pack_size
                glow_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
                for r in range(glow_radius, 0, -2):
                    alpha = int(blink_alpha * (r / glow_radius) * 0.5)
                    pygame.draw.circle(glow_surface, (255, 0, 0, alpha), (glow_radius, glow_radius), r)
                screen.blit(glow_surface, (
                    self.health_pack['rect'].centerx - glow_radius,
                    self.health_pack['rect'].centery - glow_radius
                ))
                
                # Draw red cross
                cross_surface = pygame.Surface((self.health_pack_size, self.health_pack_size), pygame.SRCALPHA)
                # Vertical bar of cross
                pygame.draw.rect(cross_surface, (255, 0, 0, blink_alpha),
                               (self.health_pack_size//2 - 4, 2, 8, self.health_pack_size-4))
                # Horizontal bar of cross
                pygame.draw.rect(cross_surface, (255, 0, 0, blink_alpha),
                               (2, self.health_pack_size//2 - 4, self.health_pack_size-4, 8))
                
                # Rotate the cross
                rotated_cross = pygame.transform.rotate(cross_surface, self.health_pack['rotation'])
                screen.blit(rotated_cross, (
                    self.health_pack['rect'].centerx - rotated_cross.get_width()//2,
                    self.health_pack['rect'].centery - rotated_cross.get_height()//2
                ))

            # Draw game over screen if game is over
            if self.is_game_over:
                # Create transparent red overlay
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((255, 0, 0, self.game_over_alpha))
                screen.blit(overlay, (0, 0))
                
                # Draw "GAME OVER" text
                game_over_font = pygame.font.Font(None, 74)
                game_over_text = game_over_font.render("GAME OVER", True, WHITE)
                text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
                screen.blit(game_over_text, text_rect)
                
                # Draw final score
                score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
                score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
                screen.blit(score_text, score_rect)
                
                # Draw instruction to return to menu
                menu_text = self.font.render("Press ESC to return to menu", True, WHITE)
                menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
                screen.blit(menu_text, menu_rect)

    def reset(self):
        """Reset the game state."""
        # Player properties
        self.player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100]
        self.player_speed = 5
        self.player_health = 100
        self.player_rect = pygame.Rect(0, 0, 50, 50)  # Will be updated in draw
        self.player_invincible = False
        self.player_invincible_timer = 0
        self.shooting_cooldown = 0  # Cooldown timer for continuous shooting
        self.is_shooting = False  # Flag to track if spacebar is held down
        self.player_bullets = []
        self.shoot_cooldown = 0
        self.shoot_delay = 15
        self.player_size = (64, 64)
        self.has_missiles = False  # Track if player has missile power-up
        self.missile_shots = 0  # Count of missiles shot
        self.max_missiles = 5  # Maximum number of missiles per power-up
        
        # Fire exhaust effect properties
        self.exhaust_particles = []
        self.exhaust_timer = 0
        self.exhaust_colors = [(255, 165, 0), (255, 140, 0), (255, 69, 0), (255, 0, 0)]  # Orange to red gradient
        self.exhaust_max_particles = 20
        
        # Power-up properties
        self.power_up = None
        self.power_up_timer = 300  # Start spawning after 5 seconds (60 FPS * 5)
        self.power_up_size = 30
        
        # Missile properties
        self.missiles = []  # List to track heat-seeking missiles
        self.explosions = []  # List to track explosion effects
        
        # Enemy properties
        self.enemies = []
        self.enemy_bullets = []
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 60  # Frames between enemy spawns
        self.enemy_behaviors = ['chase', 'zigzag', 'circle', 'ambush']  # Different movement patterns
        
        # Map properties
        self.map_scroll = 0
        self.scroll_speed = 2
        self.map_objects = []  # List of space objects (asteroids, stars, galaxies)
        self.generate_map_objects()
        
        # Create stable background stars with fixed properties
        self.stars = []
        for _ in range(100):
            self.stars.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.choice([1, 1, 2]),  # More small stars than large
                'brightness': random.randint(150, 255),
                'twinkle_speed': random.uniform(0.02, 0.1),
                'twinkle_offset': random.uniform(0, 2 * math.pi),
                'base_brightness': random.randint(150, 255)
            })
        
        # Health pack properties
        self.health_pack = None
        self.health_pack_timer = 600  # Start spawning after 10 seconds (60 FPS * 10)
        self.health_pack_size = 30
        self.health_recovery = 50  # Amount of health recovered

    def fire_missile(self):
        """Fire a missile if the player has any available"""
        if self.has_missiles and self.missile_shots < self.max_missiles:
            # Find closest enemy for initial direction
            closest_enemy = None
            closest_dist = float('inf')
            for enemy in self.enemies:
                if (0 <= enemy['rect'].right <= SCREEN_WIDTH and 
                    0 <= enemy['rect'].bottom <= SCREEN_HEIGHT):
                    dx = enemy['rect'].centerx - self.player_pos[0]
                    dy = enemy['rect'].centery - self.player_pos[1]
                    dist = (dx * dx + dy * dy) ** 0.5
                    if dist < closest_dist:
                        closest_dist = dist
                        closest_enemy = enemy

            # Calculate initial velocity towards closest enemy or straight up if no enemies
            initial_velocity = [0, -8]
            initial_angle = -math.pi/2  # Default to straight up
            if closest_enemy:
                dx = closest_enemy['rect'].centerx - self.player_pos[0]
                dy = closest_enemy['rect'].centery - self.player_pos[1]
                angle = math.atan2(-dy, dx)
                initial_velocity = [
                    math.cos(angle) * 8,
                    -math.sin(angle) * 8
                ]
                initial_angle = angle - math.pi/2

            # Shoot a heat-seeking missile
            self.missiles.append({
                'pos': [self.player_pos[0], self.player_pos[1] - 20],
                'velocity': initial_velocity,
                'target': closest_enemy,
                'turn_speed': 0.15,
                'speed': 8,
                'angle': initial_angle,
                'miss_timer': 0
            })
            self.missile_shots += 1
            if self.missile_shots >= self.max_missiles:
                self.has_missiles = False
                self.missile_shots = 0
                
            # Play missile launch sound
            self.assets.play_sound('missile_launch')
