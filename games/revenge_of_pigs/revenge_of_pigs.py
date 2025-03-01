import pygame
import pymunk
import math
import sys
import os
import random
import json
from pygame.locals import *

def run_game():
    # Initialize Pygame and Pymunk
    WIDTH = 1200
    HEIGHT = 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Revenge of the Pigs!")

    # Create assets directory if it doesn't exist
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)

    # Load and scale background image
    try:
        # Try to load the new AI-generated background first
        background = pygame.image.load(os.path.join(assets_dir, 'background_enhanced_ai.png'))
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    except:
        try:
            # Fall back to original background if AI background fails
            background = pygame.image.load(os.path.join(assets_dir, 'background.png'))
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        except:
            # Final fallback to gradient background
            background = pygame.Surface((WIDTH, HEIGHT))
            for y in range(HEIGHT):
                # Create gradient from light blue to darker blue
                if y < HEIGHT - 50:  # Sky
                    color = (135 - y//10, 206 - y//10, 235 - y//10)
                else:  # Ground
                    color = (34, 139, 34)  # Forest green
                pygame.draw.line(background, color, (0, y), (WIDTH, y))

    # Load character images
    pig_image = pygame.image.load(os.path.join(assets_dir, 'pig.png'))
    angry_bird_image = pygame.image.load(os.path.join(assets_dir, 'angry_bird.png'))

    # Physics setup
    space = pymunk.Space()
    space.gravity = (0, 900)  # Vertical gravity

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BROWN = (139, 69, 19)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)
    MENU_BLUE = (100, 149, 237)  # Cornflower blue for menu
    SELECTED_BLUE = (65, 105, 225)  # Royal blue for selected items

    class Particle:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 10)
            self.dx = math.cos(angle) * speed
            self.dy = math.sin(angle) * speed
            self.lifetime = random.randint(20, 40)
            self.color = random.choice([RED, YELLOW, ORANGE])
            self.size = random.randint(2, 6)
            
        def update(self):
            self.x += self.dx
            self.y += self.dy
            self.dy += 0.5  # Gravity effect
            self.lifetime -= 1
            
        def draw(self, screen):
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

    class Explosion:
        def __init__(self, x, y):
            self.particles = [Particle(x, y) for _ in range(30)]
            
        def update(self):
            for particle in self.particles:
                particle.update()
            self.particles = [p for p in self.particles if p.lifetime > 0]
            
        def draw(self, screen):
            for particle in self.particles:
                particle.draw(screen)
            
        @property
        def is_alive(self):
            return len(self.particles) > 0

    class Pig:
        def __init__(self, x, y):
            self.mass = 5
            self.radius = 20
            self.moment = pymunk.moment_for_circle(self.mass, 0, self.radius)
            self.initial_pos = (x, y)
            self.create_body()
            
        def create_body(self, body_type=pymunk.Body.KINEMATIC):
            self.body = pymunk.Body(self.mass, self.moment, body_type=body_type)
            self.body.position = self.initial_pos
            self.shape = pymunk.Circle(self.body, self.radius)
            self.shape.elasticity = 0.95
            self.shape.friction = 1.0
            self.shape.collision_type = 1
            space.add(self.body, self.shape)
            self.launched = False
            
        def draw(self, screen):
            try:
                x = int(self.body.position.x)
                y = int(self.body.position.y)
                if not (math.isnan(x) or math.isnan(y)):
                    # Draw the pig image instead of a circle
                    screen.blit(pig_image, (x - self.radius, y - self.radius))
                    # Rotate the pig based on velocity
                    if self.launched and (self.body.velocity.x != 0 or self.body.velocity.y != 0):
                        angle = math.degrees(math.atan2(self.body.velocity.y, self.body.velocity.x))
                        rotated_pig = pygame.transform.rotate(pig_image, -angle)
                        new_rect = rotated_pig.get_rect(center=(x, y))
                        screen.blit(rotated_pig, new_rect.topleft)
                    else:
                        screen.blit(pig_image, (x - self.radius, y - self.radius))
                else:
                    self.reset()
            except (ValueError, AttributeError):
                self.reset()
            
        def reset(self):
            try:
                space.remove(self.body, self.shape)
            except:
                pass
            self.create_body(pymunk.Body.KINEMATIC)
            
        def launch(self, impulse):
            current_pos = self.body.position
            try:
                space.remove(self.body, self.shape)
            except:
                pass
            self.body = pymunk.Body(self.mass, self.moment, body_type=pymunk.Body.DYNAMIC)
            self.body.position = current_pos
            self.shape = pymunk.Circle(self.body, self.radius)
            self.shape.elasticity = 0.95
            self.shape.friction = 1.0
            self.shape.collision_type = 1
            space.add(self.body, self.shape)
            self.launched = True
            self.body.apply_impulse_at_local_point(impulse)

    class AngryBirdBlock:
        def __init__(self, x, y, width, height):
            self.mass = 1
            self.width = width
            self.height = height
            self.body = pymunk.Body(self.mass, pymunk.moment_for_box(self.mass, (width, height)))
            self.body.position = x, y
            self.shape = pymunk.Poly.create_box(self.body, (width, height))
            self.shape.elasticity = 0.4
            self.shape.friction = 0.8
            self.shape.collision_type = 2
            self.destroyed = False

        def draw(self, screen):
            if not self.destroyed:
                vertices = [self.body.local_to_world(v) for v in self.shape.get_vertices()]
                x = int(self.body.position.x)
                y = int(self.body.position.y)
                angle = math.degrees(self.body.angle)
                rotated_bird = pygame.transform.rotate(angry_bird_image, -angle)
                new_rect = rotated_bird.get_rect(center=(x, y))
                screen.blit(rotated_bird, new_rect.topleft)

    class WoodenBlock:
        def __init__(self, x, y, width, height):
            self.mass = 2  # Heavier than birds
            self.width = width
            self.height = height
            self.body = pymunk.Body(self.mass, pymunk.moment_for_box(self.mass, (width, height)))
            self.body.position = x, y
            self.shape = pymunk.Poly.create_box(self.body, (width, height))
            self.shape.elasticity = 0.2  # Less bouncy than birds
            self.shape.friction = 1.0    # More friction
            self.shape.collision_type = 3  # New collision type for wood
            self.color = (139, 69, 19)   # Brown color for wood
            self.destroyed = False
            self.health = 3  # Takes 3 hits to destroy

        def draw(self, screen):
            if not self.destroyed:
                vertices = [self.body.local_to_world(v) for v in self.shape.get_vertices()]
                # Draw wood texture (diagonal lines)
                pygame.draw.polygon(screen, self.color, vertices)
                # Add wood grain lines
                center = self.body.position
                angle = math.degrees(self.body.angle)
                for offset in range(-int(self.width/2), int(self.width/2), 8):
                    start = (center[0] + offset, center[1] - self.height/2)
                    end = (center[0] + offset, center[1] + self.height/2)
                    rotated_start = self._rotate_point(start, center, angle)
                    rotated_end = self._rotate_point(end, center, angle)
                    pygame.draw.line(screen, (101, 67, 33), rotated_start, rotated_end, 1)

        def _rotate_point(self, point, center, angle):
            angle_rad = math.radians(angle)
            dx = point[0] - center[0]
            dy = point[1] - center[1]
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)
            new_dx = dx * cos_a - dy * sin_a
            new_dy = dx * sin_a + dy * cos_a
            return (center[0] + new_dx, center[1] + new_dy)

        def damage(self):
            self.health -= 1
            # Darken color as it takes damage
            self.color = (max(89, 139 - (3 - self.health) * 20), 
                         max(39, 69 - (3 - self.health) * 10), 
                         max(9, 19 - (3 - self.health) * 5))
            if self.health <= 0:
                self.destroyed = True
                return True
            return False

    class Slingshot:
        def __init__(self, x, y):
            self.pos = (x, y)
            # Colors for the slingshot
            self.wood_color = (139, 69, 19)  # Brown
            self.dark_wood = (101, 67, 33)   # Dark brown
            self.band_color = (60, 60, 60)   # Dark gray for rubber band
            # Dimensions
            self.fork_length = 80  # Length of Y arms
            self.base_height = 100  # Height of the base
            self.thickness = 12     # Thickness of the wood
            self.band_thickness = 4 # Thickness of the rubber band
            # Angles
            self.left_angle = 30   # Angle for left fork
            self.right_angle = -30 # Angle for right fork
            self.base_angle = 0    # Angle for the main trunk
            
        def draw(self, screen, pig_pos=None):
            x, y = self.pos
            
            # Draw base trunk
            pygame.draw.rect(screen, self.dark_wood, 
                            (x - self.thickness//2, y - self.base_height, 
                             self.thickness, self.base_height))
            
            # Calculate fork positions
            fork_base_x = x
            fork_base_y = y - self.base_height
            
            # Draw left fork
            left_angle_rad = math.radians(self.left_angle)
            left_end_x = fork_base_x + math.sin(left_angle_rad) * self.fork_length
            left_end_y = fork_base_y - math.cos(left_angle_rad) * self.fork_length
            pygame.draw.line(screen, self.dark_wood, 
                            (fork_base_x, fork_base_y),
                            (left_end_x, left_end_y), self.thickness)
            
            # Draw right fork
            right_angle_rad = math.radians(self.right_angle)
            right_end_x = fork_base_x + math.sin(right_angle_rad) * self.fork_length
            right_end_y = fork_base_y - math.cos(right_angle_rad) * self.fork_length
            pygame.draw.line(screen, self.dark_wood, 
                            (fork_base_x, fork_base_y),
                            (right_end_x, right_end_y), self.thickness)
            
            # Draw rubber bands
            if pig_pos:
                # Draw stretched rubber bands
                pygame.draw.line(screen, self.band_color, 
                               (left_end_x, left_end_y), pig_pos, self.band_thickness)
                pygame.draw.line(screen, self.band_color, 
                               (right_end_x, right_end_y), pig_pos, self.band_thickness)
            else:
                # Draw relaxed rubber band
                center_x = (left_end_x + right_end_x) / 2
                center_y = (left_end_y + right_end_y) / 2 + 20
                pygame.draw.line(screen, self.band_color, 
                               (left_end_x, left_end_y), 
                               (center_x, center_y), self.band_thickness)
                pygame.draw.line(screen, self.band_color, 
                               (right_end_x, right_end_y), 
                               (center_x, center_y), self.band_thickness)

    class Menu:
        def __init__(self):
            self.options = ["Play", "Level Editor", "Credits", "Quit"]
            self.selected = 0
            self.font = pygame.font.Font(None, 74)
            self.small_font = pygame.font.Font(None, 36)
            self.state = "menu"  # menu, game, editor, credits
            
        def draw(self, screen):
            if self.state == "menu":
                # Draw title
                title = self.font.render("Revenge of the Pigs!", True, WHITE)
                title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
                screen.blit(title, title_rect)
                
                # Draw menu options
                for i, option in enumerate(self.options):
                    color = SELECTED_BLUE if i == self.selected else MENU_BLUE
                    text = self.font.render(option, True, color)
                    rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + i * 80))
                    screen.blit(text, rect)
                    
            elif self.state == "credits":
                # Draw credits
                credits = [
                    "Credits",
                    "",
                    "Game created by Claude AI",
                    "A powerful AI assistant by Anthropic",
                    "",
                    "Developed in Cursor IDE",
                    "",
                    "Press ESC to return to menu"
                ]
                
                for i, line in enumerate(credits):
                    if i == 0:  # Title
                        text = self.font.render(line, True, WHITE)
                    else:  # Regular text
                        text = self.small_font.render(line, True, WHITE)
                    rect = text.get_rect(center=(WIDTH//2, HEIGHT//4 + i * 50))
                    screen.blit(text, rect)
        
        def handle_input(self, event):
            if self.state == "menu":
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == K_RETURN:
                        if self.options[self.selected] == "Play":
                            self.state = "game"
                        elif self.options[self.selected] == "Level Editor":
                            self.state = "editor"
                        elif self.options[self.selected] == "Credits":
                            self.state = "credits"
                        elif self.options[self.selected] == "Quit":
                            return False
            elif self.state == "credits":
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    self.state = "menu"
            
            return True

    class LevelEditor:
        def __init__(self, screen, space, assets_dir):
            self.screen = screen
            self.space = space
            self.assets_dir = assets_dir
            self.blocks = []
            self.selected_type = "bird"  # "bird" or "wood"
            self.grid_size = 50  # Size of placement grid
            self.font = pygame.font.Font(None, 36)
            self.toolbar_height = 60
            self.buttons = [
                {"text": "Bird", "rect": pygame.Rect(10, 10, 100, 40), "type": "bird"},
                {"text": "Wood", "rect": pygame.Rect(120, 10, 100, 40), "type": "wood"},
                {"text": "Clear", "rect": pygame.Rect(230, 10, 100, 40), "type": "clear"},
                {"text": "Save", "rect": pygame.Rect(340, 10, 100, 40), "type": "save"},
                {"text": "Load", "rect": pygame.Rect(450, 10, 100, 40), "type": "load"},
                {"text": "Play", "rect": pygame.Rect(560, 10, 100, 40), "type": "play"}
            ]
            
        def draw_toolbar(self):
            # Draw toolbar background
            pygame.draw.rect(self.screen, (50, 50, 50), (0, 0, WIDTH, self.toolbar_height))
            
            # Draw buttons
            for button in self.buttons:
                color = SELECTED_BLUE if button["type"] == self.selected_type else MENU_BLUE
                pygame.draw.rect(self.screen, color, button["rect"])
                text = self.font.render(button["text"], True, WHITE)
                text_rect = text.get_rect(center=button["rect"].center)
                self.screen.blit(text, text_rect)
        
        def draw_grid(self):
            # Draw placement grid
            for x in range(0, WIDTH, self.grid_size):
                pygame.draw.line(self.screen, (100, 100, 100), (x, self.toolbar_height), (x, HEIGHT), 1)
            for y in range(self.toolbar_height, HEIGHT, self.grid_size):
                pygame.draw.line(self.screen, (100, 100, 100), (0, y), (WIDTH, y), 1)
        
        def handle_click(self, pos):
            # Check toolbar buttons
            if pos[1] < self.toolbar_height:
                for button in self.buttons:
                    if button["rect"].collidepoint(pos):
                        if button["type"] in ["bird", "wood"]:
                            self.selected_type = button["type"]
                        elif button["type"] == "clear":
                            self.clear_blocks()
                        elif button["type"] == "save":
                            self.save_level()
                        elif button["type"] == "load":
                            self.load_level()
                        elif button["type"] == "play":
                            return "play"
                return None
            
            # Place block on grid
            grid_x = (pos[0] // self.grid_size) * self.grid_size + self.grid_size // 2
            grid_y = (pos[1] // self.grid_size) * self.grid_size + self.grid_size // 2
            
            # Don't place blocks too close to slingshot
            if grid_x < 300:  # Safe zone for slingshot
                return None
                
            # Create new block
            if self.selected_type == "bird":
                block = AngryBirdBlock(grid_x, grid_y, self.grid_size, self.grid_size)
            else:
                block = WoodenBlock(grid_x, grid_y, self.grid_size, self.grid_size)
            
            # Remove any existing block at this position
            self.remove_block_at(grid_x, grid_y)
            
            # Add the new block
            self.blocks.append(block)
            self.space.add(block.body, block.shape)
            return None
        
        def remove_block_at(self, x, y):
            for block in self.blocks[:]:
                if (abs(block.body.position.x - x) < self.grid_size/2 and 
                    abs(block.body.position.y - y) < self.grid_size/2):
                    self.space.remove(block.body, block.shape)
                    self.blocks.remove(block)
        
        def clear_blocks(self):
            for block in self.blocks:
                self.space.remove(block.body, block.shape)
            self.blocks.clear()
        
        def save_level(self):
            level_data = []
            for block in self.blocks:
                block_data = {
                    "type": "bird" if isinstance(block, AngryBirdBlock) else "wood",
                    "x": block.body.position.x,
                    "y": block.body.position.y
                }
                level_data.append(block_data)
            
            save_path = os.path.join(os.path.dirname(__file__), 'levels')
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            
            with open(os.path.join(save_path, 'level1.json'), 'w') as f:
                json.dump(level_data, f)
        
        def load_level(self):
            self.clear_blocks()
            
            try:
                load_path = os.path.join(os.path.dirname(__file__), 'levels', 'level1.json')
                with open(load_path, 'r') as f:
                    level_data = json.load(f)
                
                for block_data in level_data:
                    if block_data["type"] == "bird":
                        block = AngryBirdBlock(block_data["x"], block_data["y"], self.grid_size, self.grid_size)
                    else:
                        block = WoodenBlock(block_data["x"], block_data["y"], self.grid_size, self.grid_size)
                    self.blocks.append(block)
                    self.space.add(block.body, block.shape)
            except:
                pass  # Level file doesn't exist yet
        
        def draw(self):
            self.draw_grid()
            self.draw_toolbar()
            
            # Draw blocks
            for block in self.blocks:
                block.draw(self.screen)
            
            # Draw placement preview
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[1] > self.toolbar_height and mouse_pos[0] > 300:
                grid_x = (mouse_pos[0] // self.grid_size) * self.grid_size + self.grid_size // 2
                grid_y = (mouse_pos[1] // self.grid_size) * self.grid_size + self.grid_size // 2
                pygame.draw.rect(self.screen, (255, 255, 255, 128), 
                               (grid_x - self.grid_size/2, grid_y - self.grid_size/2, 
                                self.grid_size, self.grid_size), 2)

    # Create game objects
    SLINGSHOT_X = 100  # Move further left
    SLINGSHOT_Y = HEIGHT - 70  # Slightly above ground level
    pig = Pig(SLINGSHOT_X, SLINGSHOT_Y - 20)  # Position pig above the slingshot base

    # Create ground segments with a gap near the slingshot
    GAP_WIDTH = 200  # Width of the gap in the ground
    ground_left = pymunk.Segment(space.static_body, (0, HEIGHT - 50), (SLINGSHOT_X - GAP_WIDTH/2, HEIGHT - 50), 5)
    ground_right = pymunk.Segment(space.static_body, (SLINGSHOT_X + GAP_WIDTH/2, HEIGHT - 50), (WIDTH, HEIGHT - 50), 5)

    # Set ground properties
    for ground in [ground_left, ground_right]:
        ground.friction = 1.0
        ground.elasticity = 0.5
        space.add(ground)

    # Create angry bird blocks and wooden blocks
    blocks = []
    BLOCK_SIZE = 50
    STACK_START_X = 900
    STACK_START_Y = HEIGHT - 100

    # First layer: Bird, Wood, Bird
    blocks.append(AngryBirdBlock(STACK_START_X - BLOCK_SIZE, STACK_START_Y, BLOCK_SIZE, BLOCK_SIZE))
    blocks.append(WoodenBlock(STACK_START_X, STACK_START_Y, BLOCK_SIZE, BLOCK_SIZE))
    blocks.append(AngryBirdBlock(STACK_START_X + BLOCK_SIZE, STACK_START_Y, BLOCK_SIZE, BLOCK_SIZE))

    # Second layer: Wood, Bird, Wood
    blocks.append(WoodenBlock(STACK_START_X - BLOCK_SIZE, STACK_START_Y - BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    blocks.append(AngryBirdBlock(STACK_START_X, STACK_START_Y - BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    blocks.append(WoodenBlock(STACK_START_X + BLOCK_SIZE, STACK_START_Y - BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # Third layer: Bird, Wood, Bird
    blocks.append(AngryBirdBlock(STACK_START_X - BLOCK_SIZE, STACK_START_Y - 2 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    blocks.append(WoodenBlock(STACK_START_X, STACK_START_Y - 2 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    blocks.append(AngryBirdBlock(STACK_START_X + BLOCK_SIZE, STACK_START_Y - 2 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # Add all blocks to the physics space
    for block in blocks:
        space.add(block.body, block.shape)

    # Slingshot properties
    SLINGSHOT_POS = (SLINGSHOT_X, SLINGSHOT_Y)
    MAX_STRETCH = 100

    clock = pygame.time.Clock()
    running = True
    dragging = False
    mouse_pressed = False

    # Collision types
    COLLISION_TYPES = {
        "PIG": 1,
        "BIRD": 2
    }

    # Create explosion list
    explosions = []

    # Collision handler
    def collision_handler(arbiter, space, data):
        pig_shape = arbiter.shapes[0]
        target_shape = arbiter.shapes[1]
        
        # Find the corresponding block
        for block in blocks:
            if block.shape == target_shape and not block.destroyed:
                if isinstance(block, AngryBirdBlock):
                    block.destroyed = True
                    # Create explosion at the collision point
                    x = block.body.position.x
                    y = block.body.position.y
                    explosions.append(Explosion(x, y))
                    # Remove the bird from physics space
                    space.remove(target_shape, target_shape.body)
                elif isinstance(block, WoodenBlock):
                    # Only destroy wooden block if pig is moving fast enough
                    pig_velocity = math.sqrt(pig_shape.body.velocity.x**2 + pig_shape.body.velocity.y**2)
                    if pig_velocity > 500:  # Threshold for damage
                        if block.damage() and block.destroyed:
                            space.remove(target_shape, target_shape.body)
                break
            
        return True

    # Add collision handler after space creation
    space.add_collision_handler(COLLISION_TYPES["PIG"], COLLISION_TYPES["BIRD"]).begin = collision_handler

    # Create slingshot object (after pygame initialization)
    slingshot = Slingshot(SLINGSHOT_X, SLINGSHOT_Y)

    # Draw ground segments
    def draw_ground(screen):
        # Draw left ground segment
        pygame.draw.rect(screen, (0, 100, 0), (0, HEIGHT - 50, SLINGSHOT_X - GAP_WIDTH/2, 50))
        # Draw right ground segment
        pygame.draw.rect(screen, (0, 100, 0), (SLINGSHOT_X + GAP_WIDTH/2, HEIGHT - 50, WIDTH - (SLINGSHOT_X + GAP_WIDTH/2), 50))

    # Create menu
    menu = Menu()

    # Game loop
    running = True
    while running:
        # Draw background
        screen.blit(background, (0, 0))
        
        if menu.state == "menu" or menu.state == "credits":
            # Handle menu
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                else:
                    running = menu.handle_input(event)
            menu.draw(screen)
            
        elif menu.state == "game":
            # Handle game events
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        menu.state = "menu"
                    elif event.key == K_r:  # Reset pig position
                        pig.reset()
                        dragging = False
                        mouse_pressed = False
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if not pig.launched and math.dist(mouse_pos, (pig.body.position.x, pig.body.position.y)) < pig.radius:
                        dragging = True
                        mouse_pressed = True
                elif event.type == MOUSEBUTTONUP:
                    if dragging:
                        mouse_pressed = False
                        dragging = False
                        # Calculate launch velocity
                        mouse_pos = pygame.mouse.get_pos()
                        dx = SLINGSHOT_POS[0] - mouse_pos[0]
                        dy = SLINGSHOT_POS[1] - mouse_pos[1]
                        impulse_x = dx * 25
                        impulse_y = dy * 25
                        pig.launch((impulse_x, impulse_y))

            if dragging and mouse_pressed and not pig.launched:
                mouse_pos = pygame.mouse.get_pos()
                # Limit stretch distance
                dx = SLINGSHOT_POS[0] - mouse_pos[0]
                dy = SLINGSHOT_POS[1] - mouse_pos[1]
                stretch = math.sqrt(dx**2 + dy**2)
                if stretch > MAX_STRETCH:
                    scale = MAX_STRETCH / stretch
                    dx *= scale
                    dy *= scale
                pig.body.position = (SLINGSHOT_POS[0] - dx, SLINGSHOT_POS[1] - dy)
                pig.body.velocity = (0, 0)

            # Update physics
            space.step(1/60.0)
            
            # Update explosions
            for explosion in explosions[:]:
                explosion.update()
                if not explosion.is_alive:
                    explosions.remove(explosion)
            
            # Draw game elements
            if dragging and not pig.launched:
                slingshot.draw(screen, (pig.body.position.x, pig.body.position.y))
            else:
                slingshot.draw(screen)

            draw_ground(screen)
            pig.draw(screen)
            
            for block in blocks:
                block.draw(screen)
                
            for explosion in explosions:
                explosion.draw(screen)
                
        elif menu.state == "editor":
            # Initialize editor if not already done
            if not hasattr(menu, 'editor'):
                menu.editor = LevelEditor(screen, space, assets_dir)
            
            # Handle editor events
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        menu.state = "menu"
                        menu.editor = None  # Clear editor when exiting
                elif event.type == MOUSEBUTTONDOWN:
                    result = menu.editor.handle_click(pygame.mouse.get_pos())
                    if result == "play":
                        menu.state = "game"
            
            # Draw editor
            screen.blit(background, (0, 0))
            menu.editor.draw()
            draw_ground(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit() 