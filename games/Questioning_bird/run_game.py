import os
import sys
import pygame

# Add the src directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Import directly from src
from game_controller import GameController

def main():
    """Main entry point for the game"""
    # Initialize pygame
    pygame.init()
    
    # Create and run the game controller
    controller = GameController()
    controller.run()

if __name__ == "__main__":
    main() 