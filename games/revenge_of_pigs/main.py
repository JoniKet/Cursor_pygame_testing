import pygame
import pymunk
import sys
import os
import random
import math
from pygame.locals import *
import numpy as np
import wave

# Import our modular code with correct relative imports
from games.revenge_of_pigs.src.constants import *
from games.revenge_of_pigs.src.entities.pig import Pig
from games.revenge_of_pigs.src.entities.block import AngryBirdBlock, WoodenBlock
from games.revenge_of_pigs.src.entities.slingshot import Slingshot
from games.revenge_of_pigs.src.ui.menu import Menu
from games.revenge_of_pigs.src.ui.level_editor import LevelEditor
from games.revenge_of_pigs.src.effects.explosion import Explosion
from games.revenge_of_pigs.src.effects.victory_effect import VictoryEffect

# Define boundary constants
BOUNDARY_MARGIN = 50  # Extra margin beyond screen edges
LEFT_BOUNDARY = -BOUNDARY_MARGIN
RIGHT_BOUNDARY = WIDTH + BOUNDARY_MARGIN
TOP_BOUNDARY = -BOUNDARY_MARGIN
BOTTOM_BOUNDARY = HEIGHT + BOUNDARY_MARGIN
MAX_VELOCITY = 6000  # Drastically increased maximum velocity cap

# Initialize pygame mixer for sound
pygame.mixer.init()

# Sound paths and variables
SOUNDS_DIR = None
LAUNCH_SOUND = None
COLLISION_SOUND = None
WOOD_BREAK_SOUND = None
VICTORY_SOUND = None
SLINGSHOT_STRETCH_SOUND = None

def load_sound(filename):
    """Load a sound file"""
    global SOUNDS_DIR
    
    if SOUNDS_DIR is None:
        return None
        
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
    global LAUNCH_SOUND, COLLISION_SOUND, WOOD_BREAK_SOUND, VICTORY_SOUND, SLINGSHOT_STRETCH_SOUND, SOUNDS_DIR
    
    # Load the sounds
    LAUNCH_SOUND = load_sound("launch.wav")
    COLLISION_SOUND = load_sound("collision.wav")
    WOOD_BREAK_SOUND = load_sound("wood_break.wav")
    VICTORY_SOUND = load_sound("victory.wav")
    SLINGSHOT_STRETCH_SOUND = load_sound("slingshot_stretch.wav")

