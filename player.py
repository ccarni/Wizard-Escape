import pygame
import numpy as np
import attacks
import art


class Player(pygame.sprite.Sprite):
    def __init__(self, color, pos):
        pygame.sprite.Sprite.__init__(self)
        self.size = 40
        self.image = pygame.surface.Surface((self.size, self.size))
        # rects and positions
        self.pos = np.array(list(pos))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.max_health = 5
        self.health = self.max_health
        self.dead = False

        # physics and movement
        self.dir = [0, 0]
        self.last_dir = self.dir
        self.speed = 7

        # sprite stuff
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.rect(self.image, color, self.image.get_rect())

        self.color1 = (73, 48, 199)
        self.color2 = (0, 0, 0)

        self.projectiles = pygame.sprite.Group()

        #attacks
        self.primary_cooldown = 0
        self.secondary_cooldown = 0
        self.set_attack(0, attacks.fireball, attacks.fireball_cooldown)
        self.set_attack(1, attacks.earth, attacks.earth_cooldown)

    def attack(self, attack_type, mouse_pos, screen):
        if attack_type == 1:
            self.projectiles.add(self.primary_attack(mouse_pos, self.rect.center, screen))
        else:
            self.projectiles.add(self.secondary_attack(mouse_pos, self.rect.center, screen))

    def set_attack(self, mode, attack, cooldown):
        if mode == 0:
            self.primary_attack = attack
            self.primary_attack_cooldown = cooldown
        else:
            self.secondary_attack = attack
            self.secondary_attack_cooldown = cooldown

    def move_horizontal(self, bounds):
        # move player
        self.rect.x += self.dir[0] * self.speed

        # --------------- check boundaries ------------------
        # left
        if self.rect.left < bounds.left:
            self.rect.left = bounds.left
            self.rect.x -= self.dir[0]
        # right
        if self.rect.right > bounds.right:
            self.rect.right = bounds.right
            self.rect.x -= self.dir[0]

        # update position
        self.pos = np.array(self.rect.center)

    def move_vertical(self, bounds):
        # move player
        self.rect.y += self.dir[1] * self.speed

        # --------------- check boundaries -----------------
        # top
        if self.rect.top < bounds.top:
            self.rect.top = bounds.top
            self.rect.y -= self.dir[1]
        # down
        if self.rect.bottom > bounds.bottom:
            self.rect.bottom = bounds.bottom
            self.rect.y -= self.dir[1]

        # update position
        self.pos = np.array(self.rect.center)
    
    def update(self, primary_attack, secondary_attack, mouse_pos, screen):
        self.dead = True if self.health <= 0 else False

        # auto shooting timer
        self.primary_cooldown += 1
        self.secondary_cooldown += 1
        if primary_attack and self.primary_cooldown > self.primary_attack_cooldown:
            self.attack(1, mouse_pos, screen)
            self.primary_cooldown, self.secondary_cooldown = 0, 0
        if secondary_attack and self.secondary_cooldown > self.secondary_attack_cooldown:
            self.attack(2, mouse_pos, screen)
            self.primary_cooldown, self.secondary_cooldown = 0, 0

    def draw(self, screen):
        
        #put player on screen
        player_surf, self.last_dir = art.draw_player(screen, self.size, self.color1, self.color2, self.dir, self.last_dir)
        screen.blit(player_surf, self.rect.topleft)
