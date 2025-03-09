import os
import numpy as np
from scipy.io import wavfile

def generate_sine_wave(freq, duration, amplitude=0.5, sample_rate=44100):
    """Generate a sine wave with the given frequency and duration"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    return wave

def generate_noise(duration, amplitude=0.5, sample_rate=44100):
    """Generate white noise"""
    samples = int(sample_rate * duration)
    noise = amplitude * np.random.uniform(-1, 1, samples)
    return noise

def create_menu_select():
    """Create a menu selection sound"""
    duration = 0.1
    wave = generate_sine_wave(880, duration, 0.3)  # High-pitched beep
    wave *= np.linspace(1, 0, len(wave))**2  # Fade out
    return wave

def create_shoot():
    """Create a shooting sound"""
    duration = 0.2
    # Mix a sine wave with noise
    wave = generate_sine_wave(440, duration, 0.3)
    noise = generate_noise(duration, 0.2)
    combined = wave + noise
    # Apply envelope
    envelope = np.exp(-4 * np.linspace(0, 1, len(combined)))
    return combined * envelope

def create_explosion():
    """Create an explosion sound"""
    duration = 0.5
    # Start with noise
    wave = generate_noise(duration, 0.8)
    # Apply lowpass filter (simple moving average)
    window_size = 50
    wave = np.convolve(wave, np.ones(window_size)/window_size, mode='same')
    # Apply envelope
    envelope = np.exp(-6 * np.linspace(0, 1, len(wave)))
    return wave * envelope

def create_pig_talk():
    """Create a 'bla bla' sound for the general pig"""
    duration = 0.3
    # Create a modulated sine wave
    t = np.linspace(0, duration, int(44100 * duration))
    # Modulate frequency between 300 and 400 Hz
    freq = 300 + 100 * np.sin(2 * np.pi * 8 * t)
    wave = 0.5 * np.sin(2 * np.pi * freq * t)
    # Add some noise for a more "grunty" sound
    noise = generate_noise(duration, 0.2)
    combined = wave + noise
    # Apply envelope
    envelope = np.exp(-4 * np.linspace(0, 1, len(combined)))
    return combined * envelope

def save_wave(wave, filename, sample_rate=44100):
    """Save a wave array to a WAV file"""
    # Ensure the wave is in the valid range [-1, 1]
    wave = np.clip(wave, -1, 1)
    # Convert to 16-bit PCM
    wave_int = (wave * 32767).astype(np.int16)
    wavfile.write(filename, sample_rate, wave_int)

def main():
    """Generate all game sounds"""
    # Create assets/sounds directory if it doesn't exist
    sounds_dir = os.path.join('games', 'Pig_invaders', 'assets', 'sounds')
    os.makedirs(sounds_dir, exist_ok=True)
    
    # Generate and save sounds
    sounds = {
        'menu_select.wav': create_menu_select(),
        'shoot.wav': create_shoot(),
        'explosion.wav': create_explosion(),
        'pig_talk.wav': create_pig_talk()
    }
    
    for filename, wave in sounds.items():
        filepath = os.path.join(sounds_dir, filename)
        save_wave(wave, filepath)
        print(f"Generated {filepath}")

if __name__ == "__main__":
    main()
