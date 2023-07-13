import pygame
import os
from settings import *
from support import *
from timer import Timez

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, attack_sprites):
        super().__init__(group)

        #animations
        self.import_assets()
        self.status = 'down'
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.z = LAYERS['enemy']

        #collisions
        self.hitbox = self.rect.copy()  #inflate shrinks or grows the hitbox
        self.collision_sprites = collision_sprites
        #attack
        self.attack_sprites = attack_sprites

        # movement attriutes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        #self.speed = 130 #moved to stats

        
        #enemy stats
        self.stats = enemy_data['green_helmet']

        self.health = self.stats['health'] #* 0.6
        self.exp = self.stats['exp']
        self.speed = self.stats['speed']
        self.attack_radius = self.stats['attack_radius']
        self.attack_sound = self.stats['attack_sound']
        self.notice_radius = self.stats['notice_radius']
        self.resistance = self.stats['resistance']

 
    def import_assets(self):
        self.animations = {'walking_up': [], 'walking_down': [], 'walking_left': [], 'walking_right': [],
                           'up': [], 'down': [], 'left': [], 'right': []
                           }
        for animation in self.animations.keys():
            full_path = './Assets/enemy/' + animation
            self.animations[animation] = import_folder(full_path)
        #print(self.animations)


    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]


    def get_status(self):
        # idle status
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0]


    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x >0: #player move rigth
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x<0: #player moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx

                    if direction == 'vertical':
                        if self.direction.y >0: #player move down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y <0: #player moving up
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery



    def update(self, dt):
            self.get_status()
            self.animate(dt)