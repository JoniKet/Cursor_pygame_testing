import pygame
import numpy as np
import wave
import os
import random

# Initialize pygame mixer (needed for Sound objects)
pygame.mixer.init()

# Define the sounds directory
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')

# Ensure the sounds directory exists
os.makedirs(SOUNDS_DIR, exist_ok=True)

def ensure_directory_exists(directory):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def save_sound_to_file(audio_data, filename):
    """Save audio data to a WAV file"""
    try:
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(44100)  # 44.1 kHz
            wf.writeframes(audio_data.tobytes())
        print(f"Created sound file: {filename}")
    except Exception as e:
        print(f"Error saving sound file {filename}: {e}")

def generate_fart_sound(filename):
    """Generate a fart sound effect"""
    duration = 0.7  # seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a bubbling/rumbling sound
    base_freq = 80
    
    # Add some randomness to the frequency
    freq_mod = 30 * np.sin(2 * np.pi * 8 * t) + 10 * np.random.randn(len(t))
    freq = base_freq + freq_mod
    
    # Create the base tone
    audio = 0.4 * np.sin(2 * np.pi * np.cumsum(freq) / sample_rate)
    
    # Add noise bursts
    noise = 0.3 * np.random.uniform(-1, 1, len(t))
    
    # Add some random bubbling effects
    for i in range(8):
        pos = int(random.uniform(0.1, 0.9) * len(t))
        width = int(0.02 * sample_rate)
        if pos + width < len(noise):
            noise[pos:pos+width] *= 3.0
    
    # Mix the signals
    audio = audio + noise
    
    # Apply an envelope
    envelope = np.ones_like(t)
    envelope[t > 0.6 * duration] = np.exp(-10 * (t[t > 0.6 * duration] - 0.6 * duration))
    audio = audio * envelope
    
    # Convert to 16-bit data
    audio = audio * 32767 / np.max(np.abs(audio))
    audio = audio.astype(np.int16)
    
    save_sound_to_file(audio, filename)

def generate_jump_sound(filename):
    """Generate a jump sound effect"""
    duration = 0.4  # seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create an upward sweep
    freq = np.linspace(200, 600, len(t))
    note = 0.5 * np.sin(2 * np.pi * freq * t)
    
    # Apply an envelope
    envelope = np.exp(-10 * t)
    audio = note * envelope
    
    # Convert to 16-bit data
    audio = audio * 32767 / np.max(np.abs(audio))
    audio = audio.astype(np.int16)
    
    save_sound_to_file(audio, filename)

def generate_sledge_sound(filename):
    """Generate a sledge sliding sound effect"""
    duration = 1.0  # seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a rushing/sliding sound
    noise = 0.3 * np.random.uniform(-1, 1, len(t))
    
    # Add some rhythmic pattern to simulate sliding over snow
    pattern = 0.2 * np.sin(2 * np.pi * 20 * t)
    
    # Mix the signals
    audio = noise * (1 + pattern)
    
    # Apply a filter to make it sound more like sliding
    # (Simple low-pass filter simulation)
    for i in range(1, len(audio)):
        audio[i] = 0.7 * audio[i] + 0.3 * audio[i-1]
    
    # Apply an envelope
    envelope = np.ones_like(t)
    envelope[t > 0.8 * duration] = np.exp(-10 * (t[t > 0.8 * duration] - 0.8 * duration))
    audio = audio * envelope
    
    # Convert to 16-bit data
    audio = audio * 32767 / np.max(np.abs(audio))
    audio = audio.astype(np.int16)
    
    save_sound_to_file(audio, filename)

def generate_collision_sound(filename):
    """Generate a collision sound effect"""
    duration = 0.5  # seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a crash sound
    noise = 0.7 * np.random.uniform(-1, 1, len(t))
    
    # Add some metallic ringing
    ring = 0.3 * np.sin(2 * np.pi * 800 * t) * np.exp(-12 * t)
    
    # Mix the signals
    audio = noise + ring
    
    # Apply an envelope
    envelope = np.exp(-15 * t)
    audio = audio * envelope
    
    # Convert to 16-bit data
    audio = audio * 32767 / np.max(np.abs(audio))
    audio = audio.astype(np.int16)
    
    save_sound_to_file(audio, filename)

def main():
    """Generate all sound files for the Snowy Run game"""
    # Initialize pygame mixer (not strictly necessary for generation but good for testing)
    pygame.mixer.init()
    
    # Set up paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(script_dir, "assets")
    sounds_dir = os.path.join(assets_dir, "sounds")
    
    # Create directories if they don't exist
    ensure_directory_exists(assets_dir)
    ensure_directory_exists(sounds_dir)
    
    # Generate all sound files
    generate_fart_sound(os.path.join(sounds_dir, "fart.wav"))
    generate_jump_sound(os.path.join(sounds_dir, "jump.wav"))
    generate_sledge_sound(os.path.join(sounds_dir, "sledge.wav"))
    generate_collision_sound(os.path.join(sounds_dir, "collision.wav"))
    
    print("All sound files generated successfully!")
    
    # Test playing the sounds
    try:
        print("Testing sounds...")
        for sound_file in ["fart.wav", "jump.wav", "sledge.wav", "collision.wav"]:
            full_path = os.path.join(sounds_dir, sound_file)
            if os.path.exists(full_path):
                sound = pygame.mixer.Sound(full_path)
                sound.play()
                pygame.time.wait(int(sound.get_length() * 1000) + 100)  # Wait for sound to finish
                print(f"Played: {sound_file}")
    except Exception as e:
        print(f"Error testing sounds: {e}")
    
    print("Sound generation complete!")

if __name__ == "__main__":
    main() 