def enforce_boundaries(space, pig, blocks):
    """
    Check if any objects are outside the map boundaries and bring them back.
    Also applies a small dampening force to objects that hit the boundaries.
    Enhanced to handle extremely high velocities.
    """
    # Check pig boundaries
    if pig.launched:
        pos_x, pos_y = pig.body.position
        velocity_x, velocity_y = pig.body.velocity
        
        # Cap velocity to prevent boundary escapes
        velocity_magnitude = math.sqrt(velocity_x**2 + velocity_y**2)
        if velocity_magnitude > MAX_VELOCITY:
            scale_factor = MAX_VELOCITY / velocity_magnitude
            velocity_x *= scale_factor
            velocity_y *= scale_factor
            pig.body.velocity = velocity_x, velocity_y
        
        # Apply boundary constraints with stronger bounce effect for high velocities
        if pos_x < LEFT_BOUNDARY:
            pig.body.position = LEFT_BOUNDARY, pos_y
            pig.body.velocity = -velocity_x * 0.8, velocity_y  # Less dampening (was 0.7)
        elif pos_x > RIGHT_BOUNDARY:
            pig.body.position = RIGHT_BOUNDARY, pos_y
            pig.body.velocity = -velocity_x * 0.8, velocity_y  # Less dampening (was 0.7)
            
        if pos_y < TOP_BOUNDARY:
            pig.body.position = pos_x, TOP_BOUNDARY
            pig.body.velocity = velocity_x, -velocity_y * 0.8  # Less dampening (was 0.7)
        elif pos_y > BOTTOM_BOUNDARY:
            pig.body.position = pos_x, BOTTOM_BOUNDARY
            pig.body.velocity = velocity_x, -velocity_y * 0.8  # Less dampening (was 0.7)
    
    # Check block boundaries
    for block in blocks:
        if not block.destroyed:
            pos_x, pos_y = block.body.position
            velocity_x, velocity_y = block.body.velocity
            
            # Cap velocity to prevent boundary escapes
            velocity_magnitude = math.sqrt(velocity_x**2 + velocity_y**2)
            if velocity_magnitude > MAX_VELOCITY:
                scale_factor = MAX_VELOCITY / velocity_magnitude
                velocity_x *= scale_factor
                velocity_y *= scale_factor
                block.body.velocity = velocity_x, velocity_y
            
            # Apply boundary constraints with stronger bounce effect for high velocities
            if pos_x < LEFT_BOUNDARY:
                block.body.position = LEFT_BOUNDARY, pos_y
                block.body.velocity = -velocity_x * 0.8, velocity_y  # Less dampening (was 0.7)
            elif pos_x > RIGHT_BOUNDARY:
                block.body.position = RIGHT_BOUNDARY, pos_y
                block.body.velocity = -velocity_x * 0.8, velocity_y  # Less dampening (was 0.7)
                
            if pos_y < TOP_BOUNDARY:
                block.body.position = pos_x, TOP_BOUNDARY
                block.body.velocity = velocity_x, -velocity_y * 0.8  # Less dampening (was 0.7)
            elif pos_y > BOTTOM_BOUNDARY:
                block.body.position = pos_x, BOTTOM_BOUNDARY
                block.body.velocity = velocity_x, -velocity_y * 0.8  # Less dampening (was 0.7)

