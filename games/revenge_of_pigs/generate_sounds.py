import os
import numpy as np
import wave
import random
import pygame

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

def generate_launch_sound(filename):
    """Generate a launch sound effect"""
    duration = 0.5  # seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a descending frequency sweep
    freq = np.linspace(800, 200, len(t))
    note = 0.5 * np.sin(2 * np.pi * freq * t)
    
    # Apply an envelope
    envelope = np.exp(-5 * t)
    audio = note * envelope
    
    # Convert to 16-bit data
    audio = audio * 32767 / np.max(np.abs(audio))
    audio = audio.astype(np.int16)
    
    save_sound_to_file(audio, filename)

def generate_collision_sound(filename):
    """Generate a collision sound effect"""
    duration = 0.3  # seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a noise burst with some tonal components
    noise = np.random.uniform(-0.5, 0.5, len(t))
    tone = 0.5 * np.sin(2 * np.pi * 300 * t)
    
    # Mix and apply an envelope
    audio = noise + tone
    envelope = np.exp(-15 * t)
    audio = audio * envelope
    
    # Convert to 16-bit data
    audio = audio * 32767 / np.max(np.abs(audio))
    audio = audio.astype(np.int16)
    
    save_sound_to_file(audio, filename)

def generate_wood_break_sound(filename):
    """Generate a wood breaking sound effect"""
    duration = 0.4  # seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a cracking sound with noise bursts
    noise = np.random.uniform(-0.7, 0.7, len(t))
    
    # Add some cracking transients
    for i in range(5):
        pos = int(random.uniform(0.1, 0.8) * len(t))
        width = int(0.01 * sample_rate)
        if pos + width < len(noise):
            noise[pos:pos+width] *= 2.0
    
    # Apply an envelope
    envelope = np.exp(-8 * t)
    audio = noise * envelope
    
    # Convert to 16-bit data
    audio = audio * 32767 / np.max(np.abs(audio))
    audio = audio.astype(np.int16)
    
    save_sound_to_file(audio, filename)

def generate_victory_sound(filename):
    """Generate a victory sound effect"""
    duration = 1.5  # seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a triumphant ascending arpeggio
    freqs = [261.63, 329.63, 392.0, 523.25]  # C4, E4, G4, C5
    audio = np.zeros_like(t)
    
    for i, freq in enumerate(freqs):
        start = i * duration / 5
        end = start + duration / 4
        idx = np.logical_and(t >= start, t < end)
        audio[idx] += 0.5 * np.sin(2 * np.pi * freq * (t[idx] - start))
    
    # Add a final chord
    idx = t >= 4 * duration / 5
    for freq in freqs:
        audio[idx] += 0.25 * np.sin(2 * np.pi * freq * (t[idx] - 4 * duration / 5))
    
    # Apply an envelope
    envelope = np.ones_like(t)
    envelope[t > 0.8 * duration] = np.exp(-3 * (t[t > 0.8 * duration] - 0.8 * duration))
    audio = audio * envelope
    
    # Convert to 16-bit data
    audio = audio * 32767 / np.max(np.abs(audio))
    audio = audio.astype(np.int16)
    
    save_sound_to_file(audio, filename)

def generate_slingshot_stretch_sound(filename):
    """Generate a slingshot stretching sound effect"""
    duration = 0.3  # seconds
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a stretching rubber sound
    freq = 150 + 50 * np.sin(2 * np.pi * 8 * t)
    audio = 0.3 * np.sin(2 * np.pi * freq * t)
    
    # Add some noise
    noise = 0.1 * np.random.uniform(-1, 1, len(t))
    audio += noise
    
    # Apply an envelope
    envelope = np.ones_like(t)
    audio = audio * envelope
    
    # Convert to 16-bit data
    audio = audio * 32767 / np.max(np.abs(audio))
    audio = audio.astype(np.int16)
    
    save_sound_to_file(audio, filename)

def main():
    """Generate all sound files for the Revenge of Pigs game"""
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
    generate_launch_sound(os.path.join(sounds_dir, "launch.wav"))
    generate_collision_sound(os.path.join(sounds_dir, "collision.wav"))
    generate_wood_break_sound(os.path.join(sounds_dir, "wood_break.wav"))
    generate_victory_sound(os.path.join(sounds_dir, "victory.wav"))
    generate_slingshot_stretch_sound(os.path.join(sounds_dir, "slingshot_stretch.wav"))
    
    print("All sound files generated successfully!")
    
    # Test playing the sounds
    try:
        print("Testing sounds...")
        for sound_file in ["launch.wav", "collision.wav", "wood_break.wav", "victory.wav", "slingshot_stretch.wav"]:
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