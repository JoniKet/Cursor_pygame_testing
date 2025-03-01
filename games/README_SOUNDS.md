# Sound Generation for Pygame Games

This document explains how to generate sound effects for the games in this project.

## Overview

Each game has its own sound generation script that creates WAV files for all the sound effects needed by the game. These scripts use `numpy` to procedurally generate sound waveforms and save them as WAV files in the appropriate directories.

## Requirements

To run the sound generation scripts, you need:

- Python 3.6 or higher
- NumPy
- PyGame
- Wave (standard library)

## Available Sound Generation Scripts

### Revenge of Pigs

The sound generation script for Revenge of Pigs creates the following sound effects:

- `launch.wav` - Sound when the pig is launched from the slingshot
- `collision.wav` - Sound when the pig collides with objects
- `wood_break.wav` - Sound when wooden blocks break
- `victory.wav` - Sound played on victory screen
- `slingshot_stretch.wav` - Sound when stretching the slingshot

To generate these sounds, run:

```
python -m games.revenge_of_pigs.generate_sounds
```

### Snowy Run

The sound generation script for Snowy Run creates the following sound effects:

- `fart.wav` - Sound when the pig farts for a speed boost
- `jump.wav` - Sound when the sledge jumps
- `sledge.wav` - Sound of the sledge sliding on snow
- `collision.wav` - Sound when colliding with birds

To generate these sounds, run:

```
python -m games.snowy_run.generate_sounds
```

## How It Works

Each sound generation script:

1. Creates the necessary directories if they don't exist
2. Generates each sound using mathematical functions and random noise
3. Saves the sounds as WAV files in the game's assets/sounds directory
4. Tests the sounds by playing them (if pygame is available)

## Customizing Sounds

If you want to customize the generated sounds, you can modify the parameters in the generation functions:

- Change frequencies to alter pitch
- Adjust durations to make sounds longer or shorter
- Modify envelopes to change how sounds fade in or out
- Add different noise patterns for more complex sounds

## Troubleshooting

If you encounter issues:

1. Make sure you have all required dependencies installed
2. Check that the assets directory is writable
3. Verify that pygame.mixer is initialized correctly
4. If sounds don't play during testing, check your system's audio settings

## Adding New Sounds

To add a new sound to a game:

1. Create a new generation function in the appropriate generate_sounds.py file
2. Add the sound to the main generation function
3. Update the game code to load and use the new sound 