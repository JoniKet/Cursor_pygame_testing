import pygame
import sys
import os
import random
import math
from importlib import import_module

# Initialize Pygame
pygame.init()
WIDTH = 1200
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Games Collection")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MENU_BLUE = (100, 149, 237)  # Cornflower blue for menu
SELECTED_COLOR = (255, 255, 0)  # Bright yellow for selected items
HIGHLIGHT_COLOR = (255, 100, 0)  # Bright orange for highlight

class GameLauncher:
    def __init__(self):
        self.games = [
            {
                "name": "Revenge of the Pigs",
                "module": "games.revenge_of_pigs.main",
                "description": "Launch angry birds at pigs in this physics-based game!"
            },
            {
                "name": "Questioning Bird",
                "module": "games.Questioning_bird.main",
                "description": "A top-down game with an existential bird defending against approaching pigs"
            },
            {
                "name": "Snowy Run",
                "module": "games.snowy_run.main",
                "description": "Control a pig on a sledge avoiding birds in this winter sledding game!"
            },
            {
                "name": "Pig Invaders",
                "module": "games.Pig_invaders.main",
                "description": "Classic space invaders with a piggy twist - defend against waves of invading pigs!"
            }
            # Add more games here as they are created
        ]
        self.selected = 0
        
        # Load and scale background image
        try:
            self.background = pygame.image.load("assets/background.png").convert_alpha()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except Exception as e:
            self.background = None
            print(f"Warning: Could not load background image: {e}")
        
        # Fix font initialization to handle potential errors
        try:
            # Try to use the default font
            self.font = pygame.font.Font(None, 54)
            self.selected_font = pygame.font.Font(None, 64)
            self.description_font = pygame.font.Font(None, 28)
        except:
            # Fallback to SysFont if Font fails
            self.font = pygame.font.SysFont('arial', 54)
            self.selected_font = pygame.font.SysFont('arial', 64)
            self.description_font = pygame.font.SysFont('arial', 28)
        
        self.state = "menu"
        
    def draw(self, screen):
        # Draw background
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(BLACK)
            
        # Add a semi-transparent overlay to ensure text remains readable
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(100)
        screen.blit(overlay, (0, 0))
        
        # Draw title
        title = self.font.render("Pygame Games Collection", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//5))
        screen.blit(title, title_rect)
        
        # Draw game options with increased spacing for descriptions
        spacing = 100  # Increased from 80 to give more room for descriptions
        start_y = HEIGHT//3
        
        for i, game in enumerate(self.games):
            option_y = start_y + i * spacing
            
            if i == self.selected:
                # Draw simple selection marker (two lines on each side)
                marker_width = 20
                marker_gap = 5
                left_x = WIDTH//2 - 200
                right_x = WIDTH//2 + 200
                
                # Left markers
                pygame.draw.line(screen, HIGHLIGHT_COLOR, (left_x, option_y - 10), (left_x + marker_width, option_y - 10), 2)
                pygame.draw.line(screen, HIGHLIGHT_COLOR, (left_x, option_y + 10), (left_x + marker_width, option_y + 10), 2)
                
                # Right markers
                pygame.draw.line(screen, HIGHLIGHT_COLOR, (right_x - marker_width, option_y - 10), (right_x, option_y - 10), 2)
                pygame.draw.line(screen, HIGHLIGHT_COLOR, (right_x - marker_width, option_y + 10), (right_x, option_y + 10), 2)
                
                # Selected text
                text = self.selected_font.render(game["name"], True, SELECTED_COLOR)
                rect = text.get_rect(center=(WIDTH//2, option_y))
                
                # Simple highlight box with more vertical space
                highlight_rect = rect.inflate(40, 16)  # Reduced vertical inflation
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, highlight_rect, 2, border_radius=10)
                
                # Description - moved further down
                desc = self.description_font.render(game["description"], True, WHITE)
                desc_rect = desc.get_rect(center=(WIDTH//2, option_y + 40))  # Increased from 30 to 40
                screen.blit(desc, desc_rect)
            else:
                text = self.font.render(game["name"], True, MENU_BLUE)
                rect = text.get_rect(center=(WIDTH//2, option_y))
            
            screen.blit(text, rect)
        
        # Draw quit option
        quit_y = start_y + len(self.games) * spacing
        
        if self.selected == len(self.games):
            # Draw simple selection marker for quit
            marker_width = 20
            left_x = WIDTH//2 - 80
            right_x = WIDTH//2 + 80
            
            # Left markers
            pygame.draw.line(screen, HIGHLIGHT_COLOR, (left_x, quit_y - 10), (left_x + marker_width, quit_y - 10), 2)
            pygame.draw.line(screen, HIGHLIGHT_COLOR, (left_x, quit_y + 10), (left_x + marker_width, quit_y + 10), 2)
            
            # Right markers
            pygame.draw.line(screen, HIGHLIGHT_COLOR, (right_x - marker_width, quit_y - 10), (right_x, quit_y - 10), 2)
            pygame.draw.line(screen, HIGHLIGHT_COLOR, (right_x - marker_width, quit_y + 10), (right_x, quit_y + 10), 2)
            
            quit_text = self.selected_font.render("Quit", True, SELECTED_COLOR)
            quit_rect = quit_text.get_rect(center=(WIDTH//2, quit_y))
            
            # Simple highlight box
            highlight_rect = quit_rect.inflate(40, 20)
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, highlight_rect, 2, border_radius=10)
        else:
            quit_text = self.font.render("Quit", True, MENU_BLUE)
            quit_rect = quit_text.get_rect(center=(WIDTH//2, quit_y))
        
        screen.blit(quit_text, quit_rect)
        
        # Draw navigation instructions at the bottom
        nav_text = self.description_font.render("Use UP/DOWN arrows to navigate, ENTER to select", True, WHITE)
        nav_rect = nav_text.get_rect(center=(WIDTH//2, HEIGHT - 30))
        screen.blit(nav_text, nav_rect)
    
    def handle_input(self, event):
        global screen  # Use the global screen variable
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % (len(self.games) + 1)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % (len(self.games) + 1)
            elif event.key == pygame.K_RETURN:
                if self.selected == len(self.games):  # Quit option
                    return False
                else:
                    # Launch selected game
                    try:
                        game_module = import_module(self.games[self.selected]["module"])
                        # Clear the screen
                        screen.fill(BLACK)
                        pygame.display.flip()
                        
                        # Run the game
                        continue_to_menu = game_module.run_game()
                        
                        # Complete pygame shutdown
                        pygame.mixer.quit()  # Explicitly quit the mixer
                        pygame.quit()        # Completely quit pygame
                        
                        # Reinitialize pygame
                        pygame.init()
                        pygame.font.init()   # Explicitly initialize font system
                        
                        # Reset display
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        pygame.display.set_caption("Pygame Games Collection")
                        
                        # We need to reinitialize the launcher to recreate fonts properly
                        self.__init__()
                        
                        return continue_to_menu
                    except Exception as e:
                        print(f"Error launching game: {e}")
                        # If an error occurred, still try to recover
                        pygame.quit()
                        pygame.init()
                        pygame.font.init()
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        pygame.display.set_caption("Pygame Games Collection")
                        self.__init__()
        return True

def main():
    global screen  # Use the global screen variable
    clock = pygame.time.Clock()
    launcher = GameLauncher()
    running = True
    
    # Create background
    background = pygame.Surface((WIDTH, HEIGHT))
    for y in range(HEIGHT):
        # Create gradient from dark blue to black
        color = (max(0, 20 - y//20), max(0, 30 - y//20), max(0, 50 - y//20))
        pygame.draw.line(background, color, (0, y), (WIDTH, y))
    
    while running:
        # Ensure pygame is initialized
        if not pygame.get_init():
            pygame.init()
            pygame.font.init()  # Explicitly initialize the font system
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Pygame Games Collection")
            # Reinitialize launcher to recreate fonts
            launcher = GameLauncher()
        
        screen.blit(background, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                running = launcher.handle_input(event)
        
        launcher.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 