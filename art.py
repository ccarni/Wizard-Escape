import pygame
import math
import random


#ENEMIES
def draw_enemy(screen, size, color1=(255, 0, 0), color2=(0, 0, 0)):
    enemy_surf = pygame.Surface((screen.get_width() / 20, screen.get_width() / 20))
    enemy_surf.fill(color1)
    e_height = enemy_surf.get_height()
    e_width = enemy_surf.get_width()
    # eyes
    pygame.draw.circle(enemy_surf, color2, (e_width * 4 / 7, e_height / 3), e_height / 8)
    pygame.draw.circle(enemy_surf, color2, (e_width * 4 / 7, e_height * 2 / 3), e_height / 8)
    # mouth
    enemy_mouth = pygame.rect.Rect((e_width * 5 / 7, e_height / 5), (e_width * 2 / 7, e_height * 4 / 6))
    pygame.draw.polygon(enemy_surf, (255, 255, 255), (
    (e_width * 5 / 7, e_height * 5 / 10), (e_width * 5 / 7, e_height * 7 / 10),
    (e_width * 90 / 100, e_height * 13 / 20)))
    pygame.draw.polygon(enemy_surf, (255, 255, 255), (
    (e_width * 5 / 7, e_height * 5 / 10), (e_width * 11 / 14, e_height * 3 / 10),
    (e_width * 90 / 100, e_height * 9 / 20)))
    pygame.draw.arc(enemy_surf, color2, enemy_mouth, math.pi / 2, math.pi * 3 / 2, 3)
    # eyebrows
    pygame.draw.line(enemy_surf, color2, (e_width * 2 / 7, e_height / 6), (e_width * 4 / 7, e_height / 2), 3)
    pygame.draw.line(enemy_surf, color2, (e_width * 2 / 7, e_height * 5 / 6), (e_width * 4 / 7, e_height / 2), 3)
    enemy_surf = pygame.transform.smoothscale(enemy_surf, (size, size))
    return enemy_surf

#PLAYER
def player_rotate(surface, direction, last_direction):
        left = -90
        right = 90
        rotated_surface = surface
        if direction == [0, 0]:
            direction = last_direction

        if direction[0] == -1:
            rotated_surface = pygame.transform.rotate(surface, right * 2)
        elif direction == [0, 1]:
            rotated_surface = pygame.transform.rotate(surface, left)
        elif direction == [0, -1]:
            rotated_surface = pygame.transform.rotate(surface, right)
        #already looking right so we dont need to check it
        last_dir = direction
        return rotated_surface, last_dir

def draw_player(screen, size, color1, color2, direction, last_direction):
    #player draw function
        player_surf = pygame.Surface((screen.get_width() / 20, screen.get_width() / 20))
        player_surf.fill(color1)
        p_height = player_surf.get_height()
        p_width = player_surf.get_width()
        color3 = (62, 6, 145)
        color4 = (45, 2, 110)
        color5 = (191, 179, 42)
        # eyes
        pygame.draw.circle(player_surf, color2, (p_width * 5 / 7, p_height / 3), p_height / 8)
        pygame.draw.circle(player_surf, color2, (p_width * 5 / 7, p_height * 2 / 3), p_height / 8)
        # mouth
        pygame.draw.line(player_surf, color2, (p_width * 6 / 7, p_height / 3), (p_width * 6 / 7, p_height * 2 / 3), 2)
        # hat
        hat_rect = pygame.rect.Rect((p_width * 2 / 9, 0), (p_width / 2, p_height))
        pygame.draw.ellipse(player_surf, color3, hat_rect)
        pygame.draw.polygon(player_surf, color3, (
        (p_width * 3 / 100, p_height / 2), (p_width / 3, p_height / 5), (p_width / 3, p_height * 4 / 5)))
        pygame.draw.circle(player_surf, color4, (p_width * 5 / 100, p_height / 2), 3)
        pygame.draw.circle(player_surf, color5, (p_width * 3 / 5, p_height * 2 / 3), 1)
        pygame.draw.circle(player_surf, color5, (p_width / 3, p_height / 2), 1)
        pygame.draw.circle(player_surf, color5, (p_width / 3, p_height / 4), 1)
        pygame.draw.circle(player_surf, color5, (p_width / 2, p_height / 5), 1)
        pygame.draw.circle(player_surf, color5, (p_width / 3, p_height * 3 / 4), 1)
        pygame.draw.circle(player_surf, color5, (p_width / 2, p_height * 2 / 5), 1)
        pygame.draw.circle(player_surf, color5, (p_width / 3, p_height / 4), 1)
        player_surf, last_dir = player_rotate(player_surf, direction, last_direction)
        player_surf = pygame.transform.smoothscale(player_surf, (size, size))
        return player_surf, last_dir

