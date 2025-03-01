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
            }
            # Add more games here as they are created
        ]
        self.selected = 0
        
        # Fix font initialization to handle potential errors
        try:
            # Try to use the default font
            self.font = pygame.font.Font(None, 74)
            self.selected_font = pygame.font.Font(None, 84)
            self.description_font = pygame.font.Font(None, 36)
        except:
            # Fallback to SysFont if Font fails
            self.font = pygame.font.SysFont('arial', 74)
            self.selected_font = pygame.font.SysFont('arial', 84)
            self.description_font = pygame.font.SysFont('arial', 36)
        
        self.state = "menu"
        self.selection_animation = 0  # Animation counter
        
    def draw(self, screen):
        # Update animation counter
        self.selection_animation = (self.selection_animation + 0.1) % (2 * 3.14159)
        pulse_value = abs(math.sin(self.selection_animation))  # Pulsing effect
        
        # Draw title
        title = self.font.render("Pygame Games Collection", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
        screen.blit(title, title_rect)
        
        # Draw game options
        for i, game in enumerate(self.games):
            option_y = HEIGHT//2 + i * 100
            
            if i == self.selected:
                # Draw selection indicators (arrows on both sides)
                left_arrow_x = WIDTH//2 - 250 - 10 * pulse_value
                right_arrow_x = WIDTH//2 + 250 + 10 * pulse_value
                
                # Left arrow
                pygame.draw.polygon(screen, HIGHLIGHT_COLOR, [
                    (left_arrow_x, option_y),
                    (left_arrow_x - 30, option_y - 20),
                    (left_arrow_x - 30, option_y + 20)
                ])
                
                # Right arrow (pointing left)
                pygame.draw.polygon(screen, HIGHLIGHT_COLOR, [
                    (right_arrow_x, option_y),
                    (right_arrow_x + 30, option_y - 20),
                    (right_arrow_x + 30, option_y + 20)
                ])
                
                # Use bigger, brighter text for selected item
                text = self.selected_font.render(game["name"], True, SELECTED_COLOR)
                rect = text.get_rect(center=(WIDTH//2, option_y))
                
                # Draw highlight box with pulsing effect
                highlight_rect = rect.inflate(60 + 20 * pulse_value, 30 + 10 * pulse_value)
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, highlight_rect, 4, border_radius=15)
                
                # Add a subtle background fill to make it stand out more
                inner_rect = rect.inflate(40, 20)
                s = pygame.Surface((inner_rect.width, inner_rect.height))
                s.set_alpha(50)  # Transparent
                s.fill(HIGHLIGHT_COLOR)
                screen.blit(s, inner_rect)
            else:
                text = self.font.render(game["name"], True, MENU_BLUE)
                rect = text.get_rect(center=(WIDTH//2, option_y))
            
            screen.blit(text, rect)
            
            # Draw description
            if i == self.selected:
                desc = self.description_font.render(game["description"], True, WHITE)
                desc_rect = desc.get_rect(center=(WIDTH//2, option_y + 40))
                screen.blit(desc, desc_rect)
        
        # Draw quit option
        quit_y = HEIGHT//2 + len(self.games) * 100
        
        if self.selected == len(self.games):
            # Draw selection indicators (arrows on both sides) for quit
            left_arrow_x = WIDTH//2 - 100 - 10 * pulse_value
            right_arrow_x = WIDTH//2 + 100 + 10 * pulse_value
            
            # Left arrow
            pygame.draw.polygon(screen, HIGHLIGHT_COLOR, [
                (left_arrow_x, quit_y),
                (left_arrow_x - 30, quit_y - 20),
                (left_arrow_x - 30, quit_y + 20)
            ])
            
            # Right arrow (pointing left)
            pygame.draw.polygon(screen, HIGHLIGHT_COLOR, [
                (right_arrow_x, quit_y),
                (right_arrow_x + 30, quit_y - 20),
                (right_arrow_x + 30, quit_y + 20)
            ])
            
            quit_text = self.selected_font.render("Quit", True, SELECTED_COLOR)
            quit_rect = quit_text.get_rect(center=(WIDTH//2, quit_y))
            
            # Draw highlight box
            highlight_rect = quit_rect.inflate(60 + 20 * pulse_value, 30 + 10 * pulse_value)
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, highlight_rect, 4, border_radius=15)
            
            # Add a subtle background fill
            inner_rect = quit_rect.inflate(40, 20)
            s = pygame.Surface((inner_rect.width, inner_rect.height))
            s.set_alpha(50)  # Transparent
            s.fill(HIGHLIGHT_COLOR)
            screen.blit(s, inner_rect)
        else:
            quit_text = self.font.render("Quit", True, MENU_BLUE)
            quit_rect = quit_text.get_rect(center=(WIDTH//2, quit_y))
        
        screen.blit(quit_text, quit_rect)
        
        # Draw navigation instructions at the bottom
        nav_text = self.description_font.render("Use UP/DOWN arrows to navigate, ENTER to select", True, WHITE)
        nav_rect = nav_text.get_rect(center=(WIDTH//2, HEIGHT - 50))
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