import pygame
import random
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
        SCREEN_WIDTH, SCREEN_HEIGHT, STATE_MENU, STATE_PLAYING,
        FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL
    )
except ImportError:
    # Fall back to local import for direct execution
    from src.constants import (
        SCREEN_WIDTH, SCREEN_HEIGHT, STATE_MENU, STATE_PLAYING,
        FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL
    )

class GameOver:
    """Game over screen class"""
    
    def __init__(self, assets):
        """Initialize the game over screen"""
        self.assets = assets
        self.score = 0
        self.next_state = None
        self.victory = False  # Default to defeat
        
        # Create fonts
        self.title_font = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.score_font = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.option_font = pygame.font.Font(None, FONT_SIZE_SMALL)
        
        # Create buttons
        self.buttons = [
            {
                'text': 'Play Again',
                'rect': pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50),
                'action': self.play_again
            },
            {
                'text': 'Main Menu',
                'rect': pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120, 200, 50),
                'action': self.main_menu
            }
        ]
        
        # Create existential questions
        self.questions = [
            "Was it worth it?",
            "Did the pigs deserve this?",
            "What meaning did this bring?",
            "Will doing it again change anything?",
            "Does any of this matter?",
            "Are you at peace with your actions?",
            "Has this made you a better person?",
            "Could there have been another way?",
            "Did you enjoy their suffering?",
            "Will you feel remorse?",
            "Were the pigs simply misunderstood?",
            "Is victory the same as virtue?",
            "What have you truly gained from this?",
            "Is there purpose in repetition?",
            "Have you learned anything about yourself?",
            "Does the bird's questioning disturb you?",
            "Is this ending truly satisfying?",
            "Would the pigs forgive you if they could?",
            "What will you think about when this game is forgotten?",
            "Is it the journey or the score that matters?"
        ]
        self.question = random.choice(self.questions)
        self.question_timer = 0
        self.question_change_delay = 240  # Change question every 4 seconds
        
    def set_score(self, score):
        """Set the final score to display"""
        self.score = score
        
    def set_victory(self, victory):
        """Set whether the player won or lost"""
        self.victory = victory
        
    def play_again(self):
        """Return to the game state"""
        self.next_state = STATE_PLAYING
        
    def main_menu(self):
        """Return to the main menu"""
        self.next_state = STATE_MENU
        
    def handle_input(self, event):
        """Handle user input on the game over screen"""
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
                self.next_state = STATE_MENU
                return False
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.play_again()
                return False
                
        return False
        
    def update(self):
        """Update the game over screen state"""
        # Update question periodically
        self.question_timer += 1
        if self.question_timer >= self.question_change_delay:
            self.question_timer = 0
            self.question = random.choice(self.questions)
        
    def draw(self, screen):
        """Draw the game over screen"""
        # Draw a dark overlay for the background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((20, 20, 40))
        overlay.set_alpha(240)  # Semi-transparent
        screen.blit(overlay, (0, 0))
        
        # Draw game over title with different color based on victory/defeat
        if self.victory:
            title_text = "VICTORY!"
            title_color = (50, 255, 50)  # Green for victory
        else:
            title_text = "GAME OVER"
            title_color = (255, 50, 50)  # Red for defeat
            
        title_surface = self.title_font.render(title_text, True, title_color)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surface, title_rect)
        
        # Draw score
        score_text = f"Your Score: {self.score}"
        score_surface = self.score_font.render(score_text, True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 170))
        screen.blit(score_surface, score_rect)
        
        # Draw outcome message
        if self.victory:
            outcome_text = "A pig has reached you! Your existential crisis is resolved."
        else:
            outcome_text = "You shot too many pigs. Your guilt is overwhelming."
            
        outcome_surface = self.option_font.render(outcome_text, True, (200, 200, 255))
        outcome_rect = outcome_surface.get_rect(center=(SCREEN_WIDTH // 2, 210))
        screen.blit(outcome_surface, outcome_rect)
        
        # Draw existential question
        question_surface = self.option_font.render(self.question, True, (200, 200, 100))
        question_rect = question_surface.get_rect(center=(SCREEN_WIDTH // 2, 250))
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