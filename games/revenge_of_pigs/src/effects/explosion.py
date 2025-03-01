from .particle import Particle

class Explosion:
    def __init__(self, x, y):
        self.particles = [Particle(x, y) for _ in range(30)]
        
    def update(self):
        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.particles if p.lifetime > 0]
        
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
    
    @property
    def is_alive(self):
        return len(self.particles) > 0 