#POWERUPS
def draw_heart(screen, size):
        heart_surf = pygame.Surface((screen.get_width() / 10, screen.get_width() / 10)).convert_alpha()
        heart_surf.fill((0, 0, 0, 0))
        h_height = heart_surf.get_height()
        h_width = heart_surf.get_width()
        pygame.draw.polygon(heart_surf, (240, 58, 58), (
        (h_width / 2, h_height * 7 / 10), (h_width / 8, h_height / 4), (h_width * 3 / 19, h_height / 8),
        (h_width / 3, h_height / 20), (h_width * 8 / 17, h_height / 8), (h_width * 2 / 3, h_height / 20),
        (h_width * 16 / 19, h_height / 8), (h_width * 56 / 65, h_height / 4)))
        pygame.draw.polygon(heart_surf, (196, 202, 206), (
        (h_width / 2, h_height * 7 / 10), (h_width / 8, h_height / 4), (h_width * 3 / 19, h_height / 8),
        (h_width / 3, h_height / 20), (h_width * 8 / 17, h_height / 8), (h_width * 2 / 3, h_height / 20),
        (h_width * 16 / 19, h_height / 8), (h_width * 56 / 65, h_height / 4)), 3)
        heart_surf = pygame.transform.smoothscale(heart_surf, (size, size))
        return heart_surf

def draw_empty_heart(screen, size):
    heart_surf = pygame.Surface((screen.get_width() / 10, screen.get_width() / 10)).convert_alpha()
    heart_surf.fill((0, 0, 0, 0))
    h_height = heart_surf.get_height()
    h_width = heart_surf.get_width()
    pygame.draw.polygon(heart_surf, (0, 0, 0), (
    (h_width / 2, h_height * 7 / 10), (h_width / 8, h_height / 4), (h_width * 3 / 19, h_height / 8),
    (h_width / 3, h_height / 20), (h_width * 8 / 17, h_height / 8), (h_width * 2 / 3, h_height / 20),
    (h_width * 16 / 19, h_height / 8), (h_width * 56 / 65, h_height / 4)))
    pygame.draw.polygon(heart_surf, (196, 202, 206), (
    (h_width / 2, h_height * 7 / 10), (h_width / 8, h_height / 4), (h_width * 3 / 19, h_height / 8),
    (h_width / 3, h_height / 20), (h_width * 8 / 17, h_height / 8), (h_width * 2 / 3, h_height / 20),
    (h_width * 16 / 19, h_height / 8), (h_width * 56 / 65, h_height / 4)), 3)
    heart_surf = pygame.transform.smoothscale(heart_surf, (size, size))
    return heart_surf

def draw_trophy(screen, size):
    trophy_surf = pygame.Surface((screen.get_width() / 10, screen.get_width() / 10)).convert_alpha()
    trophy_surf.fill((0,0,0,0))
    trophy_surf.set_colorkey((0,0,0))
    t_height = trophy_surf.get_height()
    t_width = trophy_surf.get_width()
    pygame.draw.polygon(trophy_surf, (255,215,0), ((t_width/4, t_height/9), (t_width * 3/ 4, t_height/9), (t_width * 74/ 100, t_height * 2/10), (t_width * 94/ 100, t_height * 2/10),(t_width * 97/ 100, t_height * 3/10),(t_width * 97/ 100, t_height * 4/10),(t_width * 74/ 100, t_height * 6/10), (t_width * 70/ 100, t_height * 7/10),(t_width * 64/ 100, t_height * 78/100), (t_width * 52/100, t_height * 78/100),(t_width * 52/100, t_height),(t_width * 48/100, t_height), (t_width * 48/100, t_height * 78/100),(t_width * 36/ 100, t_height * 78/100),(t_width * 30/ 100, t_height * 7/10),(t_width * 26/ 100, t_height * 6/10),(t_width * 3/ 100, t_height * 4/10),(t_width * 3/ 100, t_height * 3/10),(t_width * 6/ 100, t_height * 2/10),(t_width * 26/ 100, t_height * 2/10)))
    pygame.draw.polygon(trophy_surf, (12,0,0),((t_width * 78/ 100, t_height * 24/100),(t_width * 90/ 100, t_height * 24/100),(t_width * 93/ 100, t_height * 3/10),(t_width * 93/ 100, t_height * 4/10),(t_width * 78/ 100, t_height * 54/100)))
    pygame.draw.polygon(trophy_surf, (12,0,0),((t_width * 22/ 100, t_height * 24/100),(t_width * 10/ 100, t_height * 24/100),(t_width * 7/ 100, t_height * 3/10),(t_width * 7/ 100, t_height * 4/10),(t_width * 22/ 100, t_height * 54/100)))
    pygame.draw.polygon(trophy_surf, (102,51,0), ((t_width*.3,t_height), (t_width*.7,t_height), (t_width * .6, t_height*.9), (t_width* .4, t_height* .9)))
    trophy_surf = pygame.transform.smoothscale(trophy_surf, (size, size))
    return trophy_surf

