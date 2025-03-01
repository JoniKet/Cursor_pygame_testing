import pygame
import math
import random
import os
import sys

# Add parent directory to path for direct execution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    # Try importing with full package path first (when run through main launcher)
    from games.Questioning_bird.src.constants import (
        SCREEN_WIDTH, SCREEN_HEIGHT, BIRD_WIDTH, BIRD_HEIGHT,
        BIRD_RADIUS, ROTATION_SPEED, SHOOT_COOLDOWN, BIRD_COLOR,
        BIRD_THOUGHTS, BIRD_QUESTIONS, POPUP_CHANCE, POPUP_COOLDOWN,
        BIRD_ANGER_THRESHOLD, BIRD_ANGER_COOLDOWN, BIRD_ANGER_DURATION,
        BIRD_ANGER_KEYWORDS, ANGRY_BIRD_THOUGHTS
    )
except ImportError:
    # Fall back to local import for direct execution
    from src.constants import (
        SCREEN_WIDTH, SCREEN_HEIGHT, BIRD_WIDTH, BIRD_HEIGHT,
        BIRD_RADIUS, ROTATION_SPEED, SHOOT_COOLDOWN, BIRD_COLOR,
        BIRD_THOUGHTS, BIRD_QUESTIONS, POPUP_CHANCE, POPUP_COOLDOWN,
        BIRD_ANGER_THRESHOLD, BIRD_ANGER_COOLDOWN, BIRD_ANGER_DURATION,
        BIRD_ANGER_KEYWORDS, ANGRY_BIRD_THOUGHTS
    )

