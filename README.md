# Pygame Games Collection - A Cursor AI Project

A collection of fun games built with Pygame, created **entirely through AI prompting** using Cursor AI.

## About This Project

This project demonstrates the capabilities of AI-assisted coding using Cursor AI. **Zero manual coding** was done in the creation of these games - everything was accomplished through natural language prompting with the Cursor AI agent.

The entire codebase, including:
- Game mechanics
- Graphics rendering
- Physics
- Sound generation
- User interfaces
- AI behaviors

...was created solely through conversation with the AI. This showcases how modern AI tools can be used to create functional, entertaining software without writing a single line of code manually.

## Games

### 1. Revenge of the Pigs
A physics-based game where you launch pigs at angry birds! Turn the tables on those pesky birds and get your revenge.

Features:
- Physics-based gameplay with realistic collisions
- Slingshot mechanics
- Destructible blocks and birds
- Particle effects for explosions

### 2. Questioning Bird
An existential game featuring a philosophical bird that questions its existence while shooting at pigs.

Features:
- Autonomous bird that targets pigs
- Philosophical dialog system with player choices
- Dynamic thought bubbles showing the bird's inner monologue
- Special "angry" state when the bird rebels against the player
- Procedurally generated sound effects and background music

## Project Structure
```
.
├── main.py              # Main game launcher
├── requirements.txt     # Python dependencies
├── games/              # Games directory
│   ├── __init__.py
│   ├── revenge_of_pigs/ # Revenge of the Pigs game
│   │   ├── __init__.py
│   │   ├── assets/     # Game assets
│   │   └── revenge_of_pigs.py
│   └── Questioning_bird/ # Questioning Bird game
│       ├── __init__.py
│       ├── assets/     # Game assets
│       ├── src/        # Game source code
│       └── run_game.py
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
- SciPy (for sound generation)

## The Power of AI-Assisted Development

This project serves as a demonstration of how AI tools like Cursor can transform the software development process. By leveraging natural language prompting, even those with limited programming experience can create complex, functional applications.

All games in this collection were conceptualized, designed, and implemented through conversation with the Cursor AI agent, highlighting the potential of AI as a collaborative tool in creative coding projects. 