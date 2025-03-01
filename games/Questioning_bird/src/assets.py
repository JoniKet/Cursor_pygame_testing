import os
import pygame
import sys

# Add parent directory to path for direct execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    # Try importing with full package path first (when run through main launcher)
    from games.Questioning_bird.src.constants import ASSET_PATH
except ImportError:
    # Fall back to local import for direct execution
    from src.constants import ASSET_PATH

class Assets:
    """Class to manage all game assets (images, sounds)"""
    
    def __init__(self):
        """Initialize and load all game assets"""
        self.images = {}
        self.sounds = {}
        
        # Create asset directory if it doesn't exist
        if not os.path.exists(ASSET_PATH):
            os.makedirs(ASSET_PATH)
            
        # Define default colors for fallback assets
        self.default_colors = {
            'bird': (255, 255, 0),       # Yellow
            'pig': (50, 205, 50),        # Green
            'bullet': (255, 0, 0),       # Red
            'explosion': (255, 165, 0),  # Orange
            'background': (135, 206, 235) # Sky blue
        }
        
        # Load images
        self.load_images()
        
        # Load sounds
        self.load_sounds()
        
    def load_images(self):
        """Load all game images or create default ones"""
        image_files = {
            'bird': 'bird.png',
            'pig': 'pig.png',
            'bullet': 'bullet.png',
            'explosion': 'explosion.png',
            'background': 'background.png'
        }
        
        for name, filename in image_files.items():
            file_path = os.path.join(ASSET_PATH, filename)
            if os.path.exists(file_path):
                try:
                    image = pygame.image.load(file_path).convert_alpha()
                    self.images[name] = image
                except pygame.error:
                    self.create_default_image(name)
            else:
                self.create_default_image(name)
                
    def create_default_image(self, name):
        """Create a default image if the asset file doesn't exist"""
        color = self.default_colors.get(name, (255, 255, 255))
        
        if name == 'bird':
            # Create a yellow circle for the bird
            image = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(image, color, (25, 25), 20)
            # Add eyes
            pygame.draw.circle(image, (0, 0, 0), (35, 15), 5)
            pygame.draw.circle(image, (255, 255, 255), (33, 13), 2)
            # Add beak
            pygame.draw.polygon(image, (255, 165, 0), [(45, 25), (55, 20), (55, 30)])
            
        elif name == 'pig':
            # Create a green circle for the pig
            image = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(image, color, (20, 20), 15)
            # Add eyes
            pygame.draw.circle(image, (0, 0, 0), (15, 15), 3)
            pygame.draw.circle(image, (0, 0, 0), (25, 15), 3)
            # Add snout
            pygame.draw.ellipse(image, (255, 200, 200), (15, 20, 10, 8))
            
        elif name == 'bullet':
            # Create a small red circle for bullets
            image = pygame.Surface((15, 15), pygame.SRCALPHA)
            pygame.draw.circle(image, color, (7, 7), 5)
            
        elif name == 'explosion':
            # Create a simple explosion effect
            image = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(image, color, (25, 25), 20)
            pygame.draw.circle(image, (255, 255, 255), (25, 25), 15)
            pygame.draw.circle(image, (255, 0, 0), (25, 25), 10)
            
        elif name == 'background':
            # Create a simple ground background
            image = pygame.Surface((800, 600))
            image.fill((76, 153, 0))  # Green for grass
            
        else:
            # Default white square
            image = pygame.Surface((50, 50))
            image.fill(color)
            
        self.images[name] = image
        
    def load_sounds(self):
        """Load all game sounds or initialize empty ones"""
        sound_files = {
            'shoot': 'shoot.wav',
            'explosion': 'explosion.wav',
            'game_over': 'game_over.wav',
            'menu_select': 'menu_select.wav'
        }
        
        for name, filename in sound_files.items():
            file_path = os.path.join(ASSET_PATH, filename)
            if os.path.exists(file_path):
                try:
                    sound = pygame.mixer.Sound(file_path)
                    self.sounds[name] = sound
                except pygame.error:
                    # Create empty sound for missing files
                    self.sounds[name] = None
            else:
                # Create empty sound for missing files
                self.sounds[name] = None
                
    def get_image(self, name):
        """Get an image by name"""
        return self.images.get(name, self.images.get('background'))
    
    def get_sound(self, name):
        """Get a sound by name"""
        return self.sounds.get(name)
    
    def play_sound(self, name):
        """Play a sound by name"""
        sound = self.get_sound(name)
        if sound:
            sound.play() 