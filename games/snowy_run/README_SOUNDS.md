# Snowy Run Sound Generator

This directory contains a sound generator script that creates all the necessary sound files for the Snowy Run game.

## Sound Files

The game uses the following sound files:

- `fart.wav` - Sound effect when the pig farts mid-air
- `jump.wav` - Sound effect when the pig jumps
- `sledge.wav` - Continuous sound of the sledge sliding on snow
- `collision.wav` - Sound effect when colliding with a bird

## How to Use

### Generating Sound Files

Run the following command from the project root directory:

```
python games/snowy_run/generate_sounds.py
```

This will generate all missing sound files in the `games/snowy_run/assets/sounds` directory.

### Regenerating All Sound Files

If you want to force regeneration of all sound files (even if they already exist), use the `--force` parameter:

```
python games/snowy_run/generate_sounds.py --force
```

## Technical Details

The sounds are generated procedurally using sine waves and noise patterns:

- The fart sound uses a decreasing frequency with random variations
- The jump sound uses an increasing frequency with a quick fade-out
- The sledge sound uses filtered white noise with a rhythmic pattern
- The collision sound uses a quick attack and decay with some noise

All sounds are generated as mono 16-bit PCM WAV files with a sample rate of 22050 Hz.

## Customizing Sounds

If you want to customize the sounds:

1. Edit the corresponding generation function in `generate_sounds.py`
2. Run the script with the `--force` parameter to regenerate all sounds

Alternatively, you can replace the WAV files directly with your own custom sounds, as long as they have the same filenames. 