#ATTACKS
def draw_fireball(screen, size):
        color1 = (219, 76, 20)
        color2 = (237, 176, 43)
        fire_surf = pygame.Surface((screen.get_width() / 20, screen.get_width() / 20))
        fire_surf.fill((0, 0, 0))
        f_height = fire_surf.get_height()
        f_width = fire_surf.get_width()
        pygame.draw.polygon(fire_surf, color2, ((0, f_height / 3),(f_width / 6, f_height / 3),(f_width / 10, f_height / 5),(f_width / 4, f_height / 5),(f_width / 5, f_height / 10),(f_width * 3 / 5, f_height / 8),(f_width * 4 / 5, f_height / 4),(f_width * 35 / 40, f_height / 2),(f_width * 4 / 5, f_height * 3 / 4),(f_width * 3 / 5, f_height * 7 / 8),(f_width / 5, f_height * 9 / 10),(f_width / 4, f_height * 4 / 5),(f_width / 10, f_height * 4 / 5),(f_width / 6, f_height * 2 / 3),(0, f_height * 2 / 3))) # this sure is a line of cose
        pygame.draw.circle(fire_surf, color1, (f_width / 2, f_height / 2), f_height / 3)
        fire_surf.set_colorkey((0, 0, 0))
        fire_surf = pygame.transform.smoothscale(fire_surf, (size, size))
        return fire_surf

def draw_ice(screen, size):
        ice_surf = pygame.Surface((screen.get_width() / 20, screen.get_width() / 20)).convert_alpha()
        ice_surf.fill((0, 0, 0, 0))
        i_height = ice_surf.get_height()
        i_width = ice_surf.get_width()
        pygame.draw.polygon(ice_surf, (109, 214, 252), ((i_width / 7, i_height / 9), (i_width * 6 / 10, i_height / 6), (i_width * 95 / 100, i_height * 4 / 10),(i_width / 3, i_height * 2 / 5)))
        pygame.draw.polygon(ice_surf, (74, 171, 207), ((i_width / 7, i_height * 6 / 9), (i_width * 4 / 10, i_height * 4 / 6), (i_width * 95 / 100, i_height * 4 / 10),(i_width / 3, i_height * 2 / 5)))
        pygame.draw.polygon(ice_surf, (20, 91, 117), ((i_width / 7, i_height / 9), (i_width / 3, i_height * 2 / 5), (i_width / 7, i_height * 6 / 9),(i_width / 100, i_height * 2 / 5)))
        ice_surf = pygame.transform.smoothscale(ice_surf, (size, size))
        return ice_surf

def draw_earth(screen, size):
        earth_surf = pygame.Surface((screen.get_width() / 20, screen.get_width() / 20)).convert_alpha()
        earth_surf.fill((0, 0, 0, 0))
        e_height = earth_surf.get_height()
        e_width = earth_surf.get_width()
        pygame.draw.circle(earth_surf, (59, 36, 1), (e_width * 4 / 6, e_height / 2), e_width / 3)
        pygame.draw.circle(earth_surf, (82, 56, 16), (e_width * 2 / 6, e_height / 2), e_width / 3)
        pygame.draw.circle(earth_surf, (107, 81, 40), (0, e_height / 2), e_width / 3)
        earth_surf = pygame.transform.smoothscale(earth_surf, (size, size))
        return earth_surf

def draw_background(screen):
    background_surf = pygame.Surface(screen.get_size())
    background_surf.fill((62, 62, 62))
    s_height = background_surf.get_height()
    s_width = background_surf.get_width()
    for i in range(600):
        floor_rect = pygame.rect.Rect((random.randint(int(s_width / 50), int(s_height * 49 / 50)), random.randint(int(s_width / 50), int(s_height * 49 / 50))), (s_width / 90, s_height / 50))
        pygame.draw.ellipse(background_surf, (90, 90, 90), floor_rect)
    return background_surf

def draw_hud(screen, max_health, health, heart_size=50):
    hud = pygame.surface.Surface(screen.get_size())
    for i in range(max_health):
        if (health - 1) >= i:
            heart = draw_heart(screen, heart_size)
        else:
            heart = draw_empty_heart(screen, heart_size)
        hud.blit(heart, (i * heart.get_width(), screen.get_height() - heart.get_height()))
        hud.set_colorkey((0, 0, 0))
    return hud


