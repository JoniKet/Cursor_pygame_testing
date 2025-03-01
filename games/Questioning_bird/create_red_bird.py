import pygame
import os
import sys

# Add parent directory to path for direct execution
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    # Try importing with full package path first (when run through main launcher)
    from games.Questioning_bird.src.constants import ASSET_PATH, BIRD_WIDTH, BIRD_HEIGHT
except ImportError:
    # Fall back to local import for direct execution
    from src.constants import ASSET_PATH, BIRD_WIDTH, BIRD_HEIGHT

def create_red_bird_image():
    """Create a custom red Angry Birds character image and save it to assets"""
    # Initialize pygame
    pygame.init()
    
    # Create a surface with transparency
    image_size = max(BIRD_WIDTH, BIRD_HEIGHT) * 2  # Make it larger for better quality
    image = pygame.Surface((image_size, image_size), pygame.SRCALPHA)
    
    # Center coordinates
    center_x, center_y = image_size // 2, image_size // 2
    radius = image_size // 2 - 10  # Slightly smaller than the surface
    
    # Draw the red bird
    # Main body - red circle
    pygame.draw.circle(image, (216, 49, 49), (center_x, center_y), radius)
    
    # Add shading/highlight for 3D effect
    highlight_radius = radius - 5
    highlight_offset = 8
    pygame.draw.circle(
        image, 
        (240, 80, 80), 
        (center_x - highlight_offset, center_y - highlight_offset), 
        highlight_radius
    )
    
    # Red bird's distinctive angry eyebrows - thick black lines
    eyebrow_length = radius * 0.6
    eyebrow_thickness = radius * 0.15
    eyebrow_y = center_y - radius * 0.3
    
    # Left eyebrow
    pygame.draw.line(
        image, 
        (0, 0, 0), 
        (center_x - eyebrow_length, eyebrow_y + eyebrow_thickness), 
        (center_x - eyebrow_length * 0.3, eyebrow_y - eyebrow_thickness), 
        int(eyebrow_thickness * 1.5)
    )
    
    # Right eyebrow
    pygame.draw.line(
        image, 
        (0, 0, 0), 
        (center_x + eyebrow_length, eyebrow_y + eyebrow_thickness), 
        (center_x + eyebrow_length * 0.3, eyebrow_y - eyebrow_thickness), 
        int(eyebrow_thickness * 1.5)
    )
    
    # Eyes - white with black pupils
    eye_radius = radius * 0.25
    eye_offset_x = radius * 0.4
    eye_offset_y = radius * 0.1
    
    # Left eye white
    pygame.draw.circle(
        image, 
        (255, 255, 255), 
        (center_x - eye_offset_x, center_y - eye_offset_y), 
        eye_radius
    )
    
    # Right eye white
    pygame.draw.circle(
        image, 
        (255, 255, 255), 
        (center_x + eye_offset_x, center_y - eye_offset_y), 
        eye_radius
    )
    
    # Pupils
    pupil_radius = eye_radius * 0.5
    pupil_offset = eye_radius * 0.2
    
    # Left pupil
    pygame.draw.circle(
        image, 
        (0, 0, 0), 
        (center_x - eye_offset_x + pupil_offset, center_y - eye_offset_y), 
        pupil_radius
    )
    
    # Right pupil
    pygame.draw.circle(
        image, 
        (0, 0, 0), 
        (center_x + eye_offset_x + pupil_offset, center_y - eye_offset_y), 
        pupil_radius
    )
    
    # Beak - orange triangle
    beak_width = radius * 0.6
    beak_height = radius * 0.5
    beak_points = [
        (center_x, center_y + radius * 0.1),  # Top point
        (center_x + beak_width, center_y + radius * 0.3),  # Right point
        (center_x, center_y + beak_height)  # Bottom point
    ]
    pygame.draw.polygon(image, (255, 165, 0), beak_points)
    
    # Add a darker outline to the beak
    pygame.draw.polygon(image, (200, 120, 0), beak_points, width=2)
    
    # Tail feathers - small red triangles at the back
    feather_size = radius * 0.4
    feather_points = [
        (center_x - radius - 5, center_y - feather_size),  # Top point
        (center_x - radius + feather_size, center_y),  # Right point
        (center_x - radius - 5, center_y + feather_size)  # Bottom point
    ]
    pygame.draw.polygon(image, (180, 40, 40), feather_points)
    
    # Create assets directory if it doesn't exist
    if not os.path.exists(ASSET_PATH):
        os.makedirs(ASSET_PATH)
    
    # Save the image
    file_path = os.path.join(ASSET_PATH, 'bird.png')
    pygame.image.save(image, file_path)
    print(f"Red Angry Birds character image saved to {file_path}")
    
    # Clean up
    pygame.quit()
    
    return file_path

if __name__ == "__main__":
    create_red_bird_image() 