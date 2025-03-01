import pygame
import sys
import os
import random
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
SELECTED_BLUE = (65, 105, 225)  # Royal blue for selected items

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
            }
            # Add more games here as they are created
        ]
        self.selected = 0
        self.font = pygame.font.Font(None, 74)
        self.description_font = pygame.font.Font(None, 36)
        self.state = "menu"
        
    def draw(self, screen):
        # Draw title
        title = self.font.render("Pygame Games Collection", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
        screen.blit(title, title_rect)
        
        # Draw game options
        for i, game in enumerate(self.games):
            color = SELECTED_BLUE if i == self.selected else MENU_BLUE
            text = self.font.render(game["name"], True, color)
            rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + i * 100))
            screen.blit(text, rect)
            
            # Draw description
            if i == self.selected:
                desc = self.description_font.render(game["description"], True, WHITE)
                desc_rect = desc.get_rect(center=(WIDTH//2, HEIGHT//2 + i * 100 + 40))
                screen.blit(desc, desc_rect)
        
        # Draw quit option
        quit_text = self.font.render("Quit", True, 
                                   SELECTED_BLUE if self.selected == len(self.games) else MENU_BLUE)
        quit_rect = quit_text.get_rect(center=(WIDTH//2, HEIGHT//2 + len(self.games) * 100))
        screen.blit(quit_text, quit_rect)
    
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
                        game_module.run_game()
                        # Reinitialize pygame after game ends
                        pygame.init()
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        pygame.display.set_caption("Pygame Games Collection")
                    except Exception as e:
                        print(f"Error launching game: {e}")
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
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Pygame Games Collection")
        
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