#SCREENS
def draw_lose_screen(screen, color1=(73, 48, 199), color2=(0, 0, 0)):
    lose_surf = pygame.Surface((screen.get_width(), screen.get_height())).convert_alpha()
    lose_surf.fill((0, 0, 0))
    hat_surf = pygame.Surface((screen.get_width() / 10, screen.get_height() / 10)).convert_alpha()
    hat_surf.fill((0, 0, 0))
    color3 = (62, 6, 145)
    color4 = (45, 2, 110)
    color5 = (191, 179, 42)
    h_height = hat_surf.get_height()
    h_width = hat_surf.get_width()
    y = draw_y(lose_surf)
    o = draw_o(lose_surf)
    u = draw_u(lose_surf)
    l = draw_l(lose_surf)
    s = draw_s(lose_surf)
    e = draw_e(lose_surf)
    lose_surf.blit(y, (0, 50))
    lose_surf.blit(o, (100, 50))
    lose_surf.blit(u, (200, 50))
    lose_surf.blit(l, (400, 50))
    lose_surf.blit(o, (500, 50))
    lose_surf.blit(s, (600, 50))
    lose_surf.blit(e, (700, 50))
    hat_rect = pygame.rect.Rect((h_width * 2 / 9, 0), (h_width / 2, h_height))
    pygame.draw.ellipse(hat_surf, color3, hat_rect)
    pygame.draw.polygon(hat_surf, color3, (
        (h_width * 3 / 100, h_height / 2), (h_width / 3, h_height / 5), (h_width / 3, h_height * 4 / 5)))
    pygame.draw.circle(hat_surf, color4, (h_width * 5 / 100, h_height / 2), 3)
    pygame.draw.circle(hat_surf, color5, (h_width * 3 / 5, h_height * 2 / 3), 1)
    pygame.draw.circle(hat_surf, color5, (h_width / 3, h_height / 2), 1)
    pygame.draw.circle(hat_surf, color5, (h_width / 3, h_height / 4), 1)
    pygame.draw.circle(hat_surf, color5, (h_width / 2, h_height / 5), 1)
    pygame.draw.circle(hat_surf, color5, (h_width / 3, h_height * 3 / 4), 1)
    pygame.draw.circle(hat_surf, color5, (h_width / 2, h_height * 2 / 5), 1)
    pygame.draw.circle(hat_surf, color5, (h_width / 3, h_height / 4), 1)

    player_spotlight_box = pygame.rect.Rect(270, 450, 250, 70)
    player_body = pygame.rect.Rect(300, 300, 200, 200)
    player_mouth = pygame.rect.Rect(350, 350, 10, 100)
    player_l_tears = pygame.rect.Rect(460, 340, 15, 140)
    player_r_tears = pygame.rect.Rect(460, 440, 15, 70)
    pygame.draw.ellipse(lose_surf, (255, 255, 255), player_spotlight_box)
    pygame.draw.rect(lose_surf, color1, player_body)
    pygame.draw.rect(lose_surf, (40, 203, 224), player_l_tears)
    pygame.draw.rect(lose_surf, (40, 203, 224), player_r_tears)
    pygame.draw.rect(lose_surf, color2, player_mouth)
    pygame.draw.circle(lose_surf, color2, (465, 340), 20)
    pygame.draw.circle(lose_surf, color2, (465, 440), 20)
    hat_surf = pygame.transform.rotate(hat_surf, 270)
    hat_surf = pygame.transform.scale(hat_surf, (150, 150))
    lose_surf.blit(hat_surf, (530, 390))
    font = pygame.font.Font(None, 40)
    text_surf = font.render('Press R to Restart', True, (255, 255, 255))
    lose_surf.blit(text_surf, (200, 650))
    return lose_surf


