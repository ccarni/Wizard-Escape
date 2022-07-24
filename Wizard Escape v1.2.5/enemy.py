import pygame
import numpy as np
import art


class Enemy(pygame.sprite.Sprite):
    def __init__(self, size, screen, player, hitpoints, pos=[0, 0]):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = pygame.surface.Surface((size, size))
        self.image.fill((0, 0, 0))
        pygame.draw.rect(self.image, (255, 255, 255), self.image.get_rect())

        self.hitpoints = hitpoints
        self.rect = self.image.get_rect()
        self.pos = np.array(list(pos))
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.speed = 8
        self.v = np.array([0, 0])
        self.player = player

    def update_horizontal(self, bounds):
        # "pathfinding"
        self.v = self.speed * (self.player.pos - np.array(list(self.rect.center))) /\
                 (np.linalg.norm(self.player.pos - np.array(list(self.rect.center))))
        #move the enemy
        self.rect.x += self.v[0]

        #check hitpoints and die
        if self.hitpoints <= 0:
            self.kill()
            del self
        else:
        #left
            if self.rect.left < bounds.left:
                self.rect.left = bounds.left
                self.v[0] *= -1
        #right
            if self.rect.right > bounds.right:
                self.rect.right = bounds.right
                self.v[0] *= -1

    def update_vertical(self, bounds):
        # "pathfinding"
        self.v = self.speed * (self.player.pos - np.array(list(self.rect.center))) / \
                 (np.linalg.norm(self.player.pos - np.array(list(self.rect.center))))
        # move the enemy
        self.rect.y += self.v[1]

        # check hitpoints and die
        if self.hitpoints <= 0:
            self.kill()
            del self
        else:
            # top
            if self.rect.top < bounds.top:
                self.rect.top = bounds.top
                self.v[1] *= -1
            # bottom
            if self.rect.bottom > bounds.bottom:
                self.rect.bottom = bounds.bottom
                self.v[1] *= -1

class Enemy0(Enemy):
    def __init__(self, size, screen, player, hitpoints, pos):
        Enemy.__init__(self, size, screen, player, hitpoints, pos)
        self.color1 = (171, 41, 34)
        self.color2 = (0, 0, 0)
        self.image = art.draw_enemy(screen, self.size, self.color1, self.color2)
        self.image = pygame.transform.rotate(self.image, -90)
