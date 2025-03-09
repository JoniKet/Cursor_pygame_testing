#!/usr/bin/env python3
import os
import sys
import pygame

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import the main game module
from main import run_game

if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    
    # Run the game
    run_game()
