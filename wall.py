import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image.copy()
        self.rect = image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def collide_player_horizontal(self, player):
        # Collide with left side
        if player.rect.right > self.rect.left and player.dir[0] == 1:
            player.rect.right = self.rect.left
        # Collide with right side
        elif player.rect.left < self.rect.right and player.dir[0] == -1:
            player.rect.left = self.rect.right

    def collide_player_vertical(self, player, **kwargs):
        # Collide on top
        if player.rect.bottom > self.rect.top and player.dir[1] == 1:
            player.rect.bottom = self.rect.top
        # Collide on bottom
        elif player.rect.top < self.rect.bottom and player.dir[1] == -1:
            player.rect.top = self.rect.bottom

    def collide_enemy_horizontal(self, enemy):
        # Collide with left side
        if enemy.rect.right > self.rect.left and enemy.v[0] > 0:
            enemy.rect.right = self.rect.left
        # Collide with right side
        elif enemy.rect.left < self.rect.right and enemy.v[0] < 0:
            enemy.rect.left = self.rect.right

    def collide_enemy_vertical(self, enemy, **kwargs):
        # Collide on top
        if enemy.rect.bottom > self.rect.top and enemy.v[1] > 0:
            enemy.rect.bottom = self.rect.top
        # Collide on bottom
        elif enemy.rect.top < self.rect.bottom and enemy.v[1] < 0:
            enemy.rect.top = self.rect.bottom
