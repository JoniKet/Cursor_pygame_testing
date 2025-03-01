import pygame
import os
import random
import sys

# Add parent directory to path for direct execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    # Try importing with full package path first (when run through main launcher)
    from games.Questioning_bird.src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
except ImportError:
    # Fall back to local import for direct execution
    from constants import SCREEN_WIDTH, SCREEN_HEIGHT

def create_basic_background():
    """Create a basic background image that can be enhanced with AI later"""
    # Create ground
    ground = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    ground.fill((76, 153, 0))  # Green grass base
    
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
    
    # Add a grid pattern to help with AI enhancement
    grid_size = 50
    for x in range(0, SCREEN_WIDTH, grid_size):
        pygame.draw.line(ground, (70, 140, 0), (x, 0), (x, SCREEN_HEIGHT), 1)
    for y in range(0, SCREEN_HEIGHT, grid_size):
        pygame.draw.line(ground, (70, 140, 0), (0, y), (SCREEN_WIDTH, y), 1)
    
    # Add a border
    pygame.draw.rect(ground, (50, 100, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)
    
    return ground

def save_background():
    """Generate and save the background as a PNG file"""
    pygame.init()
    
    # Create assets directory if it doesn't exist
    assets_dir = os.path.join(parent_dir, "assets")
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    # Generate the background
    background = create_basic_background()
    
    # Save the background
    background_path = os.path.join(assets_dir, "background.png")
    pygame.image.save(background, background_path)
    
    print(f"Background saved to {background_path}")
    print("You can now enhance this image with AI tools and replace it.")
    
    pygame.quit()

if __name__ == "__main__":
    save_background() 