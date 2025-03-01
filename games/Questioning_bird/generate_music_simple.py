import os
import numpy as np
from scipy.io import wavfile
import pygame
import sys
import random

# Add parent directory to path for direct execution
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Initialize pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=2)

# Create assets directory if it doesn't exist
assets_dir = os.path.join(current_dir, "assets")
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)

def generate_simple_tone(frequency, duration, sample_rate=44100, volume=0.5):
    """Generate a simple tone with fade in/out"""
    # Generate time array
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate the base tone
    tone = np.sin(2 * np.pi * frequency * t)
    
    # Add some harmonics for richness
    tone += 0.3 * np.sin(2 * np.pi * frequency * 2 * t)  # First harmonic (octave)
    tone += 0.15 * np.sin(2 * np.pi * frequency * 3 * t)  # Second harmonic
    
    # Create simple fade in/out
    fade_samples = int(0.1 * sample_rate)  # 100ms fade
    
    # Apply fade in
    if fade_samples > 0:
        tone[:fade_samples] *= np.linspace(0, 1, fade_samples)
    
    # Apply fade out
    if fade_samples > 0:
        tone[-fade_samples:] *= np.linspace(1, 0, fade_samples)
    
    # Apply volume
    tone = tone * volume
    
    return tone

def generate_chord(frequencies, duration, sample_rate=44100, volume=0.4):
    """Generate a chord from a list of frequencies"""
    # Create an empty array for the chord
    chord = np.zeros(int(sample_rate * duration))
    
    # Add each frequency component
    for i, freq in enumerate(frequencies):
        # Adjust volume for each note (root is loudest)
        note_volume = volume * (1.0 - (i * 0.15))
        
        # Generate the tone
        tone = generate_simple_tone(freq, duration, sample_rate, note_volume)
        
        # Add to the chord
        chord += tone
    
    # Normalize
    max_val = np.max(np.abs(chord))
    if max_val > 0:
        chord = chord / max_val * volume
    
    return chord

def generate_philosophical_music(duration=60, output_file="background_music.wav"):
    """Generate simplified philosophical ambient music"""
    print("Generating simplified philosophical background music...")
    sample_rate = 44100
    
    # Create an empty array for the full track
    full_track = np.zeros(int(sample_rate * duration))
    
    # Define a philosophical chord progression
    # A minor scale: A, B, C, D, E, F, G
    a_minor_frequencies = {
        "A3": 220.00,  # A3
        "C4": 261.63,  # C4
        "E4": 329.63,  # E4
        "G4": 392.00,  # G4
    }
    
    # Define chord progressions
    chord_progressions = [
        # Am chord (A, C, E)
        [a_minor_frequencies["A3"], a_minor_frequencies["C4"], a_minor_frequencies["E4"]],
        # F major chord (F, A, C)
        [349.23, 440.00, 523.25],
        # C major chord (C, E, G)
        [a_minor_frequencies["C4"], a_minor_frequencies["E4"], a_minor_frequencies["G4"]],
        # G major chord (G, B, D)
        [392.00, 493.88, 587.33],
        # Em chord (E, G, B)
        [a_minor_frequencies["E4"], a_minor_frequencies["G4"], 493.88],
    ]
    
    # Generate the music by layering chords
    chord_duration = 5.0  # 5 seconds per chord
    current_time = 0
    
    while current_time < duration:
        # Choose a random chord from the progression
        chord_freqs = random.choice(chord_progressions)
        
        # Generate the chord
        chord_audio = generate_chord(chord_freqs, chord_duration, volume=0.3)
        
        # Calculate start position
        start_sample = int(current_time * sample_rate)
        end_sample = min(start_sample + len(chord_audio), len(full_track))
        
        # Add to the full track
        if end_sample > start_sample:
            full_track[start_sample:end_sample] += chord_audio[:end_sample-start_sample]
        
        # Move time forward
        current_time += chord_duration - 1.0  # Overlap chords by 1 second
    
    # Add some gentle random melody notes
    melody_notes = [a_minor_frequencies["A3"], a_minor_frequencies["C4"], 
                   a_minor_frequencies["E4"], a_minor_frequencies["G4"]]
    
    for _ in range(20):  # Add 20 random notes
        # Choose a random time
        note_time = random.uniform(0, duration - 2.0)
        
        # Choose a random note
        note_freq = random.choice(melody_notes)
        
        # Random duration between 1 and 2 seconds
        note_duration = random.uniform(1.0, 2.0)
        
        # Generate the note
        note_audio = generate_simple_tone(note_freq, note_duration, volume=0.15)
        
        # Calculate start position
        start_sample = int(note_time * sample_rate)
        end_sample = min(start_sample + len(note_audio), len(full_track))
        
        # Add to the full track
        if end_sample > start_sample:
            full_track[start_sample:end_sample] += note_audio[:end_sample-start_sample]
    
    # Normalize the final track
    max_val = np.max(np.abs(full_track))
    if max_val > 0:
        full_track = full_track / max_val * 0.9
    
    # Convert to stereo
    stereo_track = np.column_stack((full_track, full_track))
    
    # Convert to 16-bit PCM
    audio_16bit = np.int16(stereo_track * 32767)
    
    # Save the file
    output_path = os.path.join(assets_dir, output_file)
    wavfile.write(output_path, sample_rate, audio_16bit)
    print(f"Saved philosophical music to {output_path}")
    
    return output_path

def main():
    """Generate background music"""
    print("Generating simplified background music for Questioning Bird...")
    
    # Check if scipy is installed
    try:
        import scipy
    except ImportError:
        print("Error: scipy is required to generate music.")
        print("Please install it with: pip install scipy")
        return
    
    # Generate the music
    output_path = generate_philosophical_music()
    
    # Play a preview
    try:
        sound = pygame.mixer.Sound(output_path)
        sound.play()
        print("Playing preview... (press Ctrl+C to stop)")
        pygame.time.wait(5000)  # Play for 5 seconds
        pygame.mixer.stop()
    except Exception as e:
        print(f"Error playing preview: {e}")
    
    print("Background music generated successfully!")

if __name__ == "__main__":
    main() 