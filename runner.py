import pygame
import sys
import world
import random_world
import attacks
import player
import art
import random


class Runner:
    def __init__(self, fps, window_size, random_game=False):
        self.screen = pygame.display.set_mode(window_size)

        self.FPS = fps
        self.clock = pygame.time.Clock()
        self.running = True
        self.won_game = False
        self.has_map = True

        size = 40
        pos = [self.screen.get_width() / 2, self.screen.get_height() / 2]
        c1 = (73, 48, 199)
        c2 = (0, 0, 0)
        max_hp = 6
        speed = 6
        sprint_speed = 7.2
        max_stamina = 50
        sprint_decay = 25
        sprint_regen = 12
        attack1 = attacks.fireball
        attack1_cooldown = attacks.fireball_cooldown
        attack2 = attacks.earth
        attack2_cooldown = attacks.earth_cooldown
        self.player = player.Player(size, pos, c1, c2, max_hp, speed, sprint_speed, max_stamina, sprint_decay, sprint_regen, attack1, attack1_cooldown, attack2, attack2_cooldown)

        # declare world here
        if random_game:
            self.world = random_world.Simple(self, 8, 8)
        else:
            self.world = world.World1(self)

        # input
        self.primary_attack = False
        self.secondary_attack = False
        self.primary_pickup = False
        self.secondary_pickup = False
        self.mouse_pos = (0, 0)

        # art
        self.lose_screen = art.draw_lose_screen(self.screen)
        self.win_screen = art.draw_win_screen(self.screen)
        self.background = art.draw_background(self.screen)
        self.minimap = art.draw_minimap(self.screen, self.world.map, self.world.current_room, self.world.visited_rooms)

    def update_minimap_position(self):
        self.minimap = art.draw_minimap(self.screen, self.world.map, self.world.current_room, self.world.visited_rooms)

    def check_important_inputs(self):
        # check for the game turned off or escape
        primary_pickup, secondary_pickup = False, False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    primary_pickup = True
                if event.button == 3:
                    secondary_pickup = True

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # reset with r if game over
                if event.key == pygame.K_r:
                    if self.player.dead or self.won_game:
                        # essentially reruns the game since we have a while true loop in main
                        self.running = False
                if event.key == pygame.K_SPACE:
                    primary_pickup = True
                if event.key == pygame.K_c:
                    secondary_pickup = True

        return primary_pickup, secondary_pickup
    
    def get_input(self):
        player_direction = [0, 0]
        f = False

        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        mouse_pos = pygame.mouse.get_pos()

        primary_attack_keys = keys[pygame.K_SPACE] or mouse[0]
        secondary_attack_keys = keys[pygame.K_c] or mouse[2]
        sprint_keys = keys[pygame.K_LSHIFT] or keys[pygame.K_LCTRL]

        # attack input
        primary_attack = primary_attack_keys
        secondary_attack = secondary_attack_keys
        sprint_held = sprint_keys

        # movement input
        if keys[pygame.K_w]:
            player_direction[1] -= 1
        if keys[pygame.K_s]:
            player_direction[1] += 1
        if keys[pygame.K_a]:
            player_direction[0] -= 1
        if keys[pygame.K_d]:
            player_direction[0] += 1

        return player_direction, primary_attack, secondary_attack, mouse_pos, sprint_held

    def do_collision(self, sprinting):
        # player wall collision after horizontal
        self.player.move_horizontal(self.screen.get_rect(), sprinting, self.FPS)
        collided = pygame.sprite.groupcollide(self.world.current_room.walls, pygame.sprite.Group(self.player), False, False)
        for wall in collided.keys():
            wall.collide_player_horizontal(self.player)

        # player wall collision after vertical
        self.player.move_vertical(self.screen.get_rect(), sprinting, self.FPS)
        collided = pygame.sprite.groupcollide(self.world.current_room.walls, pygame.sprite.Group(self.player), False, False)
        for wall in collided.keys():
            wall.collide_player_vertical(self.player)

        # player powerup collision
        collided = pygame.sprite.groupcollide(self.world.current_room.powerups, pygame.sprite.Group(self.player), False, False)
        for powerup in collided.keys():
            powerup.on_interact(self)

        # update enemies horizontally
        for enemy in self.world.current_room.enemies: enemy.update_horizontal(self.screen.get_rect(), self.FPS)
        collided = pygame.sprite.groupcollide(self.world.current_room.walls, self.world.current_room.enemies, False, False)
        for wall in collided.keys():
            for enemy in collided[wall]:
                wall.collide_enemy_horizontal(enemy)

        # update enemies vertically
        for enemy in self.world.current_room.enemies: enemy.update_vertical(self.screen.get_rect(), self.FPS)
        collided = pygame.sprite.groupcollide(self.world.current_room.walls, self.world.current_room.enemies, False, False)
        for wall in collided.keys():
            for enemy in collided[wall]:
                wall.collide_enemy_vertical(enemy)

        # projectile collision + destroy
        self.player.projectiles.update(self.screen.get_rect(), self.FPS)
        pygame.sprite.groupcollide(self.world.current_room.walls, self.player.projectiles, False, True)

        # enemy projectile collision + destroy
        collided = pygame.sprite.groupcollide(self.world.current_room.enemies, self.player.projectiles, False, True)
        for enemy in collided.keys():
            for projectile in collided[enemy]:
                enemy.hitpoints -= projectile.damage

        # player enemy collision
        collided = pygame.sprite.groupcollide(pygame.sprite.Group(self.player), self.world.current_room.enemies, False, True)
        for player in collided.keys():
            for enemies in collided[player]:
                player.health -= 1

    def update(self):
        self.clock.tick(self.FPS)
        self.primary_pickup, self.secondary_pickup = self.check_important_inputs()
        if self.player.dead: return

        player_dir, self.primary_attack, self.secondary_attack, self.mouse_pos, sprinting = self.get_input()
        self.player.dir = player_dir

        self.world.update(self.player)
        self.player.update(self.primary_attack, self.secondary_attack, self.mouse_pos, self.screen, sprinting, self.FPS)
        
        self.do_collision(sprinting)

    def draw(self):
        # death screen
        if self.player.dead:
            self.screen.blit(self.lose_screen, (0, 0))
        # win screen
        elif self.won_game:
            self.screen.blit(self.win_screen, (0, 0))
        # normal game
        else:
            self.screen.blit(self.background, (0, 0))
            self.player.draw(self.screen)
            self.world.current_room.enemies.draw(self.screen)
            self.player.projectiles.draw(self.screen)
            self.world.draw(len(list(self.world.current_room.enemies)) == 0)
            if self.has_map: self.screen.blit(self.minimap, (0, 0))
            self.screen.blit(art.draw_hud(self.screen, self.player.max_health, self.player.health, self.player.max_stamina, self.player.stamina), (0, 0))

        pygame.display.update()
