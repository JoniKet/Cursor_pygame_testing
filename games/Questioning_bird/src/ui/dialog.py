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
        SCREEN_WIDTH, SCREEN_HEIGHT, 
        FONT_SIZE_MEDIUM, FONT_SIZE_SMALL
    )
except ImportError:
    # Fall back to local import for direct execution
    from src.constants import (
        SCREEN_WIDTH, SCREEN_HEIGHT, 
        FONT_SIZE_MEDIUM, FONT_SIZE_SMALL
    )

class DialogPopup:
    """Dialog popup for bird questions"""
    
    def __init__(self, question_data, assets):
        """Initialize the dialog popup with question data"""
        self.assets = assets
        self.question = question_data["question"]
        self.options = question_data["options"]
        self.responses = question_data["responses"]
        self.selected_option = None
        self.active = True
        
        # Create fonts
        self.question_font = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.option_font = pygame.font.Font(None, FONT_SIZE_SMALL)
        
        # Calculate popup dimensions
        self.width = SCREEN_WIDTH * 0.8
        self.height = SCREEN_HEIGHT * 0.4
        self.x = (SCREEN_WIDTH - self.width) / 2
        self.y = (SCREEN_HEIGHT - self.height) / 2
        
        # Create option buttons
        self.buttons = []
        for i, option in enumerate(self.options):
            button_width = self.width * 0.8
            button_height = 40
            button_x = self.x + (self.width - button_width) / 2
            button_y = self.y + self.height * 0.4 + i * (button_height + 10)
            
            self.buttons.append({
                'text': option,
                'rect': pygame.Rect(button_x, button_y, button_width, button_height),
                'index': i
            })
        
        # Play question sound when dialog appears
        self.assets.play_sound('question', volume=0.8)
    
    def handle_input(self, event):
        """Handle user input for the dialog popup"""
        if not self.active:
            return None
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button['rect'].collidepoint(pos):
                        self.selected_option = button['index']
                        self.active = False
                        # Play sound when option is selected
                        self.assets.play_sound('menu_select', volume=0.7)
                        return self.selected_option
        elif event.type == pygame.MOUSEMOTION:
            # Check if mouse is hovering over any button
            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                # If mouse just entered the button, play a subtle hover sound
                if button['rect'].collidepoint(pos) and not hasattr(button, 'hovered'):
                    button['hovered'] = True
                    # Play a very quiet menu sound for hover
                    self.assets.play_sound('menu_select', volume=0.1)
                elif not button['rect'].collidepoint(pos) and hasattr(button, 'hovered'):
                    button.pop('hovered', None)
        
        return None
    
    def draw(self, screen):
        """Draw the dialog popup"""
        if not self.active:
            return
            
        # Draw semi-transparent background overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150)
        screen.blit(overlay, (0, 0))
        
        # Draw popup background
        popup_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (50, 50, 80), popup_rect)
        pygame.draw.rect(screen, (100, 100, 150), popup_rect, 3)
        
        # Draw question
        question_surface = self.question_font.render(self.question, True, (255, 255, 200))
        question_rect = question_surface.get_rect(center=(SCREEN_WIDTH / 2, self.y + self.height * 0.2))
        screen.blit(question_surface, question_rect)
        
        # Draw options
        for button in self.buttons:
            # Draw button background
            hover = button['rect'].collidepoint(pygame.mouse.get_pos())
            color = (80, 80, 120) if hover else (60, 60, 100)
            pygame.draw.rect(screen, color, button['rect'])
            pygame.draw.rect(screen, (150, 150, 200), button['rect'], 2)
            
            # Draw button text
            text_surface = self.option_font.render(button['text'], True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button['rect'].center)
            screen.blit(text_surface, text_rect) 