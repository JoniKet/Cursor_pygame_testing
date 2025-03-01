"""
Test script for Snowy Run game
Helps to debug issues by testing individual components
"""
import pygame
import sys
import os

# Add the project root to the path
current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from games.snowy_run.main import Player, Bird, Terrain, SCREEN_WIDTH, SCREEN_HEIGHT

def test_terrain_generation():
    """Test that terrain generation works properly"""
    pygame.init()
    print("Testing terrain generation...")
    terrain = Terrain(5000)
    print(f"Successfully created terrain with {len(terrain.segments)} segments")
    
    # Test height calculation
    test_positions = [0, 100, 1000, 2000, 4000]
    for pos in test_positions:
        height = terrain.get_height(pos)
        print(f"Terrain height at position {pos}: {height}")
    
    print("Terrain generation test complete\n")

def test_player_physics():
    """Test player physics"""
    pygame.init()
    print("Testing player physics...")
    
    # Create player and terrain
    player = Player(200, SCREEN_HEIGHT - 300)
    terrain = Terrain(5000)
    
    # Test jumping
    print("Testing jumping:")
    print(f"Initial position: ({player.x}, {player.y}), on_ground: {player.on_ground}")
    player.update(terrain)  # Should set on_ground to True
    print(f"After update: ({player.x}, {player.y}), on_ground: {player.on_ground}")
    
    player.jump()
    print(f"After jump: velocity_y = {player.velocity_y}, on_ground: {player.on_ground}")
    
    # Update a few frames to see gravity
    for i in range(5):
        player.update(terrain)
        print(f"Frame {i+1}: position = ({player.x}, {player.y}), velocity_y = {player.velocity_y}")
    
    print("Player physics test complete\n")

def test_bird_collision():
    """Test bird collision detection"""
    pygame.init()
    print("Testing bird collision detection...")
    
    player = Player(200, 200)
    
    # Test cases: bird at different positions relative to player
    test_cases = [
        # Direct hit
        {"bird_pos": (200, 200), "expected": True},
        # Near miss
        {"bird_pos": (300, 300), "expected": False},
        # Edge collision
        {"bird_pos": (240, 200), "expected": True},
    ]
    
    for i, test in enumerate(test_cases):
        bird = Bird(*test["bird_pos"])
        collision = bird.check_collision(player)
        result = "PASS" if collision == test["expected"] else "FAIL"
        print(f"Test {i+1}: Bird at {test['bird_pos']}, expected {test['expected']}, got {collision} - {result}")
    
    print("Collision detection test complete\n")

def run_tests():
    """Run all tests"""
    print("===== SNOWY RUN TESTS =====")
    test_terrain_generation()
    test_player_physics()
    test_bird_collision()
    print("All tests completed")

if __name__ == "__main__":
    run_tests() 