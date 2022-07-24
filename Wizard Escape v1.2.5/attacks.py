import projectile
import numpy as np


fireball_cooldown = 3
def fireball(mouse_pos, player_pos, screen, fireball_damage=4, fireball_lifetime=100, fireball_size=30):
    m_pos = np.array(mouse_pos)
    p_pos = np.array(player_pos)
    velocity = 10 * (m_pos - p_pos) / np.linalg.norm(m_pos - p_pos)

    return projectile.Fireball(fireball_size, screen, p_pos, velocity, fireball_lifetime, fireball_damage)

ice_cooldown = 6
def ice(mouse_pos, player_pos, screen, ice_damage=3, ice_lifetime=100, ice_size=30):
    m_pos = np.array(mouse_pos)
    p_pos = np.array(player_pos)
    velocity = 10 * (m_pos - p_pos) / np.linalg.norm(m_pos - p_pos)

    return projectile.Ice(ice_size, screen, p_pos, velocity, ice_lifetime, ice_damage)   

earth_cooldown = 7
def earth(mouse_pos, player_pos, screen, earth_damage=5, earth_lifetime=10, earth_size=40):
    m_pos = np.array(mouse_pos)
    p_pos = np.array(player_pos)
    velocity = 10 * (m_pos - p_pos) / np.linalg.norm(m_pos - p_pos)
    
    return projectile.Earth(earth_size, screen, p_pos, velocity, earth_lifetime, earth_damage)