def draw_win_screen(screen, color1=(73, 48, 199), color2=(0, 0, 0)):
    win_surf = pygame.Surface((screen.get_width(), screen.get_height())).convert_alpha()
    win_surf.fill((0, 0, 0))
    hat_surf = pygame.Surface((screen.get_width() / 10, screen.get_height() / 10)).convert_alpha()
    hat_surf.fill((0, 0, 0, 0))
    color3 = (62, 6, 145)
    color4 = (45, 2, 110)
    color5 = (191, 179, 42)
    h_height = hat_surf.get_height()
    h_width = hat_surf.get_width()
    y = draw_y(win_surf)
    o = draw_o(win_surf)
    u = draw_u(win_surf)
    w = draw_w(win_surf)
    i = draw_i(win_surf)
    n = draw_n(win_surf)
    win_surf.blit(y, (50, 50))
    win_surf.blit(o, (150, 50))
    win_surf.blit(u, (250, 50))
    win_surf.blit(w, (400, 50))
    win_surf.blit(i, (500, 50))
    win_surf.blit(n, (600, 50))
    hat_rect = pygame.rect.Rect((h_width * 2 / 9, 0), (h_width / 5, h_height))
    pygame.draw.ellipse(hat_surf, color3, hat_rect)
    pygame.draw.polygon(hat_surf, color3, (
        (h_width * 3 / 100, h_height / 2), (h_width / 3, h_height / 5), (h_width / 3, h_height * 4 / 5)))
    pygame.draw.circle(hat_surf, color4, (h_width * 5 / 100, h_height / 2), 3)
    pygame.draw.circle(hat_surf, color5, (h_width / 5, h_height * 2 / 3), 1)
    pygame.draw.circle(hat_surf, color5, (h_width * 2 / 6, h_height / 2), 1)
    pygame.draw.circle(hat_surf, color5, (h_width / 3, h_height / 4), 1)
    pygame.draw.circle(hat_surf, color5, (h_width * 2 / 7, h_height / 5), 1)
    pygame.draw.circle(hat_surf, color5, (h_width / 3, h_height * 3 / 4), 1)
    pygame.draw.circle(hat_surf, color5, (h_width / 5, h_height * 2 / 5), 1)
    pygame.draw.circle(hat_surf, color5, (h_width / 3, h_height / 4), 1)

    player_spotlight_box = pygame.rect.Rect(270, 450, 250, 70)
    player_smile_box = pygame.rect.Rect(380, 380, 40, 30)

    player_body = pygame.rect.Rect(300, 300, 200, 200)
    pygame.draw.ellipse(win_surf, (255, 255, 255), player_spotlight_box)
    pygame.draw.rect(win_surf, color1, player_body)
    pygame.draw.circle(win_surf, color2, (465, 340), 20)
    pygame.draw.circle(win_surf, color2, (365, 340), 20)
    pygame.draw.arc(win_surf, color2, player_smile_box, math.pi, 0, 3)
    hat_surf = pygame.transform.rotate(hat_surf, 270)
    hat_surf = pygame.transform.scale(hat_surf, (150, 150))
    win_surf.blit(hat_surf, (330, 250))
    font = pygame.font.Font(None, 40)
    text_surf = font.render('Press R to Restart', True, (255, 255, 255))


    win_surf.blit(text_surf, (200, 650))
    return win_surf


def draw_y(screen):
    y_surf = pygame.Surface((screen.get_width() / 10, screen.get_height() / 10)).convert_alpha()
    y_surf.fill((0, 0, 0, 0))
    y_width = y_surf.get_width()
    y_height = y_surf.get_height()
    pygame.draw.polygon(y_surf, (255, 255, 255), (
    (y_width * 3 / 20, 0), (y_width / 2, y_height / 3), (y_width * 17 / 20, 0), (y_width, y_height / 10),
    (y_width * 6 / 10, y_height / 2), (y_width * 6 / 10, y_height), (y_width * 4 / 10, y_height),
    (y_width * 4 / 10, y_height / 2), (0, y_height / 10),))
    return y_surf


def draw_o(screen):
    o_surf = pygame.Surface((screen.get_width() / 10, screen.get_height() / 10)).convert_alpha()
    o_surf.fill((0, 0, 0, 0))
    o_surf.set_colorkey((133, 0, 0))
    o_width = o_surf.get_width()
    o_height = o_surf.get_height()
    o_body = pygame.rect.Rect(0, 0, o_width, o_height)
    o_center = pygame.rect.Rect(o_width * .3, o_height * .3, o_width * .4, o_height * .4)
    pygame.draw.rect(o_surf, (255, 255, 255), o_body)
    pygame.draw.rect(o_surf, (133, 0, 0), o_center)
    return o_surf


def draw_u(screen):
    u_surf = pygame.Surface((screen.get_width() / 10, screen.get_height() / 10)).convert_alpha()
    u_surf.fill((0, 0, 0, 0))
    u_surf.set_colorkey((133, 0, 0))
    u_width = u_surf.get_width()
    u_height = u_surf.get_height()
    u_body = pygame.rect.Rect(0, 0, u_width, u_height)
    u_center = pygame.rect.Rect(u_width * .3, 0, u_width * .4, u_height * .8)
    pygame.draw.rect(u_surf, (255, 255, 255), u_body)
    pygame.draw.rect(u_surf, (133, 0, 0), u_center)
    return u_surf


def draw_w(screen):
    w_surf = pygame.Surface((screen.get_width() / 10, screen.get_height() / 10)).convert_alpha()
    w_surf.fill((0, 0, 0, 0))
    w_width = w_surf.get_width()
    w_height = w_surf.get_height()
    w_body = pygame.rect.Rect(0, 0, w_width, w_height)
    w_center1 = pygame.rect.Rect(w_width * .15, w_height * .1, w_width * .9, w_height * .3)
    w_center2 = pygame.rect.Rect(w_width * .15, w_height * .6, w_width * .9, w_height * .3)
    pygame.draw.rect(w_surf, (255, 255, 255), w_body)
    pygame.draw.rect(w_surf, (133, 0, 0), w_center1)
    pygame.draw.rect(w_surf, (133, 0, 0), w_center2)
    w_surf = pygame.transform.rotate(w_surf, 90)
    w_surf.set_colorkey((133, 0, 0))
    return w_surf


