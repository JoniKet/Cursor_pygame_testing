import pygame
import math

class Slingshot:
    def __init__(self, x, y):
        self.pos = (x, y)
        # Colors for the slingshot
        self.wood_color = (139, 69, 19)  # Brown
        self.dark_wood = (101, 67, 33)   # Dark brown
        self.band_color = (60, 60, 60)   # Dark gray for rubber band
        # Dimensions
        self.fork_length = 80  # Length of Y arms
        self.base_height = 100  # Height of the base
        self.thickness = 12     # Thickness of the wood
        self.band_thickness = 4 # Thickness of the rubber band
        # Angles
        self.left_angle = 30   # Angle for left fork
        self.right_angle = -30 # Angle for right fork
        self.base_angle = 0    # Angle for the main trunk
        
    def draw(self, screen, pig_pos=None):
        x, y = self.pos
        
        # Draw base trunk
        pygame.draw.rect(screen, self.dark_wood, 
                        (x - self.thickness//2, y - self.base_height, 
                         self.thickness, self.base_height))
        
        # Calculate fork positions
        fork_base_x = x
        fork_base_y = y - self.base_height
        
        # Draw left fork
        left_angle_rad = math.radians(self.left_angle)
        left_end_x = fork_base_x + math.sin(left_angle_rad) * self.fork_length
        left_end_y = fork_base_y - math.cos(left_angle_rad) * self.fork_length
        pygame.draw.line(screen, self.dark_wood, 
                        (fork_base_x, fork_base_y),
                        (left_end_x, left_end_y), self.thickness)
        
        # Draw right fork
        right_angle_rad = math.radians(self.right_angle)
        right_end_x = fork_base_x + math.sin(right_angle_rad) * self.fork_length
        right_end_y = fork_base_y - math.cos(right_angle_rad) * self.fork_length
        pygame.draw.line(screen, self.dark_wood, 
                        (fork_base_x, fork_base_y),
                        (right_end_x, right_end_y), self.thickness)
        
        # Draw rubber bands
        if pig_pos:
            # Draw stretched rubber bands
            pygame.draw.line(screen, self.band_color, 
                           (left_end_x, left_end_y), pig_pos, self.band_thickness)
            pygame.draw.line(screen, self.band_color, 
                           (right_end_x, right_end_y), pig_pos, self.band_thickness)
        else:
            # Draw relaxed rubber band
            center_x = (left_end_x + right_end_x) / 2
            center_y = (left_end_y + right_end_y) / 2 + 20
            pygame.draw.line(screen, self.band_color, 
                           (left_end_x, left_end_y), 
                           (center_x, center_y), self.band_thickness)
            pygame.draw.line(screen, self.band_color, 
                           (right_end_x, right_end_y), 
                           (center_x, center_y), self.band_thickness) 