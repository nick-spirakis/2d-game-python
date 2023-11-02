import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, Monster, Brute, Entry, Npc, Boss #added Boss #added Npc     #, added bullet
from pytmx.util_pygame import load_pygame
import random
from support import *

from enemy import Enemy
from door import Door

from shop import Shop

import sys

from turnBasedBattle import TurnBasedBattle

class Level:
    def __init__(self, levelNum, player_data): #added player data
        
        self.levelNum = levelNum

        self.boss_bg = None 

        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup() #pygame.sprite.Group()
        # collision
        self.collision_sprites = pygame.sprite.Group()
        # attacks
        self.attack_sprites = pygame.sprite.Group()
        self.brute_sprites = pygame.sprite.Group()
        #making doors
        self.door_sprites = pygame.sprite.Group()

        #npc making npcs
        self.npc_sprites = pygame.sprite.Group()

        #making a boss
        self.boss_sprites = pygame.sprite.Group()


        map_filename = f"map{levelNum}.tmx"
        player_start = self.get_player_start_position(map_filename)

        self.player1 = Player(
                    posi=player_start, #(self.objx, self.objy), 
                    group=self.all_sprites, 
                    collision_sprites=self.collision_sprites, 
                    attack_sprites=self.attack_sprites,
                    door_sprites=self.door_sprites, #added door sprites
                    player_data= player_data, #added player persistence data
                    npc_sprites = self.npc_sprites) #added npc sprites
        

        self.player1.posi = pygame.math.Vector2(self.player1.posi)

        self.player_data = player_data

        #states
        if self.levelNum == 1:
            self.setup()
            
        if self.levelNum == 2:
            self.setupTwo()

        if self.levelNum == 3:
            self.setupThree()

        if self.levelNum == 4:
            self.setupFour()

        self.battle_started = False
        if self.levelNum == 5:
            self.setupFive() # switches to turn based boss fight arena


        # UI

        self.overlay = Overlay(self.player1, self.player_data)

        self.shop = Shop(self.player_data, self.overlay)
        self.shop_open = False
        self.shop_cooldown = 0
        self.shop_cooldown_length = 0.5

        # npc
        self.npc_dialog_open = False


        #joysticks didnt work
        #self.joysticks = []
    


    def get_player_start_position(self, map_filename):
        tmx_data = load_pygame(map_filename)  # Load your Tiled map
        for obj in tmx_data.get_layer_by_name('player'):
            if obj.name == 'start':
                return obj.x, obj.y
        # Return a default position if 'start' object not found
        return 720, 1023
    



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
                self.player1.posi=(obj.x, obj.y)
                

        #enemies
        for obj in tmx_data.get_layer_by_name('enemy'):
            if obj.name == 'spawners':
                Monster(pos=(obj.x, obj.y), 
                        groups=[self.all_sprites, self.collision_sprites, self.attack_sprites],
                        z= LAYERS["main"],
                        player_add = self.player_add,
                        player=self.player1, #was player
                        player_pos = self.player1.pos) #was player
                
                
        #new enemy - brute
        for obj in tmx_data.get_layer_by_name('brute'):
            if obj.name == 'spawner':
                Brute(pos=(obj.x, obj.y), 
                        groups=[self.all_sprites, self.collision_sprites, self.attack_sprites, self.brute_sprites],
                        z= LAYERS["main"],
                        player_add = self.player_add_brute,
                        player=self.player1, #was just player
                        player_pos = self.player1.pos)#, was player
                        #surface=self.display_surface) #added player and surface


        Generic(pos=(0,0), 
                surf=pygame.image.load('map12.png').convert_alpha(), 
                groups=self.all_sprites,
                z=LAYERS['ground'])
        
        # music
        #self.music = [pygame.mixer.Sound("Audio/Soundtrack1-1.wav"), pygame.mixer.Sound("Audio/Soundtrack2-1.wav")]
        #self.music_index = 0
        #self.music_player = self.music[self.music_index].play(loops=-1) #(loops = -1)


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
                self.player1.posi=(obj.x, obj.y)
                '''
                self.player = Player(
                    pos=(obj.x, obj.y), 
                    group=self.all_sprites, 
                    collision_sprites=self.collision_sprites, 
                    attack_sprites=self.attack_sprites,
                    door_sprites= self.door_sprites) #added door sprites
                '''
                
        #enemies
        for obj in tmx_data.get_layer_by_name('enemy'):
            if obj.name == 'spawners':
                Monster(pos=(obj.x, obj.y), 
                        groups=[self.all_sprites, self.collision_sprites, self.attack_sprites],
                        z= LAYERS["main"],
                        player_add = self.player_add,
                        player=self.player1, #was player
                        player_pos = self.player1.pos)
                
        #new enemy - brute
        for obj in tmx_data.get_layer_by_name('brute'):
            if obj.name == 'spawner':
                Brute(pos=(obj.x, obj.y), 
                        groups=[self.all_sprites, self.collision_sprites, self.attack_sprites, self.brute_sprites],
                        z= LAYERS["main"],
                        player_add = self.player_add_brute,
                        player=self.player1,
                        player_pos = self.player1.pos)

        Generic(pos=(0,0), 
                surf=pygame.image.load('map2.png').convert_alpha(), 
                groups=self.all_sprites,
                z=LAYERS['ground'])
        
        # music
        #self.music = [pygame.mixer.Sound("Audio/Soundtrack1-1.wav"), pygame.mixer.Sound("Audio/Soundtrack2-1.wav")]
        #self.music_index = 1
        #self.music_player = self.music[self.music_index].play(loops=-1) #(loops = -1)

