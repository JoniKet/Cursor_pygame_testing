import pygame
import os
import sys
import random

# Add parent directory to path for direct execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    # Try importing with full package path first (when run through main launcher)
    from games.Questioning_bird.src.constants import (
        SCREEN_WIDTH, SCREEN_HEIGHT, 
        STATE_PLAYING, STATE_CREDITS,
        FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL
    )
except ImportError:
    # Fall back to local import for direct execution
    from src.constants import (
        SCREEN_WIDTH, SCREEN_HEIGHT, 
        STATE_PLAYING, STATE_CREDITS,
        FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL
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
        
        # Create menu options
        self.buttons = [
            {
                'text': 'Play Game',
                'rect': pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50),
                'action': self.start_game
            },
            {
                'text': 'Credits',
                'rect': pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50),
                'action': self.show_credits
            },
            {
                'text': 'Quit',
                'rect': pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 140, 200, 50),
                'action': self.quit_game
            }
        ]
        
        # Create background
        self.background = self.create_background()
        
        # Create philosophical questions
        self.questions = [
            "Why do birds question things?",
            "What is the nature of consciousness?",
            "Are games a reflection of reality?",
            "Does playing change who you are?",
            "What makes a game worth playing?",
            "Why must birds and pigs be enemies?",
            "Is conflict inevitable?",
            "Can a game make you think?",
            "What lies beyond the screen?",
            "Will you find meaning here?",
            "Is this game playing you?",
            "Are you the controller, or the controlled?",
            "How real is your experience right now?",
            "Does a digital bird dream?",
            "Can pixels have consciousness?",
            "Is entertainment a form of enlightenment?",
            "Why do we enjoy virtual conflict?",
            "Who decided birds and pigs are enemies?",
            "Is a game without purpose still a game?",
            "Are you choosing to play, or are you compelled?"
        ]
        self.question = random.choice(self.questions)
        self.question_timer = 0
        self.question_change_delay = 180  # Change question every 3 seconds (60 frames/second)
        
    def create_background(self):
        """Create a simple menu background"""
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg.fill((30, 30, 60))  # Dark blue-ish background
        
        # Add some decorative elements
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            radius = random.randint(1, 3)
            color = (random.randint(200, 255), random.randint(200, 255), 255)
            pygame.draw.circle(bg, color, (x, y), radius)
            
        return bg
        
    def start_game(self):
        """Start the game"""
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
        # Update philosophical question periodically
        self.question_timer += 1
        if self.question_timer >= self.question_change_delay:
            self.question_timer = 0
            self.question = random.choice(self.questions)
            
        # Process events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
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
        
        # Draw title
        title_text = "Questioning Bird"
        subtitle_text = "Top-Down Edition"
        
        title_surface = self.title_font.render(title_text, True, (255, 255, 0))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)
        
        subtitle_surface = self.option_font.render(subtitle_text, True, (255, 255, 255))
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(subtitle_surface, subtitle_rect)
        
        # Draw philosophical question
        question_surface = self.help_font.render(self.question, True, (200, 200, 200))
        question_rect = question_surface.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(question_surface, question_rect)
        
        # Draw buttons
        for button in self.buttons:
            # Draw button background
            pygame.draw.rect(screen, (60, 60, 100), button['rect'])
            pygame.draw.rect(screen, (150, 150, 200), button['rect'], 2)
            
            # Draw button text
            text_surface = self.option_font.render(button['text'], True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button['rect'].center)
            screen.blit(text_surface, text_rect)
            
        # Draw help text
        help_text = "Click to select - ESC to quit"
        help_surface = self.help_font.render(help_text, True, (200, 200, 200))
        help_rect = help_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(help_surface, help_rect) 