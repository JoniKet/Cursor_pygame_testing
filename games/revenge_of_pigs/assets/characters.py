import pygame
import math

def create_pig(radius):
    """Create a cute pig face"""
    # Create a surface with alpha channel
    size = radius * 2
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Main body (light green)
    pygame.draw.circle(surface, (144, 238, 144), (radius, radius), radius)
    
    # Nose (pink)
    nose_radius = radius // 4
    pygame.draw.circle(surface, (255, 192, 203), (radius, radius + nose_radius), nose_radius)
    
    # Eyes (black)
    eye_radius = radius // 5
    eye_offset = radius // 3
    pygame.draw.circle(surface, (0, 0, 0), (radius - eye_offset, radius - eye_offset), eye_radius)
    pygame.draw.circle(surface, (0, 0, 0), (radius + eye_offset, radius - eye_offset), eye_radius)
    
    # Ears (darker green)
    ear_color = (100, 200, 100)
    ear_points = [
        # Left ear
        [(radius - radius//2, radius - radius//2),
         (radius - radius//1.2, radius - radius),
         (radius - radius//4, radius - radius//1.5)],
        # Right ear
        [(radius + radius//2, radius - radius//2),
         (radius + radius//1.2, radius - radius),
         (radius + radius//4, radius - radius//1.5)]
    ]
    for ear in ear_points:
        pygame.draw.polygon(surface, ear_color, ear)
    
    return surface

def create_angry_bird(size):
    """Create an angry bird block"""
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Main body (red)
    pygame.draw.rect(surface, (255, 0, 0), (0, 0, size, size))
    
    # Eyes (white with black pupils)
    eye_size = size // 4
    eye_offset = size // 6
    
    # White parts
    pygame.draw.circle(surface, (255, 255, 255), (size//2 - eye_offset, size//3), eye_size)
    pygame.draw.circle(surface, (255, 255, 255), (size//2 + eye_offset, size//3), eye_size)
    
    # Black pupils
    pupil_size = eye_size // 2
    pygame.draw.circle(surface, (0, 0, 0), (size//2 - eye_offset, size//3), pupil_size)
    pygame.draw.circle(surface, (0, 0, 0), (size//2 + eye_offset, size//3), pupil_size)
    
    # Angry eyebrows
    eyebrow_color = (0, 0, 0)
    eyebrow_thickness = size // 10
    
    # Left eyebrow
    pygame.draw.line(surface, eyebrow_color, 
                    (size//4, size//4),
                    (size//2 - eye_offset, size//6),
                    eyebrow_thickness)
    
    # Right eyebrow
    pygame.draw.line(surface, eyebrow_color,
                    (size//2 + eye_offset, size//6),
                    (3*size//4, size//4),
                    eyebrow_thickness)
    
    # Beak
    beak_color = (255, 200, 0)  # Yellow
    beak_points = [(size//2, size//2),
                  (size//3, 2*size//3),
                  (2*size//3, 2*size//3)]
    pygame.draw.polygon(surface, beak_color, beak_points)
    
    return surface

if __name__ == '__main__':
    pygame.init()
    
    # Create and save pig
    pig = create_pig(20)
    pygame.image.save(pig, 'assets/pig.png')
    
    # Create and save angry bird block
    angry_bird = create_angry_bird(50)
    pygame.image.save(angry_bird, 'assets/angry_bird.png')
    
    pygame.quit() 