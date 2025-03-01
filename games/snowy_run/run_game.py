import os
import sys

# Add the project root to the path
current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import and run the game
from games.snowy_run.main import run_game

if __name__ == "__main__":
    run_game() 