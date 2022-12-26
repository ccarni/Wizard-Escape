import pygame


class Powerup(pygame.sprite.Sprite):
    def __init__(self, screen, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = image.copy()
        self.rect = image.get_rect()
        self.x = pos[0]
        self.y = pos[1]
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    # runner passed in so that powerup can do anything needed
    def on_interact(self, runner):
        print('interact function not implemented')


class Heart(Powerup):
    def __init__(self, screen, image, pos):
        Powerup.__init__(self, screen, image, pos)

    def on_interact(self, runner):
        if runner.player.health < runner.player.max_health:
            runner.player.health += 1
            self.kill()
            del self

class GoldHeart(Powerup):
    def __init__(self, screen, image, pos):
        Powerup.__init__(self, screen, image, pos)

    def on_interact(self, runner):
        runner.player.max_health += 1
        runner.player.health += 2
        if runner.player.health > runner.player.max_health:
            runner.player.health = runner.player.max_health
        self.kill()
        del self

class Trophy(Powerup):
    def __init__(self, screen, image, pos):
        Powerup.__init__(self, screen, image, pos)

    def on_interact(self, runner):
        runner.won_game = True
        self.kill()
        del self

class Attack(Powerup):
    def __init__(self, screen, image, pos, attack, attack_cooldown):
        Powerup.__init__(self, screen, image, pos)
        self.attack = attack
        self.attack_cooldown = attack_cooldown

    def on_interact(self, runner):
        if runner.primary_pickup:
            previous_attack = runner.player.primary_attack
            previous_cooldown = runner.player.primary_attack_cooldown
            runner.player.set_attack(0, self.attack, self.attack_cooldown)
            self.attack = previous_attack
            self.attack_cooldown = previous_cooldown
            self.image = self.attack(runner.mouse_pos, runner.player.rect.center, runner.screen).image
        elif runner.secondary_pickup:
            previous_attack = runner.player.secondary_attack
            previous_cooldown = runner.player.secondary_attack_cooldown
            runner.player.set_attack(1, self.attack, self.attack_cooldown)
            self.attack = previous_attack
            self.attack_cooldown = previous_cooldown
            self.image = self.attack(runner.mouse_pos, runner.player.rect.center, runner.screen).image
