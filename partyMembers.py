from party import Party
import pygame
from support import *


class PartyMember(pygame.sprite.Sprite):
    def __init__(self, player_pos, main_player, party, member_index, animation_folder): #changed  image path to folder
        super().__init__()

        self.main_player = main_player

        self.party = party
        self.member_index = member_index
        
        # Load animations for the party member
        self.animations = {'up': [], 'down': [], 'left': [], 'right': []}
        self.load_animations(animation_folder)
        self.status = 'right'
        self.frame_index = 0

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect()

        # Apply an offset of 10 pixels to the left of the main player
        offset_x = 10

        self.rect.topleft = (main_player.rect.topleft[0] - offset_x, main_player.rect.topleft[1])


    def load_animations(self, animation_folder):
        for direction in self.animations.keys():
            full_path = f'{animation_folder}/{direction}'
            self.animations[direction] = import_folder(full_path)


    def animate(self, dt):
        self.frame_index += 4 * dt

        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        else:
            self.image = self.animations[self.status][int(self.frame_index)]
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.9), int(self.image.get_height() * 0.9)))


    def update(self, dt):
        #print(f"Updated Position for Member {self.member_index}: {self.rect.topleft}")
        self.animate(dt)

