import pygame
import os
from settings import *
from support import *

class Chest(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, chest_sprites):
        super().__init__(group)

        # animations
        self.import_assets()
        self.status = 'closed'
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['ground']  # or whatever layer is appropriate for chests

        # collisions
        self.hitbox = self.rect.copy()
        self.collision_sprites = collision_sprites
        
        # chest-specific group
        self.chest_sprites = chest_sprites

        # state
        self.is_open = False

    def import_assets(self):
        self.animations = {'closed': [], 'open': []}
        
        for animation in self.animations.keys():
            full_path = './Graphics/chest/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 2 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def interact(self, player):
        if self.hitbox.colliderect(player.hitbox) and not self.is_open:
            self.is_open = True
            self.status = 'open'
            player.coins += 15  # Award the player with coins

    def update(self, dt):
        self.animate(dt)