def draw_i(screen):
    i_surf = pygame.Surface((screen.get_width() / 10, screen.get_height() / 10)).convert_alpha()
    i_surf.fill((0, 0, 0, 0))
    i_width = i_surf.get_width()
    i_height = i_surf.get_height()
    i_body = pygame.rect.Rect(i_width * .4, i_height * 2 / 5, i_width * .2, i_height)
    i_dot = pygame.rect.Rect(i_width * .4, 0, i_height * .2, i_height * .2)
    pygame.draw.rect(i_surf, (255, 255, 255), i_body)
    pygame.draw.rect(i_surf, (255, 255, 255), i_dot)
    return i_surf


def draw_n(screen):
    n_surf = pygame.Surface((screen.get_width() / 10, screen.get_height() / 10)).convert_alpha()
    n_surf.fill((0, 0, 0, 0))
    n_width = n_surf.get_width()
    n_height = n_surf.get_height()
    n_body = pygame.rect.Rect(0, 0, n_width, n_height)
    n_center1 = pygame.rect.Rect(0, n_height * .2, n_width * .9, n_height * .6)
    pygame.draw.rect(n_surf, (255, 255, 255), n_body)
    pygame.draw.rect(n_surf, (133, 0, 0), n_center1)
    n_surf = pygame.transform.rotate(n_surf, 90)
    n_surf.set_colorkey((133, 0, 0))
    return n_surf


def draw_l(screen):
    l_surf = pygame.Surface((screen.get_width() / 10, screen.get_height() / 10)).convert_alpha()
    l_surf.fill((0, 0, 0, 0))
    l_surf.set_colorkey((133, 0, 0))
    l_width = l_surf.get_width()
    l_height = l_surf.get_height()
    l_body = pygame.rect.Rect(0, 0, l_width, l_height)
    l_center = pygame.rect.Rect(l_width * .3, 0, l_width, l_height * .8)
    pygame.draw.rect(l_surf, (255, 255, 255), l_body)
    pygame.draw.rect(l_surf, (133, 0, 0), l_center)
    return l_surf


def draw_s(screen):
    s_surf = pygame.Surface((screen.get_width() / 10, screen.get_height() / 10)).convert_alpha()
    s_surf.fill((0, 0, 0, 0))
    s_surf.set_colorkey((133, 0, 0))
    s_width = s_surf.get_width()
    s_height = s_surf.get_height()
    s_body = pygame.rect.Rect(0, 0, s_width, s_height)
    s_center1 = pygame.rect.Rect(s_width * .3, s_height * .1, s_width * .8, s_height * .3)
    s_center2 = pygame.rect.Rect(0, s_height * .6, s_width * .8, s_height * .3)
    pygame.draw.rect(s_surf, (255, 255, 255), s_body)
    pygame.draw.rect(s_surf, (133, 0, 0), s_center1)
    pygame.draw.rect(s_surf, (133, 0, 0), s_center2)
    return s_surf


def draw_e(screen):
    e_surf = pygame.Surface((screen.get_width() / 10, screen.get_height() / 10)).convert_alpha()
    e_surf.fill((0, 0, 0, 0))
    e_surf.set_colorkey((133, 0, 0))
    e_width = e_surf.get_width()
    e_height = e_surf.get_height()
    e_body = pygame.rect.Rect(0, 0, e_width, e_height)
    e_center1 = pygame.rect.Rect(e_width * .3, e_height * .1, e_width * .8, e_height * .3)
    e_center2 = pygame.rect.Rect(e_width * .3, e_height * .6, e_width * .8, e_height * .3)
    pygame.draw.rect(e_surf, (255, 255, 255), e_body)
    pygame.draw.rect(e_surf, (133, 0, 0), e_center1)
    pygame.draw.rect(e_surf, (133, 0, 0), e_center2)
    return e_surf

