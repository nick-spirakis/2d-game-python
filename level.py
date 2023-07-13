import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, Monster, Brute #, added bullet
from pytmx.util_pygame import load_pygame
import random
from support import *

from enemy import Enemy

class Level:
    def __init__(self):
        # get display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup() #pygame.sprite.Group()
        # collision
        self.collision_sprites = pygame.sprite.Group()
        # attacks
        self.attack_sprites = pygame.sprite.Group()

        self.brute_sprites = pygame.sprite.Group()

        self.setup() #remove Two (self.setupTwo())
        # UI
        self.overlay = Overlay(self.player)

        #joysticks didnt work
        #self.joysticks = []
    
    def setup(self):

        tmx_data = load_pygame('map1.tmx')

        for layer in ['border']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), surf, [self.all_sprites, self.collision_sprites], LAYERS['border'])

        for layer in ['rock backgrounds']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, LAYERS['rock backgrounds'])

        #water
        water_frames = import_folder('Graphics/Water')
        for x, y, surf in tmx_data.get_layer_by_name('water').tiles():
            Water((x*TILE_SIZE, y*TILE_SIZE), water_frames, self.all_sprites)


        #player
        for obj in tmx_data.get_layer_by_name('player'):
            if obj.name == 'start': #start is an object in the layer 'player' in tmx, it is used for spawn point
                self.player = Player(
                    pos=(obj.x, obj.y), 
                    group=self.all_sprites, 
                    collision_sprites=self.collision_sprites, 
                    attack_sprites=self.attack_sprites)
                

        #enemies
        for obj in tmx_data.get_layer_by_name('enemy'):
            if obj.name == 'spawners':
                Monster(pos=(obj.x, obj.y), 
                        groups=[self.all_sprites, self.collision_sprites, self.attack_sprites],
                        z= LAYERS["main"],
                        player_add = self.player_add,
                        player=self.player,
                        player_pos = self.player.pos) #added player
                
                
        #new enemy - brute
        for obj in tmx_data.get_layer_by_name('brute'):
            if obj.name == 'spawner':
                Brute(pos=(obj.x, obj.y), 
                        groups=[self.all_sprites, self.collision_sprites, self.attack_sprites, self.brute_sprites],
                        z= LAYERS["main"],
                        player_add = self.player_add_brute,
                        player=self.player,
                        player_pos = self.player.pos)#,
                        #surface=self.display_surface) #added player and surface


        Generic(pos=(0,0), 
                surf=pygame.image.load('map12.png').convert_alpha(), 
                groups=self.all_sprites,
                z=LAYERS['ground'])


#========================================================================================================================

    def setupTwo(self):

        tmx_data = load_pygame('map2.tmx')

        for layer in ['border']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), surf, [self.all_sprites, self.collision_sprites], LAYERS['border'])

        for layer in ['rock backgrounds']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, LAYERS['rock backgrounds'])

        #water
        water_frames = import_folder('Graphics/Water')
        for x, y, surf in tmx_data.get_layer_by_name('water').tiles():
            Water((x*TILE_SIZE, y*TILE_SIZE), water_frames, self.all_sprites)

        #player
        for obj in tmx_data.get_layer_by_name('player'):
            if obj.name == 'start':
                self.player = Player(
                    pos=(obj.x, obj.y), 
                    group=self.all_sprites, 
                    collision_sprites=self.collision_sprites, 
                    attack_sprites=self.attack_sprites)
                
        #enemies
        for obj in tmx_data.get_layer_by_name('enemy'):
            if obj.name == 'spawners':
                Monster(pos=(obj.x, obj.y), 
                        groups=[self.all_sprites, self.collision_sprites, self.attack_sprites],
                        z= LAYERS["main"],
                        player_add = self.player_add,
                        player=self.player,
                        player_pos = self.player.pos)
                
        #new enemy - brute
        for obj in tmx_data.get_layer_by_name('brute'):
            if obj.name == 'spawner':
                Brute(pos=(obj.x, obj.y), 
                        groups=[self.all_sprites, self.collision_sprites, self.attack_sprites, self.brute_sprites],
                        z= LAYERS["main"],
                        player_add = self.player_add_brute,
                        player=self.player,
                        player_pos = self.player.pos)

        Generic(pos=(0,0), 
                surf=pygame.image.load('map2.png').convert_alpha(), 
                groups=self.all_sprites,
                z=LAYERS['ground'])



#========================================================================================================================


    def player_add(self, item):
        self.player.item_inventory[item] += 1
        self.player.exp += 10

    def player_add_brute(self, item):
        self.player.item_inventory[item] += 2
        self.player.exp += 20


    def run(self, dt):
        self.display_surface.fill('blue')
        #self.all_sprites.draw(self.display_surface)

        self.all_sprites.custom_draw(self.player)

        # updates all sprites
        self.all_sprites.update(dt)

        for brute in self.brute_sprites:
            brute.update(dt)
            #print("update brute")
            #brute.draw(self.display_surface) commented
        

        self.attack_sprites.update(dt) #added

        # UI
        self.overlay.display_items()



class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_suface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()


    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for l in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == l:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_suface.blit(sprite.image, offset_rect)

                    if sprite == player:
                        hitbox_rect = player.hitbox.copy()
                        hitbox_rect.center = offset_rect.center
                        #pygame.draw.rect(self.display_suface, 'green', hitbox_rect, 5)
                        target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
                        #pygame.draw.circle(self.display_suface, 'blue', target_pos, 5)

