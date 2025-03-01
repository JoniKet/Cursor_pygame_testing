import pygame
import os
import sys

# Add parent directory to path for direct execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = current_dir
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    # Try importing with full package path first (when run through main launcher)
    from games.Questioning_bird.src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
except ImportError:
    # Fall back to local import for direct execution
    try:
        from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
    except ImportError:
        # Hardcode values if constants can't be imported
        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600
        print("Using default screen size: 800x600")

def scale_background():
    """
    Scale the AI-generated background to match the game screen size.
    """
    pygame.init()
    
    # Assets directory
    assets_dir = os.path.join(current_dir, "assets")
    
    # Check if assets directory exists
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        print(f"Created assets directory at {assets_dir}")
    
    # Source file path
    source_path = os.path.join(assets_dir, "background_ai.png")
    
    # Check if source file exists
    if not os.path.exists(source_path):
        print(f"Error: Could not find {source_path}")
        print("Please make sure your AI-generated background is in the assets directory")
        return False
    
    try:
        # Load the image
        print(f"Loading image from {source_path}")
        original_image = pygame.image.load(source_path)
        
        # Get original dimensions
        original_width, original_height = original_image.get_size()
        print(f"Original image size: {original_width}x{original_height}")
        print(f"Target size: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        
        # Scale the image to match the screen size
        scaled_image = pygame.transform.scale(original_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Save the scaled image (overwrite the original)
        pygame.image.save(scaled_image, source_path)
        print(f"Successfully scaled background_ai.png to {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        print("The game will now use this properly sized background!")
        return True
    except Exception as e:
        print(f"Error scaling image: {e}")
        return False

if __name__ == "__main__":
    scale_background()
    pygame.quit() 