import pygame
import os
import sys

# Add parent directory to path for direct execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    # Try importing with full package path first (when run through main launcher)
    from games.Questioning_bird.src.constants import (
        SCREEN_WIDTH, SCREEN_HEIGHT, 
        STATE_MENU, STATE_PLAYING, STATE_GAME_OVER, STATE_CREDITS
    )
    from games.Questioning_bird.src.assets import Assets
    from games.Questioning_bird.src.game import Game
    from games.Questioning_bird.src.ui.menu import Menu
    from games.Questioning_bird.src.ui.credits import Credits
    from games.Questioning_bird.src.ui.game_over import GameOver
except ImportError:
    # Fall back to local import for direct execution
    from src.constants import (
        SCREEN_WIDTH, SCREEN_HEIGHT,
        STATE_MENU, STATE_PLAYING, STATE_GAME_OVER, STATE_CREDITS
    )
    from src.assets import Assets
    from src.game import Game
    from src.ui.menu import Menu
    from src.ui.credits import Credits
    from src.ui.game_over import GameOver

class GameController:
    """Main game controller that manages game states and transitions"""
    
    def __init__(self):
        """Initialize the game controller"""
        pygame.init()
        pygame.mixer.init()
        
        # Set up display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Questioning Bird - Top-Down Edition")
        
        # Load assets
        self.assets = Assets()
        
        # Set up game states
        self.states = {
            STATE_MENU: Menu(self.assets),
            STATE_PLAYING: Game(self.assets),
            STATE_GAME_OVER: GameOver(self.assets),
            STATE_CREDITS: Credits(self.assets)
        }
        
        # Set initial state
        self.current_state = STATE_MENU
        
        # Game clock
        self.clock = pygame.time.Clock()
        self.running = True
        
    def run(self):
        """Run the main game loop"""
        while self.running:
            # Delta time for frame rate independence
            dt = self.clock.tick(60) / 1000.0
            
            # Get events once per frame
            events = pygame.event.get()
            
            # Process events
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    
                # Pass events to current state
                state_obj = self.states[self.current_state]
                if hasattr(state_obj, 'handle_input'):
                    exit_requested = state_obj.handle_input(event)
                    if exit_requested:
                        # Instead of exiting the application, we'll just return from the game
                        # This will allow the main launcher to regain control
                        self.running = False
            
            # Update current state
            state_obj = self.states[self.current_state]
            if hasattr(state_obj, 'update'):
                # If it's the menu state and update accepts events parameter
                if self.current_state == STATE_MENU:
                    next_state = state_obj.update(events)
                    if next_state is not None:
                        state_obj.next_state = next_state
                else:
                    # Regular update for other states
                    state_obj.update()
                
            # Check for state transitions
            if hasattr(state_obj, 'next_state') and state_obj.next_state is not None:
                # Reset the previous state if needed
                if hasattr(state_obj, 'reset'):
                    state_obj.reset()
                    
                # Transition to new state
                next_state = state_obj.next_state
                state_obj.next_state = None
                
                # If it's a game over, update the score
                if next_state == STATE_GAME_OVER and self.current_state == STATE_PLAYING:
                    self.states[STATE_GAME_OVER].set_score(state_obj.score)
                    # Pass victory state if available
                    if hasattr(state_obj, 'victory'):
                        self.states[STATE_GAME_OVER].set_victory(state_obj.victory)
                    
                # Update current state
                self.current_state = next_state
                
                # If we're going back to playing, reset the game
                if self.current_state == STATE_PLAYING:
                    self.states[STATE_PLAYING] = Game(self.assets)
            
            # Draw current state
            self.screen.fill((0, 0, 0))  # Clear screen
            if hasattr(state_obj, 'draw'):
                state_obj.draw(self.screen)
                
            # Update display
            pygame.display.flip()
            
        # Clean up but don't exit the application
        pygame.quit()
        # Return True instead of 0 to signal to the main launcher to continue running
        return True 