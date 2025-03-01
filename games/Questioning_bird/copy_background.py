import os
import shutil
import sys

def copy_background():
    """
    Helper script to copy your AI-generated background to the correct location.
    
    Instructions:
    1. Place your AI-generated background image in the same directory as this script
    2. Make sure it's named 'background_ai.png'
    3. Run this script
    """
    # Get the current directory (where this script is located)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Source file path (where user placed the AI background)
    source_path = os.path.join(current_dir, "background_ai.png")
    
    # Destination directory (assets folder)
    assets_dir = os.path.join(current_dir, "assets")
    
    # Create assets directory if it doesn't exist
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        print(f"Created assets directory at {assets_dir}")
    
    # Destination file path
    dest_path = os.path.join(assets_dir, "background_ai.png")
    
    # Check if source file exists
    if not os.path.exists(source_path):
        print(f"Error: Could not find {source_path}")
        print("Please place your AI-generated background image in the same directory as this script")
        print("and make sure it's named 'background_ai.png'")
        return False
    
    # Copy the file
    try:
        shutil.copy2(source_path, dest_path)
        print(f"Successfully copied background_ai.png to {dest_path}")
        print("The game will now use this background when you run it!")
        return True
    except Exception as e:
        print(f"Error copying file: {e}")
        return False

if __name__ == "__main__":
    copy_background() 