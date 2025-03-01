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

def generate_note(frequency, duration, sample_rate=44100, volume=0.5, attack=0.1, decay=0.2, sustain=0.6, release=0.3):
    """Generate a single note with ADSR envelope"""
    # Generate time array
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate the base tone
    tone = np.sin(2 * np.pi * frequency * t)
    
    # Add some harmonics for richness
    tone += 0.3 * np.sin(2 * np.pi * frequency * 2 * t)  # First harmonic (octave)
    tone += 0.15 * np.sin(2 * np.pi * frequency * 3 * t)  # Second harmonic
    tone += 0.05 * np.sin(2 * np.pi * frequency * 4 * t)  # Third harmonic
    
    # Normalize
    tone = tone / np.max(np.abs(tone))
    
    # Create ADSR envelope
    attack_samples = int(attack * sample_rate)
    decay_samples = int(decay * sample_rate)
    sustain_samples = int(sustain * sample_rate)
    release_samples = int(release * sample_rate)
    
    # Ensure we don't exceed the total duration
    total_samples = len(tone)
    if attack_samples + decay_samples + sustain_samples + release_samples > total_samples:
        # Scale down proportionally
        scale = total_samples / (attack_samples + decay_samples + sustain_samples + release_samples)
        attack_samples = int(attack_samples * scale)
        decay_samples = int(decay_samples * scale)
        sustain_samples = int(sustain_samples * scale)
        release_samples = int(release_samples * scale)
    
    # Create envelope segments
    envelope = np.zeros_like(tone)
    
    # Attack (linear ramp up)
    if attack_samples > 0:
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    
    # Decay (exponential decay to sustain level)
    if decay_samples > 0:
        decay_end = attack_samples + decay_samples
        decay_curve = np.exp(-3 * np.linspace(0, 1, decay_samples))
        decay_curve = 1 - (1 - 0.7) * decay_curve  # Decay from 1.0 to 0.7
        envelope[attack_samples:decay_end] = decay_curve
    
    # Sustain (constant)
    if sustain_samples > 0:
        sustain_end = attack_samples + decay_samples + sustain_samples
        envelope[attack_samples + decay_samples:sustain_end] = 0.7
    
    # Release (exponential decay to zero)
    if release_samples > 0:
        release_start = attack_samples + decay_samples + sustain_samples
        release_end = min(release_start + release_samples, total_samples)
        release_length = release_end - release_start
        if release_length > 0:
            release_curve = np.exp(-5 * np.linspace(0, 1, release_length))
            release_curve = 0.7 * release_curve  # Start from sustain level
            envelope[release_start:release_end] = release_curve
    
    # Apply envelope
    tone = tone * envelope * volume
    
    return tone

def generate_chord(base_freq, chord_type="minor", duration=2.0, volume=0.4):
    """Generate a chord based on the base frequency"""
    sample_rate = 44100
    
    # Define intervals for different chord types
    intervals = {
        "major": [1, 5/4, 3/2],  # Root, major third, perfect fifth
        "minor": [1, 6/5, 3/2],  # Root, minor third, perfect fifth
        "diminished": [1, 6/5, 7/5],  # Root, minor third, diminished fifth
        "augmented": [1, 5/4, 8/5],  # Root, major third, augmented fifth
        "sus4": [1, 4/3, 3/2],  # Root, perfect fourth, perfect fifth
        "sus2": [1, 9/8, 3/2],  # Root, major second, perfect fifth
        "seventh": [1, 5/4, 3/2, 7/4],  # Root, major third, perfect fifth, minor seventh
        "minor_seventh": [1, 6/5, 3/2, 7/4],  # Root, minor third, perfect fifth, minor seventh
    }
    
    # Get the intervals for the requested chord type
    chord_intervals = intervals.get(chord_type, intervals["minor"])
    
    # Generate each note in the chord
    chord = np.zeros(int(sample_rate * duration))
    
    for i, interval in enumerate(chord_intervals):
        # Adjust attack/decay/sustain/release for each note to create more texture
        attack = 0.1 + (i * 0.05)
        decay = 0.2 + (i * 0.03)
        sustain = 0.6 - (i * 0.05)
        release = 0.3 + (i * 0.1)
        
        # Adjust volume for each note (root is loudest)
        note_volume = volume * (1.0 - (i * 0.15))
        
        # Generate the note
        note = generate_note(
            base_freq * interval, 
            duration, 
            volume=note_volume,
            attack=attack,
            decay=decay,
            sustain=sustain,
            release=release
        )
        
        # Add to the chord
        chord += note
    
    # Normalize
    chord = chord / np.max(np.abs(chord)) * volume
    
    return chord

