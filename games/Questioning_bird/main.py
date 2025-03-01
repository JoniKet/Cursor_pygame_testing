import os
import sys

# Add current directory to Python path for direct execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    # Try importing with full package path first (when run through main launcher)
    from games.Questioning_bird.src.game_controller import GameController
except ImportError:
    # Fall back to local import for direct execution
    from src.game_controller import GameController

def run_game():
    """Entry point for Questioning Bird game"""
    controller = GameController()
    return controller.run()

if __name__ == "__main__":
    sys.exit(run_game()) 