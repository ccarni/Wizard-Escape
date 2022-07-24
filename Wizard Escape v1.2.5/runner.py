import pygame
import sys
import world
import player
import art


class Runner():
    def __init__(self):
        #screen stuff
        window_height = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((window_height.get_height(), window_height.get_height()))
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        self.player = player.Player((255, 255, 255), [self.screen.get_width() / 2, self.screen.get_height() / 2])
        self.world = world.World1(self)

        self.FPS = 30
        self.clock = pygame.time.Clock()
        self.running = True
        self.won_game = False

        self.primary_attack = False
        self.secondary_attack = False
        self.primary_attack_down = False
        self.secondary_attack_down = False

        self.lose_screen = art.draw_lose_screen(self.screen)
        self.win_screen = art.draw_win_screen(self.screen)
        self.background = art.draw_background(self.screen)
    
    def important_inputs(self):
        #check for the game turned off or escape
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                #reset with r if game over
                if event.key == pygame.K_r:
                    if self.player.dead or self.won_game:
                        #essentially reruns the game since we have a while true loop in main
                        self.running = False
    
    def get_input(self):
        player_direction = [0, 0]
        primary_attack = False
        secondary_attack = False
        primary_down = False
        secondary_down = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    primary_down = True
                elif event.button == 2:
                    secondary_down = True

        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        #attack input
        if keys[pygame.K_SPACE] or keys[pygame.K_e] or mouse[0]:
            primary_attack = True
        if keys[pygame.K_SPACE] or keys[pygame.K_e] or mouse[2]:
            secondary_attack= True

        #movement input
        if keys[pygame.K_w]:
            player_direction[1] -= 1
        if keys[pygame.K_s]:
            player_direction[1] += 1
        if keys[pygame.K_a]:
            player_direction[0] -= 1
        if keys[pygame.K_d]:
            player_direction[0] += 1
        
        return player_direction, primary_attack, secondary_attack, primary_down, secondary_down, mouse_pos, 

    def do_collision(self):
        # player wall collision after horizontal
        self.player.move_horizontal(self.screen.get_rect())
        collided = pygame.sprite.groupcollide(self.world.current_room.walls, pygame.sprite.Group(self.player), False, False)
        for wall in collided.keys():
            wall.collide_player_horizontal(self.player)

        # player wall collision after vertical
        self.player.move_vertical(self.screen.get_rect())
        collided = pygame.sprite.groupcollide(self.world.current_room.walls, pygame.sprite.Group(self.player), False, False)
        for wall in collided.keys():
            wall.collide_player_vertical(self.player)

        # player powerup collision
        collided = pygame.sprite.groupcollide(self.world.current_room.powerups, pygame.sprite.Group(self.player), False, False)
        for powerup in collided.keys():
            powerup.on_interact(self)

        # update enemies horizontally
        for enemy in self.world.current_room.enemies: enemy.update_horizontal(self.screen.get_rect())
        collided = pygame.sprite.groupcollide(self.world.current_room.walls, self.world.current_room.enemies, False, False)
        for wall in collided.keys():
            for enemy in collided[wall]:
                wall.collide_enemy_horizontal(enemy)

        # update enemies vertically
        for enemy in self.world.current_room.enemies: enemy.update_vertical(self.screen.get_rect())
        collided = pygame.sprite.groupcollide(self.world.current_room.walls, self.world.current_room.enemies, False, False)
        for wall in collided.keys():
            for enemy in collided[wall]:
                wall.collide_enemy_vertical(enemy)

        # projectile collision + destroy
        self.player.projectiles.update(self.screen.get_rect())
        pygame.sprite.groupcollide(self.world.current_room.walls, self.player.projectiles, False, True)

        # enemy projectile collision + destroy
        collided = pygame.sprite.groupcollide(self.world.current_room.enemies, self.player.projectiles, False, True)
        for enemy in collided.keys():
            for projectile in collided[enemy]:
                enemy.hitpoints -= projectile.damage

        #player enemy collision
        collided = pygame.sprite.groupcollide(pygame.sprite.Group(self.player), self.world.current_room.enemies, False, True)
        for player in collided.keys():
            for enemies in collided[player]:
                player.health -= 1
                print(player.health)

    def update(self):
        self.important_inputs()
        if self.player.dead: return
        self.clock.tick(self.FPS)

        player_dir, self.primary_attack, self.secondary_attack, self.primary_attack_down, self.secondary_attack_down, mouse_pos = self.get_input()
        self.player.dir = player_dir

        self.world.update(self.player)
        self.player.update(self.primary_attack, self.secondary_attack, mouse_pos, self.screen)
        
        self.do_collision()

    def draw(self):
        #death screen
        if self.player.dead:
            self.screen.blit(self.lose_screen, (0, 0))
        #win screen
        elif self.won_game:
            self.screen.blit(self.win_screen, (0, 0))
        #normal game
        else:
            self.screen.blit(self.background, (0, 0))
            self.player.draw(self.screen)
            self.world.current_room.enemies.draw(self.screen)
            self.player.projectiles.draw(self.screen)
            self.world.draw(len(list(self.world.current_room.enemies)) == 0)
            self.screen.blit(art.draw_hud(self.screen, self.player.max_health, self.player.health), (0, 0))

        pygame.display.update()