def generate_ambient_pad(base_freq, duration=5.0, volume=0.3):
    """Generate an ambient pad sound"""
    sample_rate = 44100
    
    # Create a longer attack and release for a pad-like sound
    pad = generate_note(
        base_freq, 
        duration, 
        volume=volume,
        attack=duration * 0.3,
        decay=duration * 0.1,
        sustain=duration * 0.4,
        release=duration * 0.2
    )
    
    # Add some subtle modulation
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    lfo = np.sin(2 * np.pi * 0.5 * t)  # 0.5 Hz LFO
    
    # Apply subtle pitch modulation
    modulated_pad = np.zeros_like(pad)
    for i in range(len(t)):
        # Get a small segment around the current time
        segment_start = max(0, i - 100)
        segment_end = min(len(t), i + 100)
        
        # Apply a slight time shift based on the LFO
        shift = int(lfo[i] * 5)  # Small time shift
        
        # Ensure we stay within bounds
        source_idx = i + shift
        if 0 <= source_idx < len(pad):
            modulated_pad[i] = pad[source_idx]
        else:
            modulated_pad[i] = pad[i]
    
    # Add a second detuned layer for richness
    detuned_pad = generate_note(
        base_freq * 1.003,  # Slightly detuned
        duration, 
        volume=volume * 0.7,
        attack=duration * 0.25,
        decay=duration * 0.15,
        sustain=duration * 0.35,
        release=duration * 0.25
    )
    
    # Combine the layers
    combined_pad = (modulated_pad + detuned_pad) / 2
    
    # Apply a gentle filter (simple moving average as lowpass)
    window_size = 100
    filtered_pad = np.convolve(combined_pad, np.ones(window_size)/window_size, mode='same')
    
    return filtered_pad