def run_game():
    # Initialize pygame
    pygame.init()
    
    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Revenge of Pigs")
    
    # Set up the clock
    clock = pygame.time.Clock()
    
    # Create assets directory if it doesn't exist
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    # Initialize sounds directory and load sounds
    global SOUNDS_DIR
    SOUNDS_DIR = os.path.join(assets_dir, "sounds")
    if not os.path.exists(SOUNDS_DIR):
        os.makedirs(SOUNDS_DIR)
        print(f"Sound directory not found. Please run generate_sounds.py to create sound files.")
    load_sounds()
    
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
    space.gravity = GRAVITY

    # Create game objects
    pig = Pig(SLINGSHOT_X, SLINGSHOT_Y - 20, space, pig_image)

    # Create ground segments with a gap near the slingshot
    ground_left = pymunk.Segment(space.static_body, (0, HEIGHT - 50), (SLINGSHOT_X - GAP_WIDTH/2, HEIGHT - 50), 5)
    ground_right = pymunk.Segment(space.static_body, (SLINGSHOT_X + GAP_WIDTH/2, HEIGHT - 50), (WIDTH, HEIGHT - 50), 5)

    # Set ground properties
    for ground in [ground_left, ground_right]:
        ground.friction = 1.0
        ground.elasticity = 0.5
        space.add(ground)

    # Create boundary walls
    wall_thickness = 5
    # Left wall
    left_wall = pymunk.Segment(space.static_body, (0, 0), (0, HEIGHT), wall_thickness)
    # Right wall
    right_wall = pymunk.Segment(space.static_body, (WIDTH, 0), (WIDTH, HEIGHT), wall_thickness)
    # Top wall
    top_wall = pymunk.Segment(space.static_body, (0, 0), (WIDTH, 0), wall_thickness)
    
    # Set wall properties
    for wall in [left_wall, right_wall, top_wall]:
        wall.friction = 0.5
        wall.elasticity = 0.7
        space.add(wall)

    # Create angry bird blocks and wooden blocks
    blocks = []
    
    # First layer: Bird, Wood, Bird
    blocks.append(AngryBirdBlock(STACK_START_X - BLOCK_SIZE, STACK_START_Y, BLOCK_SIZE, BLOCK_SIZE, space, angry_bird_image))
    blocks.append(WoodenBlock(STACK_START_X, STACK_START_Y, BLOCK_SIZE, BLOCK_SIZE, space))
    blocks.append(AngryBirdBlock(STACK_START_X + BLOCK_SIZE, STACK_START_Y, BLOCK_SIZE, BLOCK_SIZE, space, angry_bird_image))

    # Second layer: Wood, Bird, Wood
    blocks.append(WoodenBlock(STACK_START_X - BLOCK_SIZE, STACK_START_Y - BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, space))
    blocks.append(AngryBirdBlock(STACK_START_X, STACK_START_Y - BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, space, angry_bird_image))
    blocks.append(WoodenBlock(STACK_START_X + BLOCK_SIZE, STACK_START_Y - BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, space))

    # Third layer: Bird, Wood, Bird
    blocks.append(AngryBirdBlock(STACK_START_X - BLOCK_SIZE, STACK_START_Y - 2 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, space, angry_bird_image))
    blocks.append(WoodenBlock(STACK_START_X, STACK_START_Y - 2 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, space))
    blocks.append(AngryBirdBlock(STACK_START_X + BLOCK_SIZE, STACK_START_Y - 2 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, space, angry_bird_image))

    # Create slingshot object
    slingshot = Slingshot(SLINGSHOT_X, SLINGSHOT_Y)

    # Create explosion list
    explosions = []

    # Collision handler function
    def collision_handler(arbiter, space, data):
        pig_shape = arbiter.shapes[0]
        block_shape = arbiter.shapes[1]
        
        # Get collision velocity
        points = arbiter.contact_point_set.points
        if len(points) > 0:
            point = points[0]
            pig_vel = pig_shape.body.velocity
            rel_velocity = (pig_vel.x**2 + pig_vel.y**2)**0.5
            
            # Play collision sound
            if COLLISION_SOUND:
                COLLISION_SOUND.play()
            
            # Process wooden blocks
            if block_shape.collision_type == COLLISION_TYPES["WOOD"] and rel_velocity > 200:
                for block in blocks:
                    if block.shape == block_shape:
                        # Damage the block
                        block.damage()
                        
                        # Play wood break sound
                        if WOOD_BREAK_SOUND:
                            WOOD_BREAK_SOUND.play()
                        
                        # Add score
                        menu.score += 100
                        
                        # Create explosion effect
                        pos = block.body.position
                        explosions.append(Explosion(pos.x, pos.y))
                        
                        # If block is destroyed, remove it from space
                        if block.destroyed:
                            try:
                                space.remove(block.body, block.shape)
                            except:
                                pass
                        break
            
            # Process bird blocks
            elif block_shape.collision_type == COLLISION_TYPES["BIRD"] and rel_velocity > 150:
                for block in blocks:
                    if block.shape == block_shape:
                        # Damage the bird block (should destroy it in one hit)
                        block.damage()
                        
                        # Play collision sound again for emphasis
                        if COLLISION_SOUND:
                            COLLISION_SOUND.play()
                        
                        # Add score - birds are worth more points
                        menu.score += 200
                        
                        # Create explosion effect
                        pos = block.body.position
                        explosions.append(Explosion(pos.x, pos.y))
                        
                        # If bird is destroyed, remove it from space
                        if block.destroyed:
                            try:
                                space.remove(block.body, block.shape)
                            except:
                                pass
                        break
        
        return True

    # Add collision handlers
    handler_bird = space.add_collision_handler(COLLISION_TYPES["PIG"], COLLISION_TYPES["BIRD"])
    handler_bird.begin = collision_handler
    
    handler_wood = space.add_collision_handler(COLLISION_TYPES["PIG"], COLLISION_TYPES["WOOD"])
    handler_wood.begin = collision_handler

    # Draw ground segments
    def draw_ground(screen):
        # Draw left ground segment
        pygame.draw.rect(screen, (0, 100, 0), (0, HEIGHT - 50, SLINGSHOT_X - GAP_WIDTH/2, 50))
        # Draw right ground segment
        pygame.draw.rect(screen, (0, 100, 0), (SLINGSHOT_X + GAP_WIDTH/2, HEIGHT - 50, WIDTH - (SLINGSHOT_X + GAP_WIDTH/2), 50))
        
        # Draw boundary walls
        pygame.draw.line(screen, (100, 100, 100), (0, 0), (0, HEIGHT), wall_thickness)  # Left wall
        pygame.draw.line(screen, (100, 100, 100), (WIDTH, 0), (WIDTH, HEIGHT), wall_thickness)  # Right wall
        pygame.draw.line(screen, (100, 100, 100), (0, 0), (WIDTH, 0), wall_thickness)  # Top wall

    # Create menu
    menu = Menu()

    # Game loop variables
    running = True
    dragging = False
    mouse_pressed = False

    # Game loop
    while running:
        # Handle events first
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif menu.state in ["menu", "credits", "victory"]:
                running = menu.handle_input(event)
            elif menu.state == "editor":
                # Ensure the editor is initialized
                if not hasattr(menu, 'editor') or menu.editor is None:
                    menu.editor = LevelEditor(screen, space, assets_dir)
                
                if event.type == MOUSEBUTTONDOWN:
                    result = menu.editor.handle_click(pygame.mouse.get_pos())
                    if result == "play":
                        menu.state = "game"
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    menu.state = "menu"
                    menu.editor = None
            elif menu.state == "game":
                # Handle game specific events
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        menu.state = "menu"
                    elif event.key == K_r:  # Reset pig position
                        pig.reset()
                        dragging = False
                        mouse_pressed = False
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_pressed = True
                    if not pig.launched:
                        mouse_pos = pygame.mouse.get_pos()
                        if ((mouse_pos[0] - SLINGSHOT_POS[0])**2 + 
                            (mouse_pos[1] - SLINGSHOT_POS[1])**2) < 1000:  # Within range of slingshot
                            dragging = True
                            # Play slingshot stretch sound
                            if SLINGSHOT_STRETCH_SOUND:
                                SLINGSHOT_STRETCH_SOUND.play()
                elif event.type == MOUSEBUTTONUP:
                    mouse_pressed = False
                    if menu.state == "game" and dragging:
                        dragging = False
                        if not pig.launched:
                            mouse_pos = pygame.mouse.get_pos()
                            dx = SLINGSHOT_POS[0] - mouse_pos[0]
                            dy = SLINGSHOT_POS[1] - mouse_pos[1]
                            
                            # Limit stretch distance
                            stretch = math.sqrt(dx**2 + dy**2)
                            if stretch > MAX_STRETCH:
                                scale = MAX_STRETCH / stretch
                                dx *= scale
                                dy *= scale
                            
                            # Launch the pig
                            impulse = (dx * 35, dy * 35)
                            pig.launch(impulse)
                            
                            # Play launch sound
                            if LAUNCH_SOUND:
                                LAUNCH_SOUND.play()

        # Clear screen and draw background
        screen.blit(background, (0, 0))
        
        # Draw ground for game and editor states
        if menu.state in ["game", "editor"]:
            draw_ground(screen)

        # Handle different game states
        if menu.state == "menu" or menu.state == "credits":
            menu.draw(screen)
            
        elif menu.state == "victory":
            # Initialize victory effect if needed
            if menu.victory_effect is None:
                menu.victory_effect = VictoryEffect(WIDTH, HEIGHT)
                # Play victory sound
                if VICTORY_SOUND:
                    VICTORY_SOUND.play()
            
            # Update and draw victory effects
            menu.victory_effect.update()
            menu.victory_effect.draw(screen, menu.score)
            
        elif menu.state == "editor":
            # Ensure the editor is initialized
            if not hasattr(menu, 'editor') or menu.editor is None:
                menu.editor = LevelEditor(screen, space, assets_dir)
            
            # Draw the editor
            menu.editor.draw()
            
        elif menu.state == "game":
            # If first time entering game state or coming from editor, initialize physics
            if not hasattr(menu, 'game_initialized') or (hasattr(menu, 'editor') and menu.editor is not None):
                # Reset score when starting new game
                menu.score = 0
                # Store blocks (either from editor or default level)
                if hasattr(menu, 'editor') and menu.editor is not None:
                    current_blocks = menu.editor.get_blocks()
                    menu.editor.clear_blocks()
                    menu.editor = None
                else:
                    current_blocks = blocks.copy()
                    
                # Reset physics space
                for block in blocks:
                    try:
                        space.remove(block.body, block.shape)
                    except:
                        pass
                blocks.clear()
                
                # Reset space
                try:
                    space.remove(ground_left)
                    space.remove(ground_right)
                    space.remove(left_wall)
                    space.remove(right_wall)
                    space.remove(top_wall)
                except:
                    pass
                    
                space = pymunk.Space()
                space.gravity = GRAVITY
                
                # Recreate ground segments
                ground_left = pymunk.Segment(space.static_body, (0, HEIGHT - 50), (SLINGSHOT_X - GAP_WIDTH/2, HEIGHT - 50), 5)
                ground_right = pymunk.Segment(space.static_body, (SLINGSHOT_X + GAP_WIDTH/2, HEIGHT - 50), (WIDTH, HEIGHT - 50), 5)
                for ground in [ground_left, ground_right]:
                    ground.friction = 1.0
                    ground.elasticity = 0.5
                    space.add(ground)
                
                # Recreate boundary walls
                left_wall = pymunk.Segment(space.static_body, (0, 0), (0, HEIGHT), wall_thickness)
                right_wall = pymunk.Segment(space.static_body, (WIDTH, 0), (WIDTH, HEIGHT), wall_thickness)
                top_wall = pymunk.Segment(space.static_body, (0, 0), (WIDTH, 0), wall_thickness)
                for wall in [left_wall, right_wall, top_wall]:
                    wall.friction = 0.5
                    wall.elasticity = 0.7
                    space.add(wall)
                
                # Add collision handlers
                handler_bird = space.add_collision_handler(COLLISION_TYPES["PIG"], COLLISION_TYPES["BIRD"])
                handler_bird.begin = collision_handler
                
                handler_wood = space.add_collision_handler(COLLISION_TYPES["PIG"], COLLISION_TYPES["WOOD"])
                handler_wood.begin = collision_handler
                
                # Make all blocks dynamic and add to physics space
                for block in current_blocks:
                    # Make dynamic and add to space
                    block.make_dynamic()
                    space.add(block.body, block.shape)
                
                # Update the global blocks list
                blocks = current_blocks
                
                # Reset pig
                try:
                    space.remove(pig.body, pig.shape)
                except:
                    pass
                pig = Pig(SLINGSHOT_X, SLINGSHOT_Y - 20, space, pig_image)
                
                # Mark game as initialized
                menu.game_initialized = True

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
            
            # Enforce boundaries for all objects
            enforce_boundaries(space, pig, blocks)
            
            # Update explosions
            for explosion in explosions[:]:
                explosion.update()
                if not explosion.is_alive:
                    explosions.remove(explosion)
            
            # Check for victory condition
            menu.check_victory(blocks)
            
            # Draw game elements
            if dragging and not pig.launched:
                slingshot.draw(screen, (pig.body.position.x, pig.body.position.y))
            else:
                slingshot.draw(screen)

            pig.draw(screen)
            
            for block in blocks:
                block.draw(screen)
                
            for explosion in explosions:
                explosion.draw(screen)
                
            # Draw score
            score_text = pygame.font.Font(None, 36).render(f"Score: {menu.score}", True, WHITE)
            screen.blit(score_text, (10, 10))

        # Update display
        pygame.display.flip()
        clock.tick(60)

    # Clean up and return to main launcher
    pygame.mixer.stop()  # Stop all sounds
    pygame.quit()
    return True  # Return True to continue to the main menu

if __name__ == "__main__":
    run_game() 