import pygame
import os
import sys
import random
import math

# Add parent directory to path for direct execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    # Try importing with full package path first (when run through main launcher)
    from games.Pig_invaders.src.constants import (
        SCREEN_WIDTH, SCREEN_HEIGHT, 
        STATE_PLAYING, STATE_CREDITS,
        FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL,
        DARK_BLUE, LIGHT_BLUE
    )
except ImportError:
    # Fall back to local import for direct execution
    from src.constants import (
        SCREEN_WIDTH, SCREEN_HEIGHT, 
        STATE_PLAYING, STATE_CREDITS,
        FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL,
        DARK_BLUE, LIGHT_BLUE
    )

class Menu:
    """Main menu screen class"""
    
    def __init__(self, assets):
        """Initialize the menu screen"""
        self.assets = assets
        self.next_state = None
        
        # Create fonts
        self.title_font = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.option_font = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.help_font = pygame.font.Font(None, FONT_SIZE_SMALL)
        
        # Create menu options - positioned in bottom right
        button_width = 200
        button_height = 50
        button_spacing = 20
        button_right_margin = 50  # Distance from right edge
        button_bottom_margin = 10  # Distance from bottom edge
        
        self.buttons = [
            {
                'text': 'Launch Game',
                'rect': pygame.Rect(
                    SCREEN_WIDTH - button_width - button_right_margin,
                    SCREEN_HEIGHT - button_bottom_margin - 3 * (button_height + button_spacing),
                    button_width,
                    button_height
                ),
                'action': self.start_game
            },
            {
                'text': 'Credits',
                'rect': pygame.Rect(
                    SCREEN_WIDTH - button_width - button_right_margin,
                    SCREEN_HEIGHT - button_bottom_margin - 2 * (button_height + button_spacing),
                    button_width,
                    button_height
                ),
                'action': self.show_credits
            },
            {
                'text': 'Quit',
                'rect': pygame.Rect(
                    SCREEN_WIDTH - button_width - button_right_margin,
                    SCREEN_HEIGHT - button_bottom_margin - (button_height + button_spacing),
                    button_width,
                    button_height
                ),
                'action': self.quit_game
            }
        ]
        
        # Create background
        self.background = self.create_background()
        
        # Asteroid properties
        self.asteroids = []
        self.explosions = []
        self.create_asteroids(5)  # Start with 5 asteroids
        
        # Load or create asteroid image
        self.asteroid_image = self.create_asteroid_image()
        
    def create_background(self):
        """Create the menu background using the menu background image"""
        menu_bg = self.assets.get_image('menu_background')
        # Scale the background to fit the screen
        return pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    def create_asteroid_image(self):
        """Create a simple asteroid image"""
        size = 40
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Draw a rocky, irregular circle
        points = []
        for i in range(8):
            angle = i * (2 * math.pi / 8)
            radius = random.randint(15, 20)
            x = size//2 + radius * math.cos(angle)
            y = size//2 + radius * math.sin(angle)
            points.append((x, y))
        
        # Draw the asteroid with a gray color and some shading
        pygame.draw.polygon(surface, (100, 100, 100), points)
        pygame.draw.polygon(surface, (80, 80, 80), points, 2)
        
        return surface
    
    def create_asteroids(self, count):
        """Create new asteroids"""
        for _ in range(count):
            # Randomly position asteroids along the edges
            if random.choice([True, False]):
                # Top or bottom
                x = random.randint(0, SCREEN_WIDTH)
                y = random.choice([-50, SCREEN_HEIGHT + 50])
                dx = random.uniform(-2, 2)
                dy = random.uniform(-2, 2) if y > 0 else random.uniform(1, 3)
            else:
                # Left or right
                x = random.choice([-50, SCREEN_WIDTH + 50])
                y = random.randint(0, SCREEN_HEIGHT)
                dx = random.uniform(1, 3) if x < 0 else random.uniform(-3, -1)
                dy = random.uniform(-2, 2)
            
            self.asteroids.append({
                'x': x,
                'y': y,
                'dx': dx,
                'dy': dy,
                'rotation': 0,
                'rotation_speed': random.uniform(-3, 3)
            })
    
    def create_explosion(self, x, y):
        """Create a new explosion effect"""
        self.explosions.append({
            'x': x,
            'y': y,
            'radius': 5,
            'max_radius': 30,
            'alpha': 255
        })
        
    def start_game(self):
        """Start the game with briefing"""
        # Start briefing dialog
        self.assets.briefing.start()
        self.next_state = STATE_PLAYING
        
    def show_credits(self):
        """Show the credits screen"""
        self.next_state = STATE_CREDITS
        
    def quit_game(self):
        """Return to the main launcher"""
        # Instead of quitting the application, we'll just return from the game
        # This will allow the main launcher to regain control
        self.next_state = None  # Clear any pending state transition
        pygame.event.post(pygame.event.Event(pygame.QUIT))  # Post a QUIT event to be handled by the game controller
        return True  # Signal that we want to exit
        
    def handle_input(self, event):
        """Handle user input on the menu screen"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button['rect'].collidepoint(pos):
                        button['action']()
                        # Play sound if available
                        self.assets.play_sound('menu_select')
                        return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Use the same approach as quit_game
                self.next_state = None  # Clear any pending state transition
                pygame.event.post(pygame.event.Event(pygame.QUIT))  # Post a QUIT event
                return True  # Signal that we want to exit
                
        return False
        
    def update(self, events):
        """Update menu state based on events"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Update asteroids
        for asteroid in self.asteroids[:]:
            asteroid['x'] += asteroid['dx']
            asteroid['y'] += asteroid['dy']
            asteroid['rotation'] += asteroid['rotation_speed']
            
            # Remove asteroids that are far off screen
            if (asteroid['x'] < -100 or asteroid['x'] > SCREEN_WIDTH + 100 or
                asteroid['y'] < -100 or asteroid['y'] > SCREEN_HEIGHT + 100):
                self.asteroids.remove(asteroid)
        
        # Create new asteroids to maintain count
        while len(self.asteroids) < 5:
            self.create_asteroids(1)
        
        # Update explosions
        for explosion in self.explosions[:]:
            explosion['radius'] += 2
            explosion['alpha'] -= 10
            if explosion['alpha'] <= 0:
                self.explosions.remove(explosion)
        
        # Process events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check asteroid clicks
                mouse_pos = event.pos
                for asteroid in self.asteroids[:]:
                    # Simple circular collision check
                    asteroid_center = (asteroid['x'] + 20, asteroid['y'] + 20)
                    distance = math.sqrt((mouse_pos[0] - asteroid_center[0])**2 + 
                                      (mouse_pos[1] - asteroid_center[1])**2)
                    if distance < 20:  # Radius for click detection
                        self.create_explosion(asteroid['x'], asteroid['y'])
                        self.asteroids.remove(asteroid)
                        break
                
                # Check if any button was clicked
                for button in self.buttons:
                    if button['rect'].collidepoint(event.pos):
                        result = button['action']()
                        # If the quit button was clicked (returns True), post a QUIT event
                        if result is True:
                            return None  # Return None to indicate no state change
                        return self.next_state
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_game()
                    return None
        
        return None
        
    def draw(self, screen):
        """Draw the menu screen"""
        # Draw background
        screen.blit(self.background, (0, 0))
        
        # Draw asteroids
        for asteroid in self.asteroids:
            # Rotate the asteroid image
            rotated_asteroid = pygame.transform.rotate(self.asteroid_image, asteroid['rotation'])
            # Get the rect for the rotated image
            rect = rotated_asteroid.get_rect(center=(asteroid['x'] + 20, asteroid['y'] + 20))
            screen.blit(rotated_asteroid, rect)
        
        # Draw explosions
        for explosion in self.explosions:
            # Create a surface for the explosion
            explosion_surface = pygame.Surface((explosion['radius']*2, explosion['radius']*2), pygame.SRCALPHA)
            # Draw multiple circles for the explosion effect
            pygame.draw.circle(explosion_surface, (255, 165, 0, explosion['alpha']), 
                             (explosion['radius'], explosion['radius']), explosion['radius'])
            pygame.draw.circle(explosion_surface, (255, 69, 0, explosion['alpha']), 
                             (explosion['radius'], explosion['radius']), explosion['radius']-5)
            screen.blit(explosion_surface, 
                       (explosion['x'] - explosion['radius'], 
                        explosion['y'] - explosion['radius']))
        
        # Draw title
        title_text = "PIG INVADERS"
        subtitle_text = "Space Edition"
        
        title_surface = self.title_font.render(title_text, True, (0, 255, 0))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_surface, title_rect)
        
        subtitle_surface = self.option_font.render(subtitle_text, True, (200, 255, 200))
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(subtitle_surface, subtitle_rect)
        
        # Draw buttons
        for button in self.buttons:
            # Draw semi-transparent background for better visibility
            s = pygame.Surface((button['rect'].width, button['rect'].height))
            s.set_alpha(180)
            s.fill((0, 0, 0))
            screen.blit(s, button['rect'])
            
            # Draw button border
            pygame.draw.rect(screen, (0, 255, 0), button['rect'], 2)
            
            # Draw button text with green color to match title
            text_surface = self.option_font.render(button['text'], True, (0, 255, 0))
            text_rect = text_surface.get_rect(center=button['rect'].center)
            screen.blit(text_surface, text_rect)
            
        # Draw help text
        help_text = "Click to select - ESC to quit"
        help_surface = self.help_font.render(help_text, True, (200, 200, 200))
        help_rect = help_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(help_surface, help_rect)
