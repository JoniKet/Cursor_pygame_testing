import pygame
import pymunk
import math
from ..constants import COLLISION_TYPES

class Pig:
    def __init__(self, x, y, space, image):
        self.mass = 5
        self.radius = 20
        self.moment = pymunk.moment_for_circle(self.mass, 0, self.radius)
        self.initial_pos = (x, y)
        self.space = space
        self.image = image
        self.create_body()
        
    def create_body(self, body_type=pymunk.Body.KINEMATIC):
        self.body = pymunk.Body(self.mass, self.moment, body_type=body_type)
        self.body.position = self.initial_pos
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 0.95
        self.shape.friction = 1.0
        self.shape.collision_type = COLLISION_TYPES["PIG"]
        self.space.add(self.body, self.shape)
        self.launched = False
        
    def draw(self, screen):
        try:
            x = int(self.body.position.x)
            y = int(self.body.position.y)
            if not (math.isnan(x) or math.isnan(y)):
                # Draw the pig image instead of a circle
                screen.blit(self.image, (x - self.radius, y - self.radius))
                # Rotate the pig based on velocity
                if self.launched and (self.body.velocity.x != 0 or self.body.velocity.y != 0):
                    angle = math.degrees(math.atan2(self.body.velocity.y, self.body.velocity.x))
                    rotated_pig = pygame.transform.rotate(self.image, -angle)
                    new_rect = rotated_pig.get_rect(center=(x, y))
                    screen.blit(rotated_pig, new_rect.topleft)
                else:
                    screen.blit(self.image, (x - self.radius, y - self.radius))
            else:
                self.reset()
        except (ValueError, AttributeError):
            self.reset()
        
    def reset(self):
        try:
            self.space.remove(self.body, self.shape)
        except:
            pass
        self.create_body(pymunk.Body.KINEMATIC)
        
    def launch(self, impulse):
        current_pos = self.body.position
        try:
            self.space.remove(self.body, self.shape)
        except:
            pass
        self.body = pymunk.Body(self.mass, self.moment, body_type=pymunk.Body.DYNAMIC)
        self.body.position = current_pos
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 0.95
        self.shape.friction = 1.0
        self.shape.collision_type = COLLISION_TYPES["PIG"]
        self.space.add(self.body, self.shape)
        self.launched = True
        self.body.apply_impulse_at_local_point(impulse) 