#-----------------------------------------------------------------------------------------------------------------

    def setupThree(self):

        tmx_data = load_pygame('map3.tmx')

        for layer in ['border']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), surf, [self.all_sprites, self.collision_sprites], LAYERS['border'])

        for layer in ['town backgrounds']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, LAYERS['rock backgrounds'])

        for layer in ['grass']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, LAYERS['ground'])

        #added this so player is behind roof
        for layer in ['roof']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, LAYERS['house top']) #main


        #player
        for obj in tmx_data.get_layer_by_name('player'):
            if obj.name == 'start': #start is an object in the layer 'player' in tmx, it is used for spawn point
                self.player1.posi=(obj.x, obj.y) # (720, 1023)
                print("HERE")
                print(self.player1.posi) #type is tuple
                
        #enemies
        for obj in tmx_data.get_layer_by_name('enemy'):
            if obj.name == 'spawners':
                Monster(pos=(obj.x, obj.y), 
                        groups=[self.all_sprites, self.collision_sprites, self.attack_sprites],
                        z= LAYERS["main"],
                        player_add = self.player_add,
                        player=self.player1,                            #was player = self.player
                        player_pos = self.player1.pos) #added player    #was player_pos = self.player1.pos)
                print("monster added")
                
        #DOORS
        for obj in tmx_data.get_layer_by_name('door'):
            if obj.name == 'door':
                Entry(pos=(obj.x, obj.y), 
                        groups=[self.all_sprites, self.collision_sprites, self.door_sprites],
                        z= LAYERS["main"],
                        player=self.player1, #was self.player
                        player_pos = self.player1.pos) #added player
                
        
        #NPCs
        for obj in tmx_data.get_layer_by_name('npc'):
            if obj.name == 'Nick':
                npc = Npc(pos=(obj.x, obj.y),
                    groups=[self.all_sprites, self.collision_sprites, self.npc_sprites],
                    z= LAYERS["main"],
                    npc_name = "Nick",
                    npc_message = "I hate this game",
                    player=self.player1,
                    player_pos = self.player1.pos)

                self.npc_sprites.add(npc)
                print("Added NPC 'Nick' to self.npc_sprites")
                
            if obj.name == 'Will':
                npc2 = Npc(pos=(obj.x, obj.y),
                    groups=[self.all_sprites, self.collision_sprites, self.npc_sprites],
                    z= LAYERS["main"],
                    npc_name = "Will",
                    npc_message = "I love this game",
                    player=self.player1,
                    player_pos = self.player1.pos)

                self.npc_sprites.add(npc2)
                print("Added NPC 'Will' to self.npc_sprites")      

        if self.boss_bg:
            self.boss_bg.kill()
            self.boss_bg = None  # Reset self.boss_bg          

        Generic(pos=(0,0), 
                surf=pygame.image.load('map3.png').convert_alpha(), 
                groups=self.all_sprites,
                z=LAYERS['ground'])

        # music
        #self.music = [pygame.mixer.Sound("Audio/Soundtrack1-1.wav"), pygame.mixer.Sound("Audio/Soundtrack2-1.wav")]
        #self.music_index = 0
        #self.music_player = self.music[self.music_index].play(loops=-1) #(loops = -1)


# =================================================================================================================

#setupFour is a shop

    def setupFour(self):

        tmx_data = load_pygame('shop1.tmx') #was tmx_data = load_pygame('shop1.tmx)

        #added border
        for layer in ['border']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), surf, [self.all_sprites, self.collision_sprites], LAYERS['border'])


        for layer in ['ground']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, LAYERS['ground']) #made it ground, idk

        #player
        for obj in tmx_data.get_layer_by_name('player'):
            if obj.name == 'start': #start is an object in the layer 'player' in tmx, it is used for spawn point
                self.player1.posi=(obj.x, obj.y)
                
                
        #DOORS
        for obj in tmx_data.get_layer_by_name('door'):
            if obj.name == 'door':
                Entry(pos=(obj.x, obj.y), 
                        groups=[self.all_sprites, self.collision_sprites, self.door_sprites],
                        z= LAYERS["main"],
                        player=self.player1, #was self.player
                        player_pos = self.player1.pos) #was self.player.pos


        Generic(pos=(0,0), 
                surf=pygame.image.load('shop1.png').convert_alpha(), 
                groups=self.all_sprites,
                z=LAYERS['ground'])

        # music
        #self.music = [pygame.mixer.Sound("Audio/Soundtrack1-1.wav"), pygame.mixer.Sound("Audio/Soundtrack2-1.wav")]
        #self.music_index = 1
        #self.music_player = self.music[self.music_index].play(loops=-1) #(loops = -1)

