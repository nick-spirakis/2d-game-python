from pygame.math import Vector2
import pygame

#screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

TILE_SIZE = 32 #64

OVERLAY_POSITIONS = {
    'item': (40, SCREEN_HEIGHT - 15),
    'seed': (70, SCREEN_HEIGHT - 5)}

PLAYER_TOOL_OFFSET = { #sword hitbox
    'left': Vector2(-16,13), # (-20,0)
    'right': Vector2(24, 13), #(20,0)
    'up': Vector2(0,-20), #(0,-20)
    'down': Vector2(0,20) #(0, 20)
}

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ITEM_BOX_SIZE = 80

# colors 
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
HEALTH_COLOR = 'red'
UI_BORDER_COLOR_ACTIVE = 'gold'


#enemy
enemy_data = {
    'green_helmet': {'health': 1, 'exp': 100, 'damage': 10, 
                     'attack_type': 'punch', 'attack_sound': 'Audio/attack/spit.wav', 'speed': 100, 'resistance': 3, 
                     'attack_radius': 50, 'notice_radius': 300},

    'brute': {'health': 1 , 'exp': 150, 'damage': 15, 
                     'attack_type': 'beam', 'attack_sound': 'Audio/attack/spit.wav', 'speed': 80, 'resistance': 5, 
                     'attack_radius': 20, 'notice_radius': 50}
}

LAYERS = {
    'water': 0,
    'ground': 1,
    'border': 8,
    'rock backgrounds': 3,
    'rain floor': 4,
    'enemy': 5,
    'ground plant': 6,
    'rocks, land': 7,
    'main': 8,
    
    'house top': 9,
    'fruit': 10,
    'rain drops': 11,
}
