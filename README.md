# Pygame Games Collection

A collection of fun games built with Pygame.

## Games

### 1. Revenge of the Pigs
A physics-based game where you launch pigs at angry birds! Turn the tables on those pesky birds and get your revenge.

Features:
- Physics-based gameplay with realistic collisions
- Slingshot mechanics
- Destructible blocks and birds
- Particle effects for explosions

## Project Structure
```
.
├── main.py              # Main game launcher
├── requirements.txt     # Python dependencies
├── games/              # Games directory
│   ├── __init__.py
│   └── revenge_of_pigs/ # Revenge of the Pigs game
│       ├── __init__.py
│       ├── assets/     # Game assets
│       └── revenge_of_pigs.py
```

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Games

1. Run the main launcher:
```bash
python main.py
```

2. Use the arrow keys to select a game and press ENTER to play
3. Press ESC to return to the game selection menu
4. Select "Quit" to exit

## Dependencies
- Python 3.x
- Pygame
- Pymunk (for physics) 