# =================================================================================================================

# setupFive WILL BE the testing for a turn based set up

    def setupFive(self):

        tmx_data = load_pygame('map5.tmx')

        for layer in ['border']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), surf, [self.all_sprites, self.collision_sprites], LAYERS['border'])

        for layer in ['grass']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, LAYERS['ground'])

        #player
        for obj in tmx_data.get_layer_by_name('player'):
            if obj.name == 'start':
                self.player1.posi=(obj.x, obj.y)
                
        #boss
        #for obj in tmx_data.get_layer_by_name('boss'):
            #if obj.name == 'boss1':
        self.boss1 = Boss(pos= (900, 300),#(obj.x, obj.y), #messing with spawn of boss sprite (if green dude use (900, 350))
                groups=[self.all_sprites, self.collision_sprites, self.boss_sprites],
                z= LAYERS["main"],
                player_add = self.player_add_boss,
                player = self.player1,
                player_data= self.player_data,
                player_pos = self.player1.pos,
                max_health=100,
                damage=5,
                speed = 170) #added speed for run chance

        self.boss_bg = Generic(pos=(0,0), 
                surf=pygame.image.load('map5.png').convert_alpha(), 
                groups=self.all_sprites,
                z=LAYERS['ground'])
        
        # music
        #self.music = [pygame.mixer.Sound("Audio/Soundtrack1-1.wav"), pygame.mixer.Sound("Audio/Soundtrack2-1.wav")]
        #self.music_index = 1
        #self.music_player = self.music[self.music_index].play(loops=-1) #(loops = -1)


#========================================================================================================================


    def player_add(self, item):
        #self.player1.item_inventory[item] += 1
        self.player_data.coin += 1  #self.player1.coin += 30 #was 1
        self.player1.exp += 10

    def player_add_brute(self, item):
        #self.player1.item_inventory[item] += 2 #was self.player.item
        self.player_data.coin += 2
        self.player1.exp += 20 #was self.player.exp

    # for turn based boss
    def player_add_boss(self, item):
        #self.player1.item_inventory[item] += 5 #was self.player.item
        self.player_data.coin += 5
        self.player1.exp += 50

 # =================================================================

    def run(self, dt):
        self.display_surface.fill('black')

        #chack npc
        #print("NPCs in self.npc_sprites:")
        #for npc in self.npc_sprites:
            #print(npc)

        self.all_sprites.custom_draw(self.player1, self.shop, self.npc_sprites) # added npc
        self.all_sprites.update(dt)

        for brute in self.brute_sprites:
            brute.update(dt)

        self.attack_sprites.update(dt)
        self.door_sprites.update(dt)

        #updating npc sprites
        self.npc_sprites.update(dt)
        self.npc_sprites.draw(self.display_surface) # ADDED DRAW

        #updating boss sprites
        self.boss_sprites.update(dt)
        self.boss_sprites.draw(self.display_surface)



        self.overlay.display_items()

        self.shop_cooldown -= dt
        keys = pygame.key.get_pressed()

        if self.levelNum == 4:
            if keys[pygame.K_BACKSPACE]:
                if self.shop_cooldown <= 0:
                    if not self.shop_open:
                        print("opening shop 1")
                        self.shop_open = True
                        self.shop.open_shop1()
                        print("shop 1 displayed")
                        
                    else:
                        self.shop_open = False
                        print("shop closing")
                    self.shop_cooldown = self.shop_cooldown_length

        events = pygame.event.get()

        if self.shop_open:
            self.shop.navigate_options(events)

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Check for Enter key press
                        selected_item = self.shop.options[self.shop.selected_option]
                        self.shop.buy_item(selected_item, self.player_data)

                        #print("get coins pd from level event after buy")
                        coin = self.player_data.get_coins()
                        print(coin)

        else:
            self.shop.close_shop1()

        
        for npc in self.npc_sprites:
            if npc.dialog_is_open():
                npc.show_dialog(npc.text)
                
                #close if player gets too far from npc
                #if self.player1.pos

                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            npc.close_dialog()

        
        # for turn based battle

        if self.levelNum == 5:
            self.battle_started = True

        elif self.levelNum == 3:
            self.battle_started = False
            if self.boss_bg != None:
                self.boss_bg.kill()
                print("Killed boss bg")
                self.boss_bg = None

        if self.battle_started == True:
            battle = TurnBasedBattle(self, self.player1, self.player_data, self.boss1, self.levelNum, self.overlay)
            battle.run()
            

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_suface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()


    def custom_draw(self, player, shop, npc_sprites): #added npc_sprites
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
                        #pygame.draw.rect(self.display_suface, 'green', hitbox_rect, 5) # for hitbox
                        target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
                        pygame.draw.circle(self.display_suface, 'blue', target_pos, 5) # for sword point hitbox
            
            if shop.is_open():
                shop.show_menu(shop.options)

            # added
            for npc in npc_sprites:
                if npc.dialog_is_open():
                    npc.show_dialog(npc.text)
                    #npc.close_dialog()

            

