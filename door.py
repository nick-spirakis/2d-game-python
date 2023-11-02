import pygame
import os
from settings import *
from support import *
from timer import Timez

class Door(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, door_sprites):
        super().__init__(group)

        #animations
        self.import_assets()
        self.status = 'closed'
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.z = LAYERS['enemy']

        #collisions
        self.hitbox = self.rect.copy()  #inflate shrinks or grows the hitbox
        self.collision_sprites = collision_sprites
        
        #door
        self.door_sprites = door_sprites

 
    def import_assets(self):
        self.animations = {'closed': [], 'open': []}
        
        for animation in self.animations.keys():
            full_path = './Assets/door/' + animation
            self.animations[animation] = import_folder(full_path)
        #print(self.animations)


    def animate(self, dt):
        self.frame_index += 2 * dt #was +=4
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]


    def update(self, dt):
            self.animate(dt)