import pygame

# Window dimensions
WIDTH = 1200
HEIGHT = 800

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
MENU_BLUE = (100, 149, 237)  # Cornflower blue for menu
SELECTED_BLUE = (65, 105, 225)  # Royal blue for selected items

# Game physics
GRAVITY = (0, 900)

# Slingshot properties
SLINGSHOT_X = 100
SLINGSHOT_Y = HEIGHT - 150
MAX_STRETCH = 120
SLINGSHOT_POS = (SLINGSHOT_X, SLINGSHOT_Y)

# Block properties
BLOCK_SIZE = 50
STACK_START_X = 900
STACK_START_Y = HEIGHT - 100

# Ground properties
GAP_WIDTH = 200

# Collision types
COLLISION_TYPES = {
    "PIG": 1,
    "BIRD": 2,
    "WOOD": 3
} 