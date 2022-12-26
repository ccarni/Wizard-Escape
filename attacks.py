import projectile
import numpy as np


fireball_cooldown = 3
def fireball(mouse_pos, player_pos, screen, fireball_damage=5, fireball_lifetime=100, fireball_size=30, speed=10):
    return create_projectile(mouse_pos, player_pos, screen, fireball_damage, fireball_lifetime, fireball_size, speed, projectile.Fireball)

ice_cooldown = 5
def ice(mouse_pos, player_pos, screen, ice_damage=8, ice_lifetime=120, ice_size=40, speed=10):
    return create_projectile(mouse_pos, player_pos, screen, ice_damage, ice_lifetime, ice_size, speed, projectile.Ice)

earth_cooldown = 7
def earth(mouse_pos, player_pos, screen, earth_damage=12, earth_lifetime=10, earth_size=40, speed=10):
    return create_projectile(mouse_pos, player_pos, screen, earth_damage, earth_lifetime, earth_size, speed, projectile.Earth)

wind_cooldown = 9
def wind(mouse_pos, player_pos, screen, wind_damage=15, wind_lifetime=20, wind_size=55, speed=10):
    return create_projectile(mouse_pos, player_pos, screen, wind_damage, wind_lifetime, wind_size, speed, projectile.Wind)

leaf_cooldown = 2
def leaf(mouse_pos, player_pos, screen, leaf_damage=4, leaf_lifetime=140, leaf_size=55, speed=10):
    return create_projectile(mouse_pos, player_pos, screen, leaf_damage, leaf_lifetime, leaf_size, speed, projectile.Leaf)

def create_projectile(mouse_pos, player_pos, screen, damage, lifetime, size, speed, projectile_type):
    m_pos = np.array(mouse_pos)
    p_pos = np.array(player_pos)
    velocity = speed * (m_pos - p_pos) / np.linalg.norm(m_pos - p_pos)

    return projectile_type(size, screen, p_pos, velocity, lifetime, damage)