def generate_philosophical_music(duration=120, output_file="background_music.wav"):
    """Generate philosophical ambient music"""
    print("Generating philosophical background music...")
    sample_rate = 44100
    
    # Create an empty array for the full track
    full_track = np.zeros(int(sample_rate * duration))
    
    # Define a philosophical chord progression
    # Using frequencies rather than notes for more control
    # A minor scale: A, B, C, D, E, F, G
    a_minor_frequencies = {
        "A3": 220.00,  # A3
        "B3": 246.94,  # B3
        "C4": 261.63,  # C4
        "D4": 293.66,  # D4
        "E4": 329.63,  # E4
        "F4": 349.23,  # F4
        "G4": 392.00,  # G4
        "A4": 440.00,  # A4
    }
    
    # Define a philosophical chord progression
    # Am - F - C - G - Em - Am - Dm - E
    progression = [
        {"root": "A3", "type": "minor", "duration": 8.0},
        {"root": "F4", "type": "major", "duration": 8.0},
        {"root": "C4", "type": "major", "duration": 8.0},
        {"root": "G4", "type": "major", "duration": 8.0},
        {"root": "E4", "type": "minor", "duration": 8.0},
        {"root": "A3", "type": "minor", "duration": 8.0},
        {"root": "D4", "type": "minor", "duration": 8.0},
        {"root": "E4", "type": "major", "duration": 8.0},
    ]
    
    # Generate ambient pads for the background
    pad_notes = ["A3", "E4", "A4"]
    pad_duration = 30.0  # Longer pads that overlap
    
    current_time = 0
    while current_time < duration:
        for pad_note in pad_notes:
            # Skip some pads randomly for variation
            if random.random() < 0.3:
                continue
                
            # Generate pad
            pad_freq = a_minor_frequencies[pad_note]
            pad = generate_ambient_pad(pad_freq, pad_duration, volume=0.15)
            
            # Calculate pad start position
            pad_start = int(current_time * sample_rate)
            pad_end = min(pad_start + len(pad), len(full_track))
            
            # Add pad to the track
            if pad_end > pad_start:
                full_track[pad_start:pad_end] += pad[:pad_end-pad_start]
            
            # Increment time slightly for overlapping pads
            current_time += 10.0
            
            # Reset if we've gone too far
            if current_time >= duration - pad_duration:
                current_time = 0
                break
    
    # Generate the chord progression
    current_time = 0
    while current_time < duration:
        for chord in progression:
            # Generate the chord
            root_freq = a_minor_frequencies[chord["root"]]
            chord_type = chord["type"]
            chord_duration = chord["duration"]
            
            # Generate the chord audio
            chord_audio = generate_chord(root_freq, chord_type, chord_duration, volume=0.25)
            
            # Calculate start position
            start_sample = int(current_time * sample_rate)
            end_sample = min(start_sample + len(chord_audio), len(full_track))
            
            # Add to the full track
            if end_sample > start_sample:
                full_track[start_sample:end_sample] += chord_audio[:end_sample-start_sample]
            
            # Move time forward
            current_time += chord_duration
            
            # Break if we've filled the duration
            if current_time >= duration:
                break
    
    # Add some gentle random melody notes
    melody_notes = ["A4", "C4", "E4", "G4", "A3", "D4"]
    current_time = 5.0  # Start after a short delay
    
    while current_time < duration - 2.0:
        # Randomly decide whether to play a note
        if random.random() < 0.4:  # 40% chance to play a note
            # Choose a random note
            note_name = random.choice(melody_notes)
            note_freq = a_minor_frequencies[note_name]
            
            # Random duration between 1 and 3 seconds
            note_duration = random.uniform(1.0, 3.0)
            
            # Generate the note with a softer attack and longer release
            note_audio = generate_note(
                note_freq, 
                note_duration, 
                volume=0.15,
                attack=0.2,
                decay=0.3,
                sustain=0.3,
                release=0.5
            )
            
            # Calculate start position
            start_sample = int(current_time * sample_rate)
            end_sample = min(start_sample + len(note_audio), len(full_track))
            
            # Add to the full track
            if end_sample > start_sample:
                full_track[start_sample:end_sample] += note_audio[:end_sample-start_sample]
        
        # Move time forward by a random amount (0.5 to 2.5 seconds)
        current_time += random.uniform(0.5, 2.5)
    
    # Normalize the final track
    full_track = full_track / np.max(np.abs(full_track)) * 0.9
    
    # Convert to stereo
    stereo_track = np.column_stack((full_track, full_track))
    
    # Convert to 16-bit PCM
    audio_16bit = np.int16(stereo_track * 32767)
    
    # Save the file
    output_path = os.path.join(assets_dir, output_file)
    wavfile.write(output_path, sample_rate, audio_16bit)
    print(f"Saved philosophical music to {output_path}")
    
    # Play a preview
    try:
        sound = pygame.mixer.Sound(output_path)
        sound.play()
        print("Playing preview... (press Ctrl+C to stop)")
        pygame.time.wait(10000)  # Play for 10 seconds
        pygame.mixer.stop()
    except Exception as e:
        print(f"Error playing preview: {e}")

def main():
    """Generate background music"""
    print("Generating background music for Questioning Bird...")
    
    # Check if scipy is installed
    try:
        import scipy
    except ImportError:
        print("Error: scipy is required to generate music.")
        print("Please install it with: pip install scipy")
        return
    
    # Generate the music
    generate_philosophical_music()
    
    print("Background music generated successfully!")

if __name__ == "__main__":
    main() 