class Bird:
    """Bird class that represents the player character"""
    
    def __init__(self, x, y, assets):
        """Initialize bird position and assets"""
        self.x = x
        self.y = y
        self.assets = assets
        self.original_image = assets.get_image('bird')
        # Resize image if needed
        self.original_image = pygame.transform.scale(self.original_image, (BIRD_WIDTH, BIRD_HEIGHT))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        
        # Bird rotation attributes
        self.angle = 0  # In degrees, 0 is right, 90 is down
        
        # Thinking timer and messages
        self.thinking_timer = 0
        self.current_thought = ""
        self.thought_duration = 0
        
        # Dialog popup timer
        self.popup_timer = 0
        self.popup_cooldown = POPUP_COOLDOWN
        
        # Response to player choices
        self.current_response = ""
        self.response_timer = 0
        self.response_duration = 180  # 3 seconds at 60 FPS
        
        # Anger state
        self.anger_level = 0
        self.is_angry = False
        self.anger_timer = 0
        self.anger_cooldown = 0
        
        # Autonomous movement
        self.movement_timer = 0
        self.movement_duration = random.randint(120, 240)  # 2-4 seconds at 60 FPS
        self.target_angle = random.randint(0, 360)  # Random initial angle
        self.idle_rotation_speed = 0.5  # Slower rotation when idle
        
        # Fast rotation complaints
        self.fast_rotation_speed = ROTATION_SPEED * 2.5  # Faster rotation when targeting pigs
        self.complaint_timer = 0
        self.complaint_cooldown = 120  # 2 seconds between complaints
        self.rotation_complaints = [
            "Ugh! Too @#$% fast!",
            "I'm getting *&^% dizzy!",
            "Slow down, darn it!",
            "My @#$% neck hurts!",
            "This is %^&* ridiculous!",
            "Who designed this @#$%?!",
            "I hate this *&^% job!",
            "Can't keep up with this @#$%!",
            "Blasted pigs! *&^%!",
            "My head is @#$% spinning!",
            "Holy @#$%! Too fast!",
            "What the @#$%?!",
            "Son of a @#$%!",
            "This is bull@#$%!",
            "Mother@#$%er!",
            "For @#$%'s sake!",
            "Are you @#$% kidding me?!",
            "This is @#$% insane!",
            "I can't @#$% do this!",
            "My @#$% life..."
        ]
        
    def update(self, target_angle=None):
        """Update bird state"""
        # Handle anger state
        if self.is_angry:
            self.anger_timer -= 1
            if self.anger_timer <= 0:
                self.is_angry = False
                print("Bird is no longer angry")
                
            # When angry, bird rotates randomly
            self.angle = (self.angle + random.uniform(-5, 5)) % 360
        else:
            # If target_angle is provided (from targeting a pig), use it
            if target_angle is not None:
                # Smoothly rotate towards target angle
                angle_diff = (target_angle - self.angle) % 360
                if angle_diff > 180:
                    angle_diff -= 360
                
                # Check if we need to rotate quickly (large angle difference)
                large_rotation = abs(angle_diff) > 45
                rotation_speed = self.fast_rotation_speed if large_rotation else ROTATION_SPEED
                
                # Rotate towards target at appropriate speed
                if abs(angle_diff) > rotation_speed:
                    if angle_diff > 0:
                        self.angle = (self.angle + rotation_speed) % 360
                    else:
                        self.angle = (self.angle - rotation_speed) % 360
                        
                    # Complain about fast rotation if rotating quickly
                    if large_rotation and self.complaint_timer <= 0:
                        self.current_thought = random.choice(self.rotation_complaints)
                        self.thinking_timer = 60  # Show complaint for 1 second
                        self.thought_duration = self.thinking_timer
                        self.complaint_timer = self.complaint_cooldown
                else:
                    self.angle = target_angle
            else:
                # Autonomous movement when no pigs to target
                self.movement_timer += 1
                if self.movement_timer >= self.movement_duration:
                    # Choose a new random target angle
                    self.target_angle = random.randint(0, 360)
                    self.movement_duration = random.randint(120, 240)
                    self.movement_timer = 0
                
                # Rotate slowly towards the random target angle
                angle_diff = (self.target_angle - self.angle) % 360
                if angle_diff > 180:
                    angle_diff -= 360
                
                if abs(angle_diff) > self.idle_rotation_speed:
                    if angle_diff > 0:
                        self.angle = (self.angle + self.idle_rotation_speed) % 360
                    else:
                        self.angle = (self.angle - self.idle_rotation_speed) % 360
        
        # Rotate the image
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        # Update thinking
        self.thinking_timer -= 1
        if self.thinking_timer <= 0:
            # Chance to generate a new thought
            if random.random() < 0.01:  # 1% chance per frame
                if self.is_angry:
                    self.current_thought = random.choice(ANGRY_BIRD_THOUGHTS)
                else:
                    self.current_thought = random.choice(BIRD_THOUGHTS)
                self.thinking_timer = random.randint(180, 300)  # 3-5 seconds
                self.thought_duration = self.thinking_timer
        
        # Update dialog popup timer
        self.popup_timer -= 1
        if self.popup_timer <= 0:
            self.popup_timer = self.popup_cooldown
        
        # Update response timer
        if self.current_response:
            self.response_timer -= 1
            if self.response_timer <= 0:
                self.current_response = ""
        
        # Update anger cooldown
        if self.anger_cooldown > 0:
            self.anger_cooldown -= 1
        
        # Update complaint timer
        if self.complaint_timer > 0:
            self.complaint_timer -= 1
        
    def should_show_dialog(self):
        """Check if it's time to show a dialog popup"""
        if self.popup_timer >= self.popup_cooldown:
            # Small random chance to show dialog
            if random.random() < POPUP_CHANCE:
                self.popup_timer = 0
                # Play question sound when showing dialog
                self.assets.play_sound('question', volume=0.8)
                return True
        return False
    
    def set_response(self, option_index, question_data):
        """Set the bird's response based on player's choice"""
        if not question_data:
            return
            
        # Get the selected option text
        selected_option = question_data["options"][option_index]
        print(f"Selected option: {selected_option}")
        
        # Check if the option contains any anger keywords
        print(f"Checking for anger keywords: {BIRD_ANGER_KEYWORDS}")
        
        # Print current anger level for debugging
        print(f"Current anger level: {self.anger_level}")
        
        # Check if any anger keywords are in the selected option
        for keyword in BIRD_ANGER_KEYWORDS:
            if keyword.lower() in selected_option.lower():
                print(f"Anger keyword found! Increasing anger level.")
                self.anger_level += 1
                print(f"Anger level increased to: {self.anger_level}")
                break
        
        # Set the response based on the option index
        if "responses" in question_data and len(question_data["responses"]) > option_index:
            self.current_response = question_data["responses"][option_index]
        else:
            # Default responses if not specified
            default_responses = [
                "Interesting perspective...",
                "I hadn't thought of it that way.",
                "That's one way to look at it.",
                "Hmm, I'll have to ponder that."
            ]
            self.current_response = random.choice(default_responses)
        
        # Reset response timer
        self.response_timer = self.response_duration
        
        # Check if anger threshold reached
        if self.anger_level >= BIRD_ANGER_THRESHOLD:
            self.become_angry()
            self.anger_level = 0  # Reset anger level after becoming angry
    
    def become_angry(self):
        """Make the bird angry"""
        if not self.is_angry and self.anger_cooldown <= 0:
            print("BIRD IS BECOMING ANGRY!")
            self.is_angry = True
            self.anger_timer = BIRD_ANGER_DURATION
            self.anger_cooldown = BIRD_ANGER_COOLDOWN
            
            # Play angry sound
            self.assets.play_sound('angry', volume=1.0)
            
            # Set an angry thought
            self.current_thought = random.choice(ANGRY_BIRD_THOUGHTS)
            self.thinking_timer = 120  # Show thought for 2 seconds
            self.thought_duration = self.thinking_timer
    
    def is_ready_to_attack(self):
        """Check if the bird is ready to attack the player"""
        return self.is_angry and self.anger_timer <= BIRD_ANGER_DURATION / 2
    
    def get_attack_position(self):
        """Get the position for the special attack bullet"""
        return self.x, self.y
    
    def draw(self, screen):
        """Draw the bird on the screen"""
        # Draw the bird image
        screen.blit(self.image, self.rect)
        
        # Draw thought bubble if thinking
        if self.current_thought and self.thinking_timer > 0:
            self.draw_thought_bubble(screen, self.current_thought)
        
        # Draw response if active
        if self.current_response and self.response_timer > 0:
            self.draw_response(screen, self.current_response)
    
    def draw_thought_bubble(self, screen, text):
        """Draw a thought bubble with the given text"""
        font = pygame.font.Font(None, 24)
        
        # Check if this is a complaint (contains @#$% or *&^%)
        is_complaint = "@#$%" in text or "*&^%" in text
        
        # Create a text surface with appropriate color
        text_color = (255, 50, 50) if is_complaint else (0, 0, 0)  # Red for complaints, black for normal thoughts
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect()
        
        # Position the bubble above the bird
        bubble_x = self.x - text_rect.width // 2
        bubble_y = self.y - text_rect.height - 40
        
        # Ensure bubble stays on screen
        bubble_x = max(10, min(bubble_x, SCREEN_WIDTH - text_rect.width - 10))
        bubble_y = max(10, bubble_y)
        
        # Draw bubble background
        padding = 10
        bubble_rect = pygame.Rect(
            bubble_x - padding,
            bubble_y - padding,
            text_rect.width + padding * 2,
            text_rect.height + padding * 2
        )
        
        # Draw background with appropriate color
        bubble_bg_color = (255, 220, 220) if is_complaint else (255, 255, 255)  # Light red for complaints
        bubble_border_color = (200, 0, 0) if is_complaint else (0, 0, 0)  # Red border for complaints
        
        # Draw bubble with appropriate style
        pygame.draw.ellipse(screen, bubble_bg_color, bubble_rect)
        pygame.draw.ellipse(screen, bubble_border_color, bubble_rect, 2)
        
        # Draw connecting circles (smaller bubbles leading to bird)
        circle_sizes = [6, 4, 2]
        for i, size in enumerate(circle_sizes):
            circle_x = self.x
            circle_y = self.y - 20 - (i * 8)
            pygame.draw.circle(screen, bubble_bg_color, (circle_x, circle_y), size)
            pygame.draw.circle(screen, bubble_border_color, (circle_x, circle_y), size, 1)
        
        # Draw the text
        screen.blit(text_surface, (bubble_x, bubble_y))
    
    def draw_response(self, screen, text):
        """Draw the bird's response"""
        font = pygame.font.Font(None, 24)
        
        # Create a text surface
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        
        # Position the response below the bird
        response_x = self.x - text_rect.width // 2
        response_y = self.y + BIRD_HEIGHT // 2 + 20
        
        # Ensure response stays on screen
        response_x = max(10, min(response_x, SCREEN_WIDTH - text_rect.width - 10))
        response_y = min(response_y, SCREEN_HEIGHT - text_rect.height - 10)
        
        # Draw response background
        padding = 10
        response_rect = pygame.Rect(
            response_x - padding,
            response_y - padding,
            text_rect.width + padding * 2,
            text_rect.height + padding * 2
        )
        
        # Draw white background with black border
        pygame.draw.rect(screen, (255, 255, 255), response_rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), response_rect, 2, border_radius=10)
        
        # Draw the text
        screen.blit(text_surface, (response_x, response_y)) 