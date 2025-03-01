import pygame
import pymunk
import math
from ..constants import COLLISION_TYPES

class AngryBirdBlock:
    def __init__(self, x, y, width, height, space, image):
        self.mass = 1
        self.width = width
        self.height = height
        self.body = pymunk.Body(self.mass, pymunk.moment_for_box(self.mass, (width, height)), body_type=pymunk.Body.KINEMATIC)
        self.body.position = x, y
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.elasticity = 0.4
        self.shape.friction = 0.8
        self.shape.collision_type = COLLISION_TYPES["BIRD"]
        self.destroyed = False
        self.image = image
        self.health = 1  # Birds only need one hit to destroy

    def make_dynamic(self):
        # Store current position and angle
        pos = self.body.position
        angle = self.body.angle
        
        # Create new dynamic body with proper moment
        moment = pymunk.moment_for_box(self.mass, (self.width, self.height))
        self.body = pymunk.Body(self.mass, moment, body_type=pymunk.Body.DYNAMIC)
        self.body.position = pos
        self.body.angle = angle
        
        # Create new shape with proper properties
        self.shape = pymunk.Poly.create_box(self.body, (self.width, self.height))
        self.shape.elasticity = 0.4
        self.shape.friction = 0.8
        self.shape.collision_type = COLLISION_TYPES["BIRD"]
        self.shape.mass = self.mass

    def draw(self, screen):
        if not self.destroyed:
            x = int(self.body.position.x)
            y = int(self.body.position.y)
            angle = math.degrees(self.body.angle)
            rotated_bird = pygame.transform.rotate(self.image, -angle)
            new_rect = rotated_bird.get_rect(center=(x, y))
            screen.blit(rotated_bird, new_rect.topleft)
            
    def damage(self):
        self.health -= 1
        if self.health <= 0:
            self.destroyed = True
            return True
        return False

class WoodenBlock:
    def __init__(self, x, y, width, height, space):
        self.mass = 2  # Heavier than birds
        self.width = width
        self.height = height
        self.body = pymunk.Body(self.mass, pymunk.moment_for_box(self.mass, (width, height)), body_type=pymunk.Body.KINEMATIC)
        self.body.position = x, y
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.elasticity = 0.2  # Less bouncy than birds
        self.shape.friction = 1.0    # More friction
        self.shape.collision_type = COLLISION_TYPES["WOOD"]
        self.color = (139, 69, 19)   # Brown color for wood
        self.destroyed = False
        self.health = 3  # Takes 3 hits to destroy

    def make_dynamic(self):
        # Store current position and angle
        pos = self.body.position
        angle = self.body.angle
        
        # Create new dynamic body with proper moment
        moment = pymunk.moment_for_box(self.mass, (self.width, self.height))
        self.body = pymunk.Body(self.mass, moment, body_type=pymunk.Body.DYNAMIC)
        self.body.position = pos
        self.body.angle = angle
        
        # Create new shape with proper properties
        self.shape = pymunk.Poly.create_box(self.body, (self.width, self.height))
        self.shape.elasticity = 0.2
        self.shape.friction = 1.0
        self.shape.collision_type = COLLISION_TYPES["WOOD"]
        self.shape.mass = self.mass

    def draw(self, screen):
        if not self.destroyed:
            vertices = [self.body.local_to_world(v) for v in self.shape.get_vertices()]
            # Draw wood texture (diagonal lines)
            pygame.draw.polygon(screen, self.color, vertices)
            # Add wood grain lines
            center = self.body.position
            angle = math.degrees(self.body.angle)
            for offset in range(-int(self.width/2), int(self.width/2), 8):
                start = (center[0] + offset, center[1] - self.height/2)
                end = (center[0] + offset, center[1] + self.height/2)
                rotated_start = self._rotate_point(start, center, angle)
                rotated_end = self._rotate_point(end, center, angle)
                pygame.draw.line(screen, (101, 67, 33), rotated_start, rotated_end, 1)

    def _rotate_point(self, point, center, angle):
        angle_rad = math.radians(angle)
        dx = point[0] - center[0]
        dy = point[1] - center[1]
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        new_dx = dx * cos_a - dy * sin_a
        new_dy = dx * sin_a + dy * cos_a
        return (center[0] + new_dx, center[1] + new_dy)

    def damage(self):
        self.health -= 1
        # Darken color as it takes damage
        self.color = (max(89, 139 - (3 - self.health) * 20), 
                     max(39, 69 - (3 - self.health) * 10), 
                     max(9, 19 - (3 - self.health) * 5))
        if self.health <= 0:
            self.destroyed = True
            return True
        return False 