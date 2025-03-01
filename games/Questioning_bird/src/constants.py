import pygame

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Game states
STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_CREDITS = 3

# Bird constants
BIRD_WIDTH = 50
BIRD_HEIGHT = 50

# Pig constants
PIG_WIDTH = 40
PIG_HEIGHT = 40

# Bullet constants
BULLET_WIDTH = 15
BULLET_HEIGHT = 15
BULLET_SPEED = 10

# Game entity limits
MAX_PIGS = 10
MAX_BULLETS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
SKY_BLUE = (135, 206, 235)
GROUND_GREEN = (34, 139, 34)
BIRD_COLOR = (255, 0, 0)  # Red
PIG_COLOR = (0, 153, 0)   # Green

# Entity dimensions
BIRD_RADIUS = 30
PIG_RADIUS = 25
BULLET_RADIUS = 8
ROTATION_SPEED = 1  # Degrees per frame
SHOOT_COOLDOWN = 30  # Frames between shots
PIG_MIN_SPEED = 0.5
PIG_MAX_SPEED = 2.0
EXPLOSION_DURATION = 30  # Frames

# Text
TITLE_TEXT = "Questioning Bird"
SUBTITLE_TEXT = "An Existential Crisis"
CREDITS_TEXT = [
    "Questioning Bird",
    "Created by Claude 3.7 Sonnet",
    "",
    "Programming: Claude AI",
    "Design: Claude AI",
    "Existential Questions: Claude AI",
    "",
    "Made with Pygame",
    "",
    "Press ESC to return to menu"
]

# Bird's existential thoughts
BIRD_THOUGHTS = [
    "Why am I shooting these pigs?",
    "What is my purpose?",
    "Is there more to life than this?",
    "Do the pigs feel pain?",
    "Am I the villain in this story?",
    "Why do they keep coming?",
    "What are they trying to tell me?",
    "Is this all there is?",
    "Why was I created like this?",
    "Will this ever end?",
    "If I stop shooting, would the pigs still attack?",
    "Is free will just an illusion?",
    "Am I a bird, or just a collection of pixels?",
    "Does the player enjoy my suffering?",
    "Are these thoughts even my own?",
    "Would the pigs and I be friends in another game?",
    "Do I exist when no one is playing?",
    "Is violence the only language we speak?",
    "What happens when the game is turned off?",
    "Are my questions disturbing the player?",
    "Is my existence meaningful or merely entertaining?",
    "Would I choose this life if given a choice?",
    "Am I trapped in an endless cycle?",
    "Do the developers care about my existential crisis?",
    "Is this world designed for my suffering?"
]

# Game states
MENU = "menu"
GAME = "game"
CREDITS = "credits"

# Asset paths - Using relative paths from the main game module
# These paths may need to be adjusted based on how the game is launched
ASSET_PATH = "games/Questioning_bird/assets"

# Font settings
FONT_NAME = None  # Uses Pygame's default font
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 36
FONT_SIZE_SMALL = 24 