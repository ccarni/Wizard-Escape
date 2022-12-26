from matplotlib import projections
import pygame
import numpy as np
import art

class Projectile(pygame.sprite.Sprite):
    def __init__(self, size, screen, pos=(0, 0), v=(0,0), lifetime=300, damage=1):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.screen = screen

        #sprite stuff
        self.image = pygame.surface.Surface((size, size))
        self.image.fill((0, 0, 0))
        pygame.draw.rect(self.image, (0, 0, 0), self.image.get_rect())
        self.image.set_colorkey((0,0,0))

        self.lifetime = lifetime
        self.damage = damage
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.v = np.array(v)

    def vector_to_angle(self, v):
        vector = np.array(v)
        angle = -np.degrees(np.arctan2(vector[1], vector[0])) % 360.0
        return angle

    def destroy(self):
        self.kill()
        del self
        return

    def setup_image(self, draw_function):
        rotation = self.vector_to_angle(self.v)
        image = pygame.transform.rotate(draw_function, rotation)
        return image

    def update(self, bounds, fps):
        # kill if over lifetime
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.destroy()

        self.rect.x += self.v[0] * (30/fps)
        self.rect.y += self.v[1] * (30/fps)

        if self.rect.left < bounds.left or self.rect.right > bounds.right or self.rect.top < bounds.top or self.rect.bottom > bounds.bottom:
            self.destroy()

class Fireball(Projectile):
    def __init__(self, size, screen, pos=(0, 0), v=(0,0), lifetime=300, damage=1):
        Projectile.__init__(self, size, screen, pos, v, lifetime, damage)
        self.image = self.setup_image(art.draw_fireball(self.screen, self.size))

class Ice(Projectile):
    def __init__(self, size, screen, pos=(0, 0), v=(0,0), lifetime=300, damage=1):
        Projectile.__init__(self, size, screen, pos, v, lifetime, damage)
        self.image = self.setup_image(art.draw_ice(self.screen, self.size))

class Earth(Projectile):
    def __init__(self, size, screen, pos=(0, 0), v=(0,0), lifetime=300, damage=1):
        Projectile.__init__(self, size, screen, pos, v, lifetime, damage)
        self.image = self.setup_image(art.draw_earth(self.screen, self.size))

class Wind(Projectile):
    def __init__(self, size, screen, pos=(0, 0), v=(0,0), lifetime=300, damage=1):
        Projectile.__init__(self, size, screen, pos, v, lifetime, damage)
        self.image = self.setup_image(art.draw_wind(self.screen, self.size))

class Leaf(Projectile):
    def __init__(self, size, screen, pos=(0, 0), v=(0, 0), lifetime=300, damage=1):
        Projectile.__init__(self, size, screen, pos, v, lifetime, damage)
        self.image = self.setup_image(art.draw_leaf(self.screen, self.size))
