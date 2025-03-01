import pygame
import json
import os
from ..constants import WIDTH, HEIGHT, MENU_BLUE, SELECTED_BLUE, WHITE
from ..entities.block import AngryBirdBlock, WoodenBlock

class LevelEditor:
    def __init__(self, screen, space, assets_dir):
        self.screen = screen
        self.space = space
        self.assets_dir = assets_dir
        self.blocks = []
        self.selected_type = "bird"  # "bird" or "wood"
        self.grid_size = 50  # Size of placement grid
        self.font = pygame.font.Font(None, 36)
        self.toolbar_height = 60
        self.buttons = [
            {"text": "Bird", "rect": pygame.Rect(10, 10, 100, 40), "type": "bird"},
            {"text": "Wood", "rect": pygame.Rect(120, 10, 100, 40), "type": "wood"},
            {"text": "Clear", "rect": pygame.Rect(230, 10, 100, 40), "type": "clear"},
            {"text": "Save", "rect": pygame.Rect(340, 10, 100, 40), "type": "save"},
            {"text": "Load", "rect": pygame.Rect(450, 10, 100, 40), "type": "load"},
            {"text": "Play", "rect": pygame.Rect(560, 10, 100, 40), "type": "play"}
        ]
        
        # Load images 
        try:
            self.angry_bird_image = pygame.image.load(os.path.join(assets_dir, 'angry_bird.png'))
        except:
            # Create fallback image if needed
            self.angry_bird_image = pygame.Surface((self.grid_size, self.grid_size))
            self.angry_bird_image.fill((255, 0, 0))
        
    def get_blocks(self):
        # Return a copy of the blocks list
        return list(self.blocks)

    def clear_blocks(self):
        for block in self.blocks:
            self.space.remove(block.body, block.shape)
        self.blocks.clear()
    
    def draw_toolbar(self):
        # Draw toolbar background
        pygame.draw.rect(self.screen, (50, 50, 50), (0, 0, WIDTH, self.toolbar_height))
        
        # Draw buttons
        for button in self.buttons:
            color = SELECTED_BLUE if button["type"] == self.selected_type else MENU_BLUE
            pygame.draw.rect(self.screen, color, button["rect"])
            text = self.font.render(button["text"], True, WHITE)
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)
    
    def draw_grid(self):
        # Draw placement grid
        for x in range(0, WIDTH, self.grid_size):
            pygame.draw.line(self.screen, (100, 100, 100), (x, self.toolbar_height), (x, HEIGHT), 1)
        for y in range(self.toolbar_height, HEIGHT, self.grid_size):
            pygame.draw.line(self.screen, (100, 100, 100), (0, y), (WIDTH, y), 1)
    
    def handle_click(self, pos):
        # Check toolbar buttons
        if pos[1] < self.toolbar_height:
            for button in self.buttons:
                if button["rect"].collidepoint(pos):
                    if button["type"] in ["bird", "wood"]:
                        self.selected_type = button["type"]
                    elif button["type"] == "clear":
                        self.clear_blocks()
                    elif button["type"] == "save":
                        self.save_level()
                    elif button["type"] == "load":
                        self.load_level()
                    elif button["type"] == "play":
                        return "play"
            return None
        
        # Place block on grid
        grid_x = (pos[0] // self.grid_size) * self.grid_size + self.grid_size // 2
        grid_y = (pos[1] // self.grid_size) * self.grid_size + self.grid_size // 2
        
        # Don't place blocks too close to slingshot
        if grid_x < 300:  # Safe zone for slingshot
            return None
            
        # Create new block
        if self.selected_type == "bird":
            block = AngryBirdBlock(grid_x, grid_y, self.grid_size, self.grid_size, self.space, self.angry_bird_image)
        else:
            block = WoodenBlock(grid_x, grid_y, self.grid_size, self.grid_size, self.space)
        
        # Remove any existing block at this position
        self.remove_block_at(grid_x, grid_y)
        
        # Add the new block
        self.blocks.append(block)
        self.space.add(block.body, block.shape)
        return None
    
    def remove_block_at(self, x, y):
        for block in self.blocks[:]:
            if (abs(block.body.position.x - x) < self.grid_size/2 and 
                abs(block.body.position.y - y) < self.grid_size/2):
                self.space.remove(block.body, block.shape)
                self.blocks.remove(block)
    
    def save_level(self):
        level_data = []
        for block in self.blocks:
            block_data = {
                "type": "bird" if isinstance(block, AngryBirdBlock) else "wood",
                "x": block.body.position.x,
                "y": block.body.position.y
            }
            level_data.append(block_data)
        
        save_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'levels')
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        with open(os.path.join(save_path, 'level1.json'), 'w') as f:
            json.dump(level_data, f)
    
    def load_level(self):
        self.clear_blocks()
        
        try:
            load_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'levels', 'level1.json')
            with open(load_path, 'r') as f:
                level_data = json.load(f)
            
            for block_data in level_data:
                if block_data["type"] == "bird":
                    block = AngryBirdBlock(block_data["x"], block_data["y"], self.grid_size, self.grid_size, self.space, self.angry_bird_image)
                else:
                    block = WoodenBlock(block_data["x"], block_data["y"], self.grid_size, self.grid_size, self.space)
                self.blocks.append(block)
                self.space.add(block.body, block.shape)
        except:
            pass  # Level file doesn't exist yet
    
    def draw(self):
        self.draw_grid()
        self.draw_toolbar()
        
        # Draw blocks
        for block in self.blocks:
            block.draw(self.screen)
        
        # Draw placement preview
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[1] > self.toolbar_height and mouse_pos[0] > 300:
            grid_x = (mouse_pos[0] // self.grid_size) * self.grid_size + self.grid_size // 2
            grid_y = (mouse_pos[1] // self.grid_size) * self.grid_size + self.grid_size // 2
            pygame.draw.rect(self.screen, (255, 255, 255, 128), 
                           (grid_x - self.grid_size/2, grid_y - self.grid_size/2, 
                            self.grid_size, self.grid_size), 2) 