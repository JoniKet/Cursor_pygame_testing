import pygame

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Game states
STATE_MENU = 0
STATE_PLAYING = 1
STATE_CREDITS = 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
DARK_BLUE = (30, 30, 60)
LIGHT_BLUE = (100, 100, 200)

# Font settings
FONT_NAME = None  # Uses Pygame's default font
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 36
FONT_SIZE_SMALL = 24

# Asset paths
ASSET_PATH = "games/Pig_invaders/assets"

# Credits text
CREDITS_TEXT = [
    "Pig Invaders",
    "Created by Claude AI",
    "",
    "Programming: Claude AI",
    "Design: Claude AI",
    "Graphics: Claude AI",
    "",
    "Made with Pygame",
    "",
    "Press ESC to return to menu"
]
