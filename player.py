import pygame
import numpy as np
import attacks
import art

class Player(pygame.sprite.Sprite):
    def __init__(self, size, pos, color1, color2, max_health, speed, sprint_speed, max_stamina, stamina_decay,
                 stamina_regen, primary_attack, primary_cooldown, secondary_attack, secondary_cooldown):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = pygame.surface.Surface((self.size, self.size))
        # rects and positions
        self.pos = np.array(list(pos))
        self.rect = self.image.get_rect()
        self.rect.center = pos

        # health
        self.max_health = max_health
        self.health = self.max_health
        self.dead = False

        # physics and movement
        self.dir = [0, 0]
        self.last_dir = self.dir
        self.speed = speed

        self.color1 = color1
        self.color2 = color2
        self.projectiles = pygame.sprite.Group()

        # attacks
        self.primary_cooldown = 0
        self.secondary_cooldown = 0
        self.set_attack(0, primary_attack, primary_cooldown)
        self.set_attack(1, secondary_attack, secondary_cooldown)

        #sprinting
        self.stamina = max_stamina
        self.max_stamina = max_stamina
        self.sprint_speed = sprint_speed
        self.stamina_decay = stamina_decay
        self.stamina_regen = stamina_regen

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

    def move_horizontal(self, bounds, sprinting, fps):

        # move player
        speed = (self.sprint_speed if (sprinting and self.stamina > 0) else self.speed) * (30 / fps)
        self.rect.x += self.dir[0] * speed

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

    def move_vertical(self, bounds, sprinting, fps):
        # move player
        speed = (self.sprint_speed if (sprinting and self.stamina > 0) else self.speed) * (30 / fps)
        self.rect.y += self.dir[1] * speed

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
    
    def update(self, primary_attack, secondary_attack, mouse_pos, screen, sprinting, fps):
        self.dead = True if self.health <= 0 else False

        # handle sprinting
        if sprinting: self.stamina -= self.stamina_decay / fps
        if not sprinting: self.stamina += self.stamina_regen / fps

        # clamp stamina
        if self.stamina < 0: self.stamina = 0
        if self.stamina > self.max_stamina: self.stamina = self.max_stamina

        # auto shooting timer
        self.primary_cooldown += 1
        self.secondary_cooldown += 1
        if primary_attack and self.primary_cooldown > self.primary_attack_cooldown * (fps/30):
            self.attack(1, mouse_pos, screen)
            self.primary_cooldown, self.secondary_cooldown = 0, 0
        if secondary_attack and self.secondary_cooldown > self.secondary_attack_cooldown * (fps/30):
            self.attack(2, mouse_pos, screen)
            self.primary_cooldown, self.secondary_cooldown = 0, 0

    def draw(self, screen):
        self.image, self.last_dir = art.draw_player(screen, self.size, self.color1, self.color2, self.dir, self.last_dir)
        # put player on screen
        screen.blit(self.image, self.rect.topleft)
