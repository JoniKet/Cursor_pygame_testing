import os
import pygame
import sys

# Add parent directory to path for direct execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    # Try importing with full package path first (when run through main launcher)
    from games.Pig_invaders.src.constants import ASSET_PATH
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
            'background': (0, 0, 40),  # Dark space blue
            'player': (0, 255, 0),     # Green
            'enemy': (255, 0, 0),      # Red
            'bullet': (255, 255, 0),   # Yellow
            'explosion': (255, 165, 0)  # Orange
        }
        
        # Load assets
        self.load_images()
        self.load_sounds()
        
        # Import and initialize dialog after assets are loaded
        from .ui.dialog import Dialog
        self.briefing = Dialog(self)
        
    def load_images(self):
        """Load all game images or create default ones"""
        image_files = {
            'background': 'background.png',
            'player': 'spaceship.png',
            'enemy': 'enemy.png',
            'bullet': 'bullet.png',
            'explosion': 'explosion.png',
            'menu_background': 'menu_background.png',
            'intel_photo': 'intel_photo.png',
            'general_pig_briefing': 'general_pig_briefing.png'
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
        
        if name == 'background':
            # Create a space background
            image = pygame.Surface((800, 600))
            image.fill((0, 0, 40))  # Dark blue for space
            
            # Add some stars
            for _ in range(100):
                x = pygame.time.get_ticks() % 800
                y = pygame.time.get_ticks() % 600
                pygame.draw.circle(image, (255, 255, 255), (x, y), 1)
            
        elif name == 'player':
            # Create a green pig spaceship
            image = pygame.Surface((50, 50), pygame.SRCALPHA)
            # Main body - green circle
            pygame.draw.circle(image, (50, 205, 50), (25, 25), 20)  # Green color
            # Eyes
            pygame.draw.circle(image, (255, 255, 255), (18, 18), 5)  # Left eye white
            pygame.draw.circle(image, (255, 255, 255), (32, 18), 5)  # Right eye white
            pygame.draw.circle(image, (0, 0, 0), (18, 18), 2)  # Left pupil
            pygame.draw.circle(image, (0, 0, 0), (32, 18), 2)  # Right pupil
            # Snout
            pygame.draw.ellipse(image, (255, 200, 200), (20, 25, 10, 8))
            # Spaceship elements
            pygame.draw.rect(image, (150, 150, 150), (10, 35, 30, 10))  # Base
            
        elif name == 'enemy':
            # Create a red angry bird enemy
            image = pygame.Surface((40, 40), pygame.SRCALPHA)
            # Main body - red circle
            pygame.draw.circle(image, (216, 49, 49), (20, 20), 15)  # Red color
            # Eyebrows
            pygame.draw.line(image, (0, 0, 0), (12, 12), (18, 10), 2)  # Left eyebrow
            pygame.draw.line(image, (0, 0, 0), (22, 10), (28, 12), 2)  # Right eyebrow
            # Eyes
            pygame.draw.circle(image, (255, 255, 255), (15, 15), 4)  # Left eye white
            pygame.draw.circle(image, (255, 255, 255), (25, 15), 4)  # Right eye white
            pygame.draw.circle(image, (0, 0, 0), (15, 15), 2)  # Left pupil
            pygame.draw.circle(image, (0, 0, 0), (25, 15), 2)  # Right pupil
            # Beak
            pygame.draw.polygon(image, (255, 165, 0), [(20, 18), (25, 22), (20, 26)])
            
        elif name == 'bullet':
            # Create a small yellow circle for bullets
            image = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(image, color, (5, 5), 3)
            
        elif name == 'explosion':
            # Create a simple explosion effect
            image = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(image, color, (25, 25), 20)
            pygame.draw.circle(image, (255, 255, 255), (25, 25), 15)
            pygame.draw.circle(image, (255, 0, 0), (25, 25), 10)
            
        else:
            # Default white square
            image = pygame.Surface((50, 50))
            image.fill(color)
            
        self.images[name] = image
        
    def load_sounds(self):
        """Load all game sounds or initialize empty ones"""
        sound_files = {
            'shoot': 'sounds/shoot.wav',
            'explosion': 'sounds/explosion.wav',
            'menu_select': 'sounds/menu_select.wav',
            'pig_talk': 'sounds/pig_talk.wav',
            'background_music': 'sounds/Space_Swine_Shooter!.mp3',
            'briefing_music': 'sounds/Space_pork.mp3'
        }
        
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        for name, filename in sound_files.items():
            file_path = os.path.join(ASSET_PATH, filename)
            if os.path.exists(file_path):
                try:
                    sound = pygame.mixer.Sound(file_path)
                    self.sounds[name] = sound
                except pygame.error as e:
                    print(f"Error loading sound {name}: {e}")
                    # Create empty sound for missing files
                    self.sounds[name] = None
            else:
                print(f"Sound file not found: {file_path}")
                # Create empty sound for missing files
                self.sounds[name] = None
                
    def get_image(self, name):
        """Get an image by name"""
        return self.images.get(name, self.images.get('background'))
    
    def get_sound(self, name):
        """Get a sound by name"""
        return self.sounds.get(name)
    
    def play_sound(self, name, volume=1.0):
        """Play a sound by name with optional volume control"""
        sound = self.get_sound(name)
        if sound:
            # Set volume (0.0 to 1.0)
            sound.set_volume(volume)
            sound.play()
        else:
            print(f"Sound '{name}' not found or not loaded properly")
            
    def play_background_music(self, volume=0.5):
        """Play background music in a loop"""
        music = self.get_sound('background_music')
        if music:
            music.set_volume(volume)
            music.play(loops=-1)  # -1 means loop indefinitely
        else:
            print("Background music not found or not loaded properly")
            
    def play_briefing_music(self, volume=0.5):
        """Play briefing music in a loop"""
        music = self.get_sound('briefing_music')
        if music:
            music.set_volume(volume)
            music.play(loops=-1)
        else:
            print("Briefing music not found or not loaded properly")
            
    def stop_music(self, name):
        """Stop specific music track"""
        music = self.get_sound(name)
        if music:
            music.stop()
            
    def stop_all_music(self):
        """Stop all music tracks"""
        for name in ['background_music', 'briefing_music']:
            self.stop_music(name)
