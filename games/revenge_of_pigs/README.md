# Revenge of the Pigs

A physics-based game where you play as a pig seeking revenge against angry birds! Launch yourself from a slingshot to destroy the birds and their wooden fortifications.

## Features

- Physics-based gameplay with realistic collisions and trajectories
- Multiple target types:
  - Angry birds that explode on impact
  - Wooden blocks that can be damaged and destroyed
- Score system with points for destroying birds
- Level editor to create custom challenges
- Victory celebration with particle effects
- Clean, intuitive menu system

## Installation

1. Ensure you have Python 3.8 or higher installed
2. Install required packages:
   ```bash
   pip install pygame pymunk
   ```
3. Run the game:
   ```bash
   python main.py
   ```

## Controls

- **Mouse**: Click and drag the pig to aim
- **Mouse Release**: Launch the pig
- **R**: Reset pig position to slingshot
- **ESC**: Return to menu
- **Arrow Keys**: Navigate menu
- **Enter**: Select menu option

## Level Editor

Create your own levels with the built-in editor:
1. Select block type (Bird/Wood)
2. Click on grid to place blocks
3. Use buttons to:
   - Clear level
   - Save level
   - Load level
   - Test your creation

## Scoring

- Each destroyed angry bird: 1000 points
- Destroy all birds to win!

## Development

See [CHANGELOG.md](CHANGELOG.md) for detailed development history and updates.

## Credits

- Created by Claude AI
- Developed in Cursor IDE
- Uses Pygame and Pymunk for physics simulation 