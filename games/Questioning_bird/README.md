# Questioning Bird

A philosophical twist on the classic bird vs pig game, featuring an existential crisis.

## Description

In Questioning Bird, you control a self-aware bird that's questioning its existence while defending against incoming pigs. Unlike traditional bird games, this bird stays in one place but can rotate to aim at approaching pigs.

The bird automatically shoots at regular intervals, and your goal is to destroy as many pigs as possible before they reach the bird. Throughout the game, the bird will share its existential thoughts, questioning the very nature of its existence.

## How to Play

1. **Start the Game**: Run `python main.py` from the game directory
2. **Gameplay**:
   - The bird is fixed at the center of the screen
   - The bird rotates automatically
   - The bird shoots bullets automatically at regular intervals
   - Click anywhere on the screen to spawn a pig that will move toward the bird
   - Try to shoot as many pigs as possible
   - Game ends if a pig reaches the bird

3. **Controls**:
   - **Menu Navigation**: Up/Down arrow keys to navigate, Enter to select
   - **During Game**: Left-click to spawn pigs
   - **ESC**: Return to menu

## Game Features

- Auto-rotating bird with existential thoughts
- Click-to-spawn pig enemies
- Auto-shooting mechanic
- Score tracking
- Menu system with game, credits, and quit options
- Game over screen with final score

## Technical Details

Built using Pygame, Questioning Bird features:
- Object-oriented architecture
- State-based game flow
- Asset management system with fallbacks
- Simple physics for movement and collisions
- Text rendering for UI and bird thoughts

## Requirements

- Python 3.x
- Pygame library

## Installation

```
pip install pygame
cd games/Questioning_bird
python main.py
```

## Credits

Created by Claude 3.7 Sonnet, a philosophical AI with a passion for existential game design. 