#gross code dont touch
def draw_title_screen(screen):
    def draw_player(screen, color1=(73, 48, 199), color2=(0, 0, 0)):
        player_surf = pygame.Surface((screen.get_width() / 20, screen.get_width() / 20))
        player_surf.fill(color1)
        color3 = (62, 6, 145)
        color4 = (45, 2, 110)
        color5 = (191, 179, 42)
        p_height = player_surf.get_height()
        p_width = player_surf.get_width()
        # eyes
        pygame.draw.circle(player_surf, color2, (p_width * 5 / 7, p_height / 3), p_height / 8)
        pygame.draw.circle(player_surf, color2, (p_width * 5 / 7, p_height * 2 / 3), p_height / 8)
        # hat
        hat_rect = pygame.rect.Rect((p_width * 2 / 9, 0), (p_width / 2, p_height))
        pygame.draw.ellipse(player_surf, color3, hat_rect)
        pygame.draw.polygon(player_surf, color3, (
        (p_width * 3 / 100, p_height / 2), (p_width / 3, p_height / 5), (p_width / 3, p_height * 4 / 5)))
        pygame.draw.circle(player_surf, color4, (p_width * 5 / 100, p_height / 2), 3)
        pygame.draw.circle(player_surf, color5, (p_width * 3 / 5, p_height * 2 / 3), 1)
        pygame.draw.circle(player_surf, color5, (p_width / 3, p_height / 2), 1)
        pygame.draw.circle(player_surf, color5, (p_width / 3, p_height / 4), 1)
        pygame.draw.circle(player_surf, color5, (p_width / 2, p_height / 5), 1)
        pygame.draw.circle(player_surf, color5, (p_width / 3, p_height * 3 / 4), 1)
        pygame.draw.circle(player_surf, color5, (p_width / 2, p_height * 2 / 5), 1)
        pygame.draw.circle(player_surf, color5, (p_width / 3, p_height / 4), 1)

        # mouth
        pygame.draw.line(player_surf, color2, (p_width * 6 / 7, p_height / 3), (p_width * 6 / 7, p_height * 2 / 3),
                        2)

        return player_surf

    def draw_enemy(screen, color1=(255, 0, 0), color2=(0, 0, 0)):
        enemy_surf = pygame.Surface((screen.get_width() / 20, screen.get_width() / 20))
        enemy_surf.fill(color1)
        e_height = enemy_surf.get_height()
        e_width = enemy_surf.get_width()
        # eyes
        pygame.draw.circle(enemy_surf, color2, (e_width * 4 / 7, e_height / 3), e_height / 8)
        pygame.draw.circle(enemy_surf, color2, (e_width * 4 / 7, e_height * 2 / 3), e_height / 8)
        # mouth
        enemy_mouth = pygame.rect.Rect((e_width * 5 / 7, e_height / 5), (e_width * 2 / 7, e_height * 4 / 6))
        pygame.draw.polygon(enemy_surf, (255, 255, 255), (
        (e_width * 5 / 7, e_height * 5 / 10), (e_width * 5 / 7, e_height * 7 / 10),
        (e_width * 90 / 100, e_height * 13 / 20)))
        pygame.draw.polygon(enemy_surf, (255, 255, 255), (
        (e_width * 5 / 7, e_height * 5 / 10), (e_width * 11 / 14, e_height * 3 / 10),
        (e_width * 90 / 100, e_height * 9 / 20)))
        pygame.draw.arc(enemy_surf, color2, enemy_mouth, math.pi / 2, math.pi * 3 / 2, 3)
        # eyebrows
        pygame.draw.line(enemy_surf, color2, (e_width * 2 / 7, e_height / 6), (e_width * 4 / 7, e_height / 2), 3)
        pygame.draw.line(enemy_surf, color2, (e_width * 2 / 7, e_height * 5 / 6), (e_width * 4 / 7, e_height / 2),
                        3)
        return enemy_surf

    def draw_earth(screen):
        earth_surf = pygame.Surface((screen.get_width() / 20, screen.get_width() / 20)).convert_alpha()
        earth_surf.fill((0, 0, 0, 0))
        e_height = earth_surf.get_height()
        e_width = earth_surf.get_width()
        pygame.draw.circle(earth_surf, (59, 36, 1), (e_width * 4 / 6, e_height / 2), e_width / 3)
        pygame.draw.circle(earth_surf, (82, 56, 16), (e_width * 2 / 6, e_height / 2), e_width / 3)
        pygame.draw.circle(earth_surf, (107, 81, 40), (0, e_height / 2), e_width / 3)

        return earth_surf

    def draw_fireball(screen):
        color1 = (219, 76, 20)
        color2 = (237, 176, 43)
        fire_surf = pygame.Surface((screen.get_width() / 20, screen.get_width() / 20)).convert_alpha()
        fire_surf.fill((0, 0, 0, 0))
        f_height = fire_surf.get_height()
        f_width = fire_surf.get_width()
        pygame.draw.polygon(fire_surf, color2, ((0, f_height / 3),
                                                (f_width / 6, f_height / 3),
                                                (f_width / 10, f_height / 5),
                                                (f_width / 4, f_height / 5),
                                                (f_width / 5, f_height / 10),
                                                (f_width * 3 / 5, f_height / 8),
                                                (f_width * 4 / 5, f_height / 4),
                                                (f_width * 35 / 40, f_height / 2),
                                                (f_width * 4 / 5, f_height * 3 / 4),
                                                (f_width * 3 / 5, f_height * 7 / 8),
                                                (f_width / 5, f_height * 9 / 10),
                                                (f_width / 4, f_height * 4 / 5),
                                                (f_width / 10, f_height * 4 / 5),
                                                (f_width / 6, f_height * 2 / 3),
                                                (0, f_height * 2 / 3)
                                                ))
        pygame.draw.circle(fire_surf, color1, (f_width / 2, f_height / 2), f_height / 3)
        return fire_surf

    #unused since ice was removed during development
    # def draw_ice(screen):
    #     ice_surf = pygame.Surface((screen.get_width() / 20, screen.get_width() / 20)).convert_alpha()
    #     ice_surf.fill((0, 0, 0, 0))
    #     i_height = ice_surf.get_height()
    #     i_width = ice_surf.get_width()
    #     pygame.draw.polygon(ice_surf, (109, 214, 252), (
    #     (i_width / 7, i_height / 9), (i_width * 6 / 10, i_height / 6), (i_width * 95 / 100, i_height * 4 / 10),
    #     (i_width / 3, i_height * 2 / 5)))
    #     pygame.draw.polygon(ice_surf, (74, 171, 207), (
    #     (i_width / 7, i_height * 6 / 9), (i_width * 4 / 10, i_height * 4 / 6),
    #     (i_width * 95 / 100, i_height * 4 / 10), (i_width / 3, i_height * 2 / 5)))
    #     pygame.draw.polygon(ice_surf, (20, 91, 117), (
    #     (i_width / 7, i_height / 9), (i_width / 3, i_height * 2 / 5), (i_width / 7, i_height * 6 / 9),
    #     (i_width / 100, i_height * 2 / 5)))

    #     return ice_surf

    title_surf = pygame.Surface((screen.get_width(), screen.get_height())).convert_alpha()
    title_surf.fill((0, 0, 0))
    title_font = pygame.font.Font(None, 100)
    slightly_less_title_font = pygame.font.Font(None, 70)

    text_font = pygame.font.Font(None, 30)
    title = title_font.render('Magic Escape', True, (255, 255, 255))
    text_surf1 = text_font.render(
        'You have been selected by the WC Tribunal to find an artifact inside a ruin.', True, (255, 255, 255))
    text_surf2 = text_font.render('As you traverse the ruins, you find yourself trapped with no way out!', True,
                                (255, 255, 255))
    text_surf3 = text_font.render('However, you choose to bravely continue and find the artifact.', True,
                                (255, 255, 255))
    text_surf4 = text_font.render('You ready your fireballs..... and immediately blackout.', True,
                                (255, 255, 255))
    text_surfplayer1 = text_font.render('This is you! ', True, (255, 255, 255))
    text_surfplayer2 = text_font.render('Move with WASD. ', True, (255, 255, 255))
    text_surfenemy1 = text_font.render('This is an Enemy! ', True, (255, 255, 255))
    text_surfenemy2 = text_font.render('When they touch you, you lose health. ', True, (255, 255, 255))
    text_surffire1 = text_font.render('This is a Fireball! ', True, (255, 255, 255))
    text_surffire2 = text_font.render('Fire with left click. ', True, (255, 255, 255))
    text_surfspell1 = text_font.render('These are Secondary Spells! ', True, (255, 255, 255))
    text_surfspell2 = text_font.render('Fire with right click.', True, (255, 255, 255))
    text_surfspell3 = text_font.render('These are found in the ruins.', True, (255, 255, 255))
    text_surfstart = slightly_less_title_font.render('Press ENTER to start the game!', True, (255, 255, 255))

    title_surf.blit(text_surf1, (40, 100))
    title_surf.blit(text_surf2, (40, 150))
    title_surf.blit(text_surf3, (40, 200))
    title_surf.blit(text_surf4, (40, 250))
    title_surf.blit(draw_player(title_surf, (73, 48, 199)), (40, 350))
    title_surf.blit(text_surfplayer1, (90, 350))
    title_surf.blit(text_surfplayer2, (90, 380))
    title_surf.blit(draw_enemy(title_surf), (300, 350))
    title_surf.blit(text_surfenemy1, (350, 350))
    title_surf.blit(text_surfenemy2, (350, 380))
    title_surf.blit(draw_fireball(title_surf), (40, 410))
    title_surf.blit(text_surffire1, (90, 410))
    title_surf.blit(text_surffire2, (90, 440))
    title_surf.blit(draw_earth(title_surf), (310, 410))
    title_surf.blit(text_surfspell1, (360, 410))
    title_surf.blit(text_surfspell2, (360, 440))
    title_surf.blit(text_surfspell3, (360, 470))
    title_surf.blit(text_surfstart, (40, 600))

    title_surf.blit(title, (150, 0))

    return title_surf
