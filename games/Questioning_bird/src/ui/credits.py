import pygame
import os
import sys

# Add parent directory to path for direct execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    # Try importing with full package path first (when run through main launcher)
    from games.Questioning_bird.src.constants import (
        SCREEN_WIDTH, SCREEN_HEIGHT, STATE_MENU,
        FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL
    )
except ImportError:
    # Fall back to local import for direct execution
    from src.constants import (
        SCREEN_WIDTH, SCREEN_HEIGHT, STATE_MENU,
        FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL
    )

class Credits:
    """Credits screen class"""
    
    def __init__(self, assets):
        """Initialize the credits screen"""
        self.assets = assets
        self.next_state = None
        
        # Create fonts
        self.title_font = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.subtitle_font = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.text_font = pygame.font.Font(None, FONT_SIZE_SMALL)
        
        # Create back button
        self.back_button = {
            'text': 'Back to Menu',
            'rect': pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50),
            'action': self.go_to_menu
        }
        
        # Credits content
        self.credits = [
            {"title": "Questioning Bird", "text": "Top-Down Edition", "type": "title"},
            {"title": "Game Concept", "text": "A game about a bird questioning its existence while defending itself from pigs", "type": "section"},
            {"title": "How to Play", "text": "- Click to spawn pigs that will chase the bird", "type": "content"},
            {"text": "- Bird automatically shoots bullets at pigs", "type": "content"},
            {"text": "- Score points by shooting pigs", "type": "content"},
            {"text": "- Game ends if a pig reaches the bird", "type": "content"},
            {"title": "Game Philosophy", "text": "This game is a meditation on existence, free will, and the nature of conflict", "type": "section"},
            {"title": "Created With", "text": "Python and Pygame", "type": "section"},
            {"title": "Version", "text": "1.0", "type": "content"},
        ]
        
        # Scroll position
        self.scroll_y = 0
        self.scroll_speed = 2
        
    def go_to_menu(self):
        """Return to the main menu"""
        self.next_state = STATE_MENU
        
    def handle_input(self, event):
        """Handle user input on the credits screen"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                pos = pygame.mouse.get_pos()
                if self.back_button['rect'].collidepoint(pos):
                    self.back_button['action']()
                    # Play sound if available
                    self.assets.play_sound('menu_select')
            elif event.button == 4:  # Mouse wheel up
                self.scroll_y += 20
            elif event.button == 5:  # Mouse wheel down
                self.scroll_y -= 20
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = STATE_MENU
            elif event.key == pygame.K_UP:
                self.scroll_y += 20
            elif event.key == pygame.K_DOWN:
                self.scroll_y -= 20
                
        return False
        
    def update(self):
        """Update credits screen state (scroll animation)"""
        # Auto-scroll
        self.scroll_y -= self.scroll_speed * 0.1
        
        # Limit scrolling
        max_scroll = -800  # Adjust based on content height
        self.scroll_y = max(max_scroll, min(0, self.scroll_y))
        
    def draw(self, screen):
        """Draw the credits screen"""
        # Fill background
        screen.fill((20, 20, 40))
        
        # Draw scrolling credits
        y_pos = self.scroll_y + 100
        
        for item in self.credits:
            if item['type'] == 'title':
                # Draw title
                title_surface = self.title_font.render(item['title'], True, (255, 255, 0))
                title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
                screen.blit(title_surface, title_rect)
                
                # Draw subtitle
                subtitle_surface = self.subtitle_font.render(item['text'], True, (255, 255, 255))
                subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos + 50))
                screen.blit(subtitle_surface, subtitle_rect)
                
                y_pos += 100
            elif item['type'] == 'section':
                # Draw section title
                section_surface = self.subtitle_font.render(item['title'], True, (200, 200, 255))
                section_rect = section_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
                screen.blit(section_surface, section_rect)
                
                # Draw section text
                if 'text' in item:
                    text_surface = self.text_font.render(item['text'], True, (200, 200, 200))
                    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos + 30))
                    screen.blit(text_surface, text_rect)
                
                y_pos += 80
            else:  # content
                if 'title' in item:
                    # Draw content title
                    title_surface = self.text_font.render(item['title'], True, (255, 255, 255))
                    title_rect = title_surface.get_rect(midleft=(SCREEN_WIDTH // 4, y_pos))
                    screen.blit(title_surface, title_rect)
                    
                # Draw content text
                text_surface = self.text_font.render(item['text'], True, (200, 200, 200))
                if 'title' in item:
                    text_rect = text_surface.get_rect(midleft=(SCREEN_WIDTH // 2, y_pos))
                else:
                    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
                screen.blit(text_surface, text_rect)
                
                y_pos += 40
        
        # Draw back button
        pygame.draw.rect(screen, (60, 60, 100), self.back_button['rect'])
        pygame.draw.rect(screen, (150, 150, 200), self.back_button['rect'], 2)
        
        text_surface = self.subtitle_font.render(self.back_button['text'], True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.back_button['rect'].center)
        screen.blit(text_surface, text_rect)
        
        # Draw scroll instructions
        help_text = "Use mouse wheel or arrow keys to scroll"
        help_surface = self.text_font.render(help_text, True, (150, 150, 150))
        help_rect = help_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(help_surface, help_rect) 