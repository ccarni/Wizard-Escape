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

    def flip(self, index):
        #self.image = pygame.transform.rotate(self.image, (self.rotate + 180) % 360)
        #self.v[index] *= -1
        self.destroy() # lazy so just replace flip will kill

    def destroy(self):
        self.kill()
        del self
        return

    def setup_image(self, draw_function):
        rotation = self.vector_to_angle(self.v)
        image = pygame.transform.rotate(draw_function, rotation)
        return image

    def update(self, bounds):
        #kill if over lifetime
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.destroy()

        self.rect.x += self.v[0]
        self.rect.y += self.v[1]

        if self.rect.left < bounds.left:
            self.rect.left = bounds.left
            self.flip(0)
        if self.rect.right > bounds.right:
            self.rect.right = bounds.right
            self.flip(0)
        if self.rect.top < bounds.top:
            self.rect.top = bounds.top
            self.flip(1)
        if self.rect.bottom > bounds.bottom:
            self.rect.bottom = bounds.bottom
            self.flip(1)

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
