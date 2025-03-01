import os
import pygame
import numpy as np
from scipy.io import wavfile
import sys

# Add parent directory to path for direct execution
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Initialize pygame mixer
pygame.mixer.init()

# Create assets directory if it doesn't exist
assets_dir = os.path.join(current_dir, "assets")
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)

def generate_shoot_sound():
    """Generate a laser-like shoot sound"""
    print("Generating shoot sound...")
    sample_rate = 44100
    duration = 0.3  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a frequency sweep (from high to low)
    f_start = 1000
    f_end = 300
    frequency = np.linspace(f_start, f_end, len(t))
    
    # Generate the tone
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    
    # Apply an envelope to avoid clicks
    envelope = np.exp(-5 * t)
    tone = tone * envelope
    
    # Convert to 16-bit PCM
    audio = np.int16(tone * 32767)
    
    # Save the file
    output_path = os.path.join(assets_dir, "shoot.wav")
    wavfile.write(output_path, sample_rate, audio)
    print(f"Saved shoot sound to {output_path}")
    
    # Play the sound
    sound = pygame.mixer.Sound(output_path)
    sound.play()
    pygame.time.wait(int(duration * 1000))

def generate_explosion_sound():
    """Generate an explosion sound"""
    print("Generating explosion sound...")
    sample_rate = 44100
    duration = 0.5  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create noise
    noise = np.random.normal(0, 1, len(t))
    
    # Apply a lowpass filter (simple moving average)
    window_size = 50
    noise_filtered = np.convolve(noise, np.ones(window_size)/window_size, mode='same')
    
    # Apply an envelope for the explosion shape
    envelope = np.exp(-8 * t)
    audio = noise_filtered * envelope
    
    # Normalize and convert to 16-bit PCM
    audio = audio / np.max(np.abs(audio))
    audio = np.int16(audio * 32767 * 0.8)
    
    # Save the file
    output_path = os.path.join(assets_dir, "explosion.wav")
    wavfile.write(output_path, sample_rate, audio)
    print(f"Saved explosion sound to {output_path}")
    
    # Play the sound
    sound = pygame.mixer.Sound(output_path)
    sound.play()
    pygame.time.wait(int(duration * 1000))

def generate_game_over_sound():
    """Generate a game over sound"""
    print("Generating game over sound...")
    sample_rate = 44100
    duration = 1.0  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a descending tone
    f_start = 400
    f_end = 100
    frequency = np.linspace(f_start, f_end, len(t))
    
    # Generate the tone with some harmonics
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    tone += 0.3 * np.sin(2 * np.pi * frequency * 2 * t)  # Add first harmonic
    
    # Apply an envelope
    envelope = 1 - np.exp(-0.5 * t)  # Attack
    envelope = envelope * np.exp(-2 * (t - 0.2))  # Decay
    tone = tone * envelope
    
    # Convert to 16-bit PCM
    audio = np.int16(tone * 32767 * 0.8)
    
    # Save the file
    output_path = os.path.join(assets_dir, "game_over.wav")
    wavfile.write(output_path, sample_rate, audio)
    print(f"Saved game over sound to {output_path}")
    
    # Play the sound
    sound = pygame.mixer.Sound(output_path)
    sound.play()
    pygame.time.wait(int(duration * 1000))

def generate_menu_select_sound():
    """Generate a menu selection sound"""
    print("Generating menu select sound...")
    sample_rate = 44100
    duration = 0.15  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create an ascending tone
    f_start = 300
    f_end = 600
    frequency = np.linspace(f_start, f_end, len(t))
    
    # Generate the tone
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    
    # Apply an envelope
    envelope = np.exp(-10 * (t - duration/2)**2)
    tone = tone * envelope
    
    # Convert to 16-bit PCM
    audio = np.int16(tone * 32767 * 0.8)
    
    # Save the file
    output_path = os.path.join(assets_dir, "menu_select.wav")
    wavfile.write(output_path, sample_rate, audio)
    print(f"Saved menu select sound to {output_path}")
    
    # Play the sound
    sound = pygame.mixer.Sound(output_path)
    sound.play()
    pygame.time.wait(int(duration * 1000))

def generate_angry_sound():
    """Generate an angry bird sound"""
    print("Generating angry bird sound...")
    sample_rate = 44100
    duration = 0.8  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a growling sound with frequency modulation
    carrier_freq = 200
    mod_freq = 20
    mod_index = 5
    
    # Generate the modulated tone
    modulator = np.sin(2 * np.pi * mod_freq * t)
    carrier = np.sin(2 * np.pi * (carrier_freq + mod_index * modulator) * t)
    
    # Add some noise for texture
    noise = np.random.normal(0, 0.3, len(t))
    
    # Combine signals
    signal = 0.7 * carrier + 0.3 * noise
    
    # Apply an envelope
    envelope = np.exp(-3 * (t - 0.2)**2)
    signal = signal * envelope
    
    # Convert to 16-bit PCM
    audio = np.int16(signal * 32767 * 0.8)
    
    # Save the file
    output_path = os.path.join(assets_dir, "angry.wav")
    wavfile.write(output_path, sample_rate, audio)
    print(f"Saved angry bird sound to {output_path}")
    
    # Play the sound
    sound = pygame.mixer.Sound(output_path)
    sound.play()
    pygame.time.wait(int(duration * 1000))

def generate_question_sound():
    """Generate a questioning sound"""
    print("Generating question sound...")
    sample_rate = 44100
    duration = 0.4  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create an ascending tone (question-like)
    f_start = 300
    f_mid = 400
    f_end = 500
    
    # First half ascending
    t1 = t[:len(t)//2]
    f1 = np.linspace(f_start, f_mid, len(t1))
    
    # Second half ascending more (question mark)
    t2 = t[len(t)//2:]
    f2 = np.linspace(f_mid, f_end, len(t2))
    
    # Combine frequencies
    frequency = np.concatenate((f1, f2))
    
    # Generate the tone
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    
    # Apply an envelope
    envelope = np.exp(-5 * (t - duration/2)**2)
    tone = tone * envelope
    
    # Convert to 16-bit PCM
    audio = np.int16(tone * 32767 * 0.8)
    
    # Save the file
    output_path = os.path.join(assets_dir, "question.wav")
    wavfile.write(output_path, sample_rate, audio)
    print(f"Saved question sound to {output_path}")
    
    # Play the sound
    sound = pygame.mixer.Sound(output_path)
    sound.play()
    pygame.time.wait(int(duration * 1000))

def main():
    """Generate all sound effects"""
    print("Generating sound effects for Questioning Bird...")
    
    # Check if scipy is installed
    try:
        import scipy
    except ImportError:
        print("Error: scipy is required to generate sounds.")
        print("Please install it with: pip install scipy")
        return
    
    # Generate all sounds
    generate_shoot_sound()
    generate_explosion_sound()
    generate_game_over_sound()
    generate_menu_select_sound()
    generate_angry_sound()
    generate_question_sound()
    
    print("All sound effects generated successfully!")

if __name__ == "__main__":
    main() 