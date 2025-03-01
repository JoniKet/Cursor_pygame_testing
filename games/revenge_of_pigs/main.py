import pygame
import pymunk
import sys
import os
import random
import math
from pygame.locals import *

# Import our modular code with correct relative imports
from games.revenge_of_pigs.src.constants import *
from games.revenge_of_pigs.src.entities.pig import Pig
from games.revenge_of_pigs.src.entities.block import AngryBirdBlock, WoodenBlock
from games.revenge_of_pigs.src.entities.slingshot import Slingshot
from games.revenge_of_pigs.src.ui.menu import Menu
from games.revenge_of_pigs.src.ui.level_editor import LevelEditor
from games.revenge_of_pigs.src.effects.explosion import Explosion
from games.revenge_of_pigs.src.effects.victory_effect import VictoryEffect

def run_game():
    # Initialize Pygame and Pymunk
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

    # Collision handler
    def collision_handler(arbiter, space, data):
        # Print collision information for debugging
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
                    # Add score for destroying a bird
                    menu.score += 1000
                elif isinstance(block, WoodenBlock):
                    # Only destroy wooden block if pig is moving fast enough
                    pig_velocity = math.sqrt(pig_shape.body.velocity.x**2 + pig_shape.body.velocity.y**2)
                    if pig_velocity > 500:  # Threshold for damage
                        if block.damage() and block.destroyed:
                            space.remove(target_shape, target_shape.body)
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

    # Create menu
    menu = Menu()

    # Game loop variables
    clock = pygame.time.Clock()
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

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_game() 