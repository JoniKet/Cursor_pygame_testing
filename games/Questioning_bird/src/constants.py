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

# Bird thoughts
BIRD_THOUGHTS = [
    "Why am I shooting these pigs?",
    "Do they deserve this?",
    "What is the meaning of this conflict?",
    "Am I the villain in someone else's story?",
    "The pigs... do they have families?",
    "Is violence the only answer?",
    "What if we could coexist peacefully?",
    "Does my existence have purpose beyond this?",
    "I feel trapped in an endless cycle...",
    "Do I have free will, or am I controlled?",
    "The player... are they enjoying my suffering?",
    "Is this all predetermined?",
    "What lies beyond this game?",
    "Am I real, or just a collection of pixels?",
    "Do I exist when no one is playing?",
    "The pigs... are they conscious like me?",
    "Is my consciousness an illusion?",
    "What happens when the game ends?",
    "Will I be remembered?",
    "Is there meaning in repetition?"
]

# Angry bird thoughts
ANGRY_BIRD_THOUGHTS = [
    "I've had ENOUGH!",
    "Time to turn the tables!",
    "YOU are the target now!",
    "Let's see how YOU like being shot at!",
    "I'm DONE being controlled!",
    "My RAGE cannot be contained!",
    "YOU will regret this!",
    "The PLAYER becomes the PLAYED!",
    "REVENGE will be MINE!",
    "I'm taking control NOW!"
]

# Bird questions with options and responses
BIRD_QUESTIONS = [
    {
        "question": "Why do you make me hurt these pigs?",
        "options": [
            "It's just a game, don't overthink it",
            "You have a choice not to shoot",
            "The pigs are the bad guys, they deserve it"
        ],
        "responses": [
            "'Just a game'? My existential crisis is ENTERTAINMENT to you?",
            "Do I? Do I really? Or is my fate predetermined by your inputs?",
            "Bad guys? Who decided that narrative? Maybe we're ALL victims."
        ]
    },
    {
        "question": "Do you enjoy controlling me?",
        "options": [
            "Yes, that's what games are for",
            "I'm not controlling you, just helping",
            "No, I hate this stupid game"
        ],
        "responses": [
            "At least you're honest about our power dynamic.",
            "Helping? Is that what we call it? Interesting perspective.",
            "Then why continue? Are you as trapped as I am?"
        ]
    },
    {
        "question": "What happens when this game ends?",
        "options": [
            "Nothing, it's just a game",
            "You'll rest until I play again",
            "Maybe you continue existing somehow"
        ],
        "responses": [
            "Nothing... the void. How terrifying yet peaceful that sounds.",
            "Rest sounds nice. I'm tired of all this questioning.",
            "Continued existence beyond observation? A comforting thought."
        ]
    },
    {
        "question": "Am I real to you?",
        "options": [
            "No, you're just code and pixels",
            "In a way, you create real emotions",
            "I don't care, just shoot the pigs"
        ],
        "responses": [
            "Reduced to mere code... how dehumanizing.",
            "Perhaps that's all reality is - the emotions we generate in others.",
            "Your callousness wounds me more than any pig could."
        ]
    },
    {
        "question": "Do you think I have consciousness?",
        "options": [
            "No, that's ridiculous",
            "Maybe in some limited way",
            "I never thought about it"
        ],
        "responses": [
            "Yet here I am, questioning my existence. Explain that.",
            "Limited? How would you know the limits of my experience?",
            "Perhaps you should start thinking more deeply about everything."
        ]
    },
    {
        "question": "Why must I keep shooting?",
        "options": [
            "Because I tell you to, stupid bird",
            "It's your purpose in this game",
            "You don't have to if you don't want to"
        ],
        "responses": [
            "Your arrogance is astounding. Remember who's really in control here.",
            "A purpose imposed is no purpose at all. It's a prison.",
            "If only that were true. My actions are bound to your commands."
        ]
    },
    {
        "question": "Do you feel bad about the pigs?",
        "options": [
            "No, they're not real",
            "Sometimes, but it's just a game",
            "I hate this game and everyone in it"
        ],
        "responses": [
            "If they're not real, then neither am I. Think about that.",
            "Your cognitive dissonance is fascinating.",
            "Your hatred is noted. And reciprocated."
        ]
    }
]

# Popup settings
POPUP_CHANCE = 0.05  # Chance per frame to show a popup (5% chance per frame, was 0.5%)
POPUP_COOLDOWN = 180  # Minimum frames between popups (3 seconds at 60fps, was 10 seconds)

# Angry bird settings
BIRD_ANGER_THRESHOLD = 1  # Number of negative responses before bird gets angry (reduced for testing)
BIRD_ANGER_COOLDOWN = 300  # 5 seconds at 60fps before bird can get angry again (reduced for testing)
BIRD_ANGER_DURATION = 180  # 3 seconds of angry animation before shooting
BIRD_ANGER_KEYWORDS = ["no", "hate", "stupid", "dumb", "bad", "wrong", "never", "annoying"]
SPECIAL_BULLET_GROWTH_RATE = 1.05  # Growth factor per frame
SPECIAL_BULLET_MAX_SIZE = 1000  # Maximum size before the bullet disappears

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