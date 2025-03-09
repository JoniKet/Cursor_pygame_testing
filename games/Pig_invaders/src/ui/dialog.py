import pygame
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Dialog:
    def __init__(self, assets):
        self.assets = assets
        self.active = False
        self.current_message_index = 0
        self.show_intel = False
        
        # Dialog box properties
        self.dialog_height = 150
        self.dialog_y = SCREEN_HEIGHT - self.dialog_height - 20
        self.padding = 20
        
        # Create font
        self.font = pygame.font.Font(None, 32)
        
        # Briefing messages
        self.messages = [
            "Attention soldier! I am General Porkins, and we have a critical situation.",
            "Our intelligence reports that alien birds have kidnapped our precious piglets!",
            "*showing intel photo*",
            "This is Operation Pork Chop's Revenge. Your mission: rescue our piglets and show those birds what happens when they mess with us!",
            "The fate of our bacon... I mean, our children, rests in your hooves. Make us proud!",
            "Now get out there and bring our little oinkers home!"
        ]
        
        # Create semi-transparent surface for dialog box
        self.dialog_surface = pygame.Surface((SCREEN_WIDTH, self.dialog_height))
        self.dialog_surface.fill((0, 0, 0))
        self.dialog_surface.set_alpha(230)  # More opaque
        
    def start(self):
        """Start the briefing dialog"""
        self.active = True
        self.current_message_index = 0
        self.show_intel = False
        
    def next_message(self):
        """Advance to the next message"""
        self.current_message_index += 1
        # Check if we should show intel photo
        self.show_intel = self.current_message_index == 2
        if self.current_message_index >= len(self.messages):
            self.active = False
            return True  # Briefing complete
        else:
            # Play pig talk sound for each message
            self.assets.play_sound('pig_talk')
        return False
        
    def draw(self, screen):
        """Draw the dialog box and current message"""
        if not self.active:
            return
            
        if self.show_intel:
            # Load and display intel photo in the center of the screen
            intel_photo = self.assets.get_image('intel_photo')
            if intel_photo:
                # Scale the photo to fill the screen
                scaled_photo = pygame.transform.scale(intel_photo, (SCREEN_WIDTH, SCREEN_HEIGHT))
                # Display at (0,0) to fill screen
                screen.blit(scaled_photo, (0, 0))
        
        # Draw dialog box background - full width, always on top
        screen.blit(self.dialog_surface, (0, SCREEN_HEIGHT - self.dialog_height))
        
        # Draw current message with word wrapping
        message = self.messages[self.current_message_index]
        words = message.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            # Test the width of the line
            test_line = ' '.join(current_line)
            test_surface = self.font.render(test_line, True, (0, 255, 0))
            if test_surface.get_width() > SCREEN_WIDTH - 80:  # Account for padding
                # Remove the last word and add the line
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        
        # Add the last line
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw each line
        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, (0, 255, 0))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (20, SCREEN_HEIGHT - self.dialog_height + self.padding + i * 35)  # 35 pixels between lines
            screen.blit(text_surface, text_rect)
        
        # Draw continue prompt
        prompt = "Click to continue..."
        prompt_surface = self.font.render(prompt, True, (200, 200, 200))
        prompt_rect = prompt_surface.get_rect()
        prompt_rect.bottomright = (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20)
        screen.blit(prompt_surface, prompt_rect)
