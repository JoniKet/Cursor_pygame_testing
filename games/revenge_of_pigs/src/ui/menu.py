import pygame
from pygame.locals import *
from ..constants import WIDTH, HEIGHT, WHITE, MENU_BLUE, SELECTED_BLUE
from ..effects.victory_effect import VictoryEffect
from ..entities.block import AngryBirdBlock

class Menu:
    def __init__(self):
        self.options = ["Play", "Level Editor", "Credits", "Quit"]
        self.selected = 0
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        self.instruction_font = pygame.font.Font(None, 32)  # Increased font size for instructions
        self.state = "menu"  # menu, game, editor, credits, victory
        self.score = 0  # Initialize score
        self.victory_effect = None
        
    def draw(self, screen):
        if self.state == "menu":
            # Draw title
            title = self.font.render("Revenge of the Pigs!", True, WHITE)
            title_rect = title.get_rect(center=(WIDTH//2, 100))  # Fixed position
            screen.blit(title, title_rect)
            
            # Draw menu options with fixed positions
            menu_start_y = 250  # Start menu items lower
            for i, option in enumerate(self.options):
                color = SELECTED_BLUE if i == self.selected else MENU_BLUE
                text = self.font.render(option, True, color)
                rect = text.get_rect(center=(WIDTH//2, menu_start_y + i * 60))
                screen.blit(text, rect)
            
            # Draw instructions with solid background
            instructions = [
                "HOW TO PLAY:",
                "1. Click and drag the pig in the slingshot",
                "2. Release to launch!",
                "3. Destroy all angry birds to win",
                "4. Wooden blocks can be destroyed with multiple hits",
                "5. Each destroyed bird is worth 1000 points",
                "6. Press 'R' to reset the pig to the slingshot"
            ]
            
            # Draw solid background box for instructions
            box_width = 600
            box_height = 250  # Increased height for additional instruction
            box_x = WIDTH//2 - box_width//2
            box_y = 500  # Fixed position
            pygame.draw.rect(screen, (0, 0, 50), (box_x, box_y, box_width, box_height))  # Dark blue background
            pygame.draw.rect(screen, MENU_BLUE, (box_x, box_y, box_width, box_height), 2)  # Blue border
            
            # Draw instructions text
            for i, line in enumerate(instructions):
                color = SELECTED_BLUE if i == 0 else WHITE
                text = self.instruction_font.render(line, True, color)
                rect = text.get_rect(center=(WIDTH//2, box_y + 30 + i * 32))
                screen.blit(text, rect)
                
        elif self.state == "credits":
            # Draw credits
            credits = [
                "Credits",
                "",
                "Game created by Claude AI",
                "A powerful AI assistant by Anthropic",
                "",
                "Developed in Cursor IDE",
                "",
                "Press ESC to return to menu"
            ]
            
            for i, line in enumerate(credits):
                if i == 0:  # Title
                    text = self.font.render(line, True, WHITE)
                else:  # Regular text
                    text = self.small_font.render(line, True, WHITE)
                rect = text.get_rect(center=(WIDTH//2, HEIGHT//4 + i * 50))
                screen.blit(text, rect)
    
    def check_victory(self, blocks):
        # Check if all birds are destroyed
        birds_remaining = False
        for block in blocks:
            if isinstance(block, AngryBirdBlock) and not block.destroyed:
                birds_remaining = True
                break
        
        if not birds_remaining:
            self.state = "victory"
            if self.victory_effect is None:
                self.victory_effect = VictoryEffect(WIDTH, HEIGHT)

    def handle_input(self, event):
        if self.state == "menu":
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == K_RETURN:
                    if self.options[self.selected] == "Play":
                        self.state = "game"
                        self.victory_effect = None  # Reset victory effect
                    elif self.options[self.selected] == "Level Editor":
                        self.state = "editor"
                    elif self.options[self.selected] == "Credits":
                        self.state = "credits"
                    elif self.options[self.selected] == "Quit":
                        return False
        elif self.state == "credits" or self.state == "victory":
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.state = "menu"
                self.victory_effect = None  # Clear victory effect
        
        return True 