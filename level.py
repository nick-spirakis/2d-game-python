import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, Monster, Brute, Entry, Npc, Boss
from pytmx.util_pygame import load_pygame
import random
from support import *

from enemy import Enemy
from door import Door

from shop import Shop
from spellbook import Spellbook #added

import sys

from turnBasedBattle import TurnBasedBattle

from party import Party
from partyMembers import PartyMember

class Level:
    def __init__(self, levelNum, player_data): #added player data
        
        self.levelNum = levelNum

        self.boss_bg = None 

        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = CameraGroup()
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

        #making the player
        self.player1 = Player(
                    posi=player_start,
                    group=self.all_sprites, 
                    collision_sprites=self.collision_sprites, 
                    attack_sprites=self.attack_sprites,
                    door_sprites=self.door_sprites, #added door sprites
                    player_data= player_data, #added player persistence data
                    npc_sprites = self.npc_sprites) #added npc sprites
        

        self.player1.posi = pygame.math.Vector2(self.player1.posi)

        self.player_data = player_data

        
        #party

        # create a sprite group for party members
        self.party_sprites = pygame.sprite.Group()

        # create instances of PartyMember and add them to the sprite group
        
        self.party = Party(self.player1) #player1 is user, initializes party

        #penguin = PartyMember(self.player1.posi, self.player1, self.party, 1) # make a party member
        #self.party.add_member(penguin) # add to party
        #self.party_sprites.add(penguin) # add to sprite group

        for i in range(1):
            image_path = "./Assets/penguin"  #"./Assets/character" #/down_idle/0.png"
            penguin = PartyMember((0,0), self.player1, self.party, i, image_path)  # added image_path
            self.party.add_member(penguin)
            print("TOP:")
            print(len(self.party.members))
            self.party_sprites.add(penguin)


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
            self.setupFive()


        # UI
        self.overlay = Overlay(self.player1, self.player_data)

        self.shop = Shop(self.player_data, self.overlay)
        self.shop_open = False
        self.shop_cooldown = 0
        self.shop_cooldown_length = 0.5

        # spellbook
        self.book = Spellbook(self.player_data, self.overlay)
        self.book_open = False
        self.book_cooldown = 0
        self.book_cooldown_length = 0.5

        # npc
        self.npc_dialog_open = False


        #joysticks controller work in progress
        #self.joysticks = []
    

    def get_player_start_position(self, map_filename):
        tmx_data = load_pygame(map_filename) 
        for obj in tmx_data.get_layer_by_name('player'):
            if obj.name == 'start':
                return obj.x, obj.y
        #or default pos
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
            if obj.name == 'start':
                self.player1.posi=(obj.x, obj.y)
                

        #enemies
        for obj in tmx_data.get_layer_by_name('enemy'):
            if obj.name == 'spawners':
                Monster(pos=(obj.x, obj.y), 
                        groups=[self.all_sprites, self.collision_sprites, self.attack_sprites],
                        z= LAYERS["main"],
                        player_add = self.player_add,
                        player=self.player1, 
                        player_pos = self.player1.pos) 
                
                
        #enemy - brute
        for obj in tmx_data.get_layer_by_name('brute'):
            if obj.name == 'spawner':
                Brute(pos=(obj.x, obj.y),
                        groups=[self.all_sprites, self.collision_sprites, self.attack_sprites, self.brute_sprites],
                        z= LAYERS["main"],
                        player_add = self.player_add_brute,
                        player=self.player1, 
                        player_pos = self.player1.pos)


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
                
        #enemies
        for obj in tmx_data.get_layer_by_name('enemy'):
            if obj.name == 'spawners':
                Monster(pos=(obj.x, obj.y), 
                        groups=[self.all_sprites, self.collision_sprites, self.attack_sprites],
                        z= LAYERS["main"],
                        player_add = self.player_add,
                        player=self.player1,
                        player_pos = self.player1.pos)
                
        #enemy - brute
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
                Generic((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, LAYERS['house top'])


        #player
        for obj in tmx_data.get_layer_by_name('player'):
            if obj.name == 'start': 
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
                        player=self.player1,
                        player_pos = self.player1.pos)
                print("monster added")
                
        #DOORS
        for obj in tmx_data.get_layer_by_name('door'):
            if obj.name == 'door':
                Entry(pos=(obj.x, obj.y), 
                        groups=[self.all_sprites, self.collision_sprites, self.door_sprites],
                        z= LAYERS["main"],
                        player=self.player1,
                        player_pos = self.player1.pos) 
                
        
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
            self.boss_bg = None  #reseting self.boss_bg          

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

        tmx_data = load_pygame('shop1.tmx')

        #added border
        for layer in ['border']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), surf, [self.all_sprites, self.collision_sprites], LAYERS['border'])


        for layer in ['ground']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), surf, self.all_sprites, LAYERS['ground'])

        #player
        for obj in tmx_data.get_layer_by_name('player'):
            if obj.name == 'start':
                self.player1.posi=(obj.x, obj.y)
                
                
        #DOORS
        for obj in tmx_data.get_layer_by_name('door'):
            if obj.name == 'door':
                Entry(pos=(obj.x, obj.y), 
                        groups=[self.all_sprites, self.collision_sprites, self.door_sprites],
                        z= LAYERS["main"],
                        player=self.player1,
                        player_pos = self.player1.pos)


        Generic(pos=(0,0), 
                surf=pygame.image.load('shop1.png').convert_alpha(), 
                groups=self.all_sprites,
                z=LAYERS['ground'])

        # music
        #self.music = [pygame.mixer.Sound("Audio/Soundtrack1-1.wav"), pygame.mixer.Sound("Audio/Soundtrack2-1.wav")]
        #self.music_index = 1
        #self.music_player = self.music[self.music_index].play(loops=-1) #(loops = -1)

# =================================================================================================================

# setupFive is the testing for a turn based set up

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
                
        
        self.boss1 = Boss(pos= (900, 300), #900, 300 seems to be the best spot to spawn this boss in
                groups=[self.all_sprites, self.collision_sprites, self.boss_sprites],
                z= LAYERS["main"],
                player_add = self.player_add_boss,
                player = self.player1,
                player_data= self.player_data,
                player_pos = self.player1.pos,
                max_health=100,
                damage=5,
                speed = 170) #added speed for player menu run chance

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
        self.player_data.coin += 1 
        self.player1.exp += 10

    def player_add_brute(self, item):
        #self.player1.item_inventory[item] += 2
        self.player_data.coin += 2
        self.player1.exp += 20

    # for turn based boss
    def player_add_boss(self, item):
        #self.player1.item_inventory[item] += 5
        self.player_data.coin += 5
        self.player1.exp += 50

 # =================================================================

    def run(self, dt):
        self.display_surface.fill('black')

        self.all_sprites.custom_draw(self.player1, self.shop, self.npc_sprites, self.book, self.brute_sprites, self.party_sprites, self.levelNum) #added levelNum
        self.all_sprites.update(dt)

        self.attack_sprites.update(dt)

        self.door_sprites.update(dt)

        #updating npc sprites
        self.npc_sprites.update(dt)
        #self.npc_sprites.draw(self.display_surface) #removed this to see if duplicates go away

        #updating boss sprites
        self.boss_sprites.update(dt)
        self.boss_sprites.draw(self.display_surface)

        self.overlay.display_items()

        # Update the positions directly using the player's position
        main_player_pos = self.player1.rect.topleft
        for i, party_member in enumerate(self.party.members):
            # Calculate relative position behind the player
            party_member.rect.topleft = (main_player_pos[0], main_player_pos[1])

        self.party_sprites.update(dt)

        #self.party_sprites.draw(self.display_surface) #(caused the duplicate penguin)


        #for shop
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
                    if event.key == pygame.K_RETURN:
                        selected_item = self.shop.options[self.shop.selected_option]
                        self.shop.buy_item(selected_item, self.player_data)

                        coin = self.player_data.get_coins()
                        print(coin)

        else:
            self.shop.close_shop1()


        # for spellbook
        self.book_cooldown -= dt

        if keys[pygame.K_BACKSLASH]:
            if self.book_cooldown <= 0:
                if not self.book_open:
                    print("opening spellbook")
                    self.book_open = True
                    self.book.open_spellbook()
                    print("spellbook displayed")
                    
                else:
                    self.book_open = False
                    print("spellbook closing")
                self.book_cooldown = self.book_cooldown_length


        if self.book_open:
            self.book.navigate_options(events)

            self.book.navigate_all_options(events)

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.book.swap_spells()

        else:
            self.book.close_spellbook()

        # for npcs
        for npc in self.npc_sprites:
            if npc.dialog_is_open():
                npc.show_dialog(npc.text)
                
                # might add a feature to close if player gets too far from npc
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
                
                self.boss_bg.stop()
                self.boss_bg = None

        if self.battle_started == True:
            battle = TurnBasedBattle(self, self.player1, self.player_data, self.boss1, self.levelNum, self.overlay, self.party) #added party
            battle.run()
            

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        self.last_known_direction = (0, 0)


    def custom_draw(self, player, shop, npc_sprites, book, brute_sprites, party_sprites, levelNum): #added levelNum
        self.offset.x = player.rect.centerx - self.half_width 
        self.offset.y = player.rect.centery - self.half_height

        for l in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == l:
                    offset_rect = sprite.rect.copy()
                    
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

                    if sprite == player:
                        hitbox_rect = player.hitbox.copy()
                        hitbox_rect.center = offset_rect.center
                        target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
                        # draw sword hitbox
                        #pygame.draw.circle(self.display_surface, 'blue', target_pos, 5)
            
            # new blasts for brute
            for brute in brute_sprites:
                brute_blasts = brute.get_blasts()
                for blast in brute_blasts:
                    # draw blast
                    offset_blast_rect = blast.rect.copy()
                    offset_blast_rect.center -= self.offset
                    self.display_surface.blit(blast.image, offset_blast_rect)

            if shop.is_open():
                shop.show_menu(shop.options)

            for npc in npc_sprites:
                if npc.dialog_is_open():
                    npc.show_dialog(npc.text)

            if book.is_open():
                book.show_menu(book.options)
                book.show_all_spells(book.unlocked_spells)
        
            # Draw party members with a slightly increased offset

            # Check if the player is moving before updating last_known_direction
            if player.direction.x != 0 or player.direction.y != 0:
                if player.direction.x == -1:
                    self.last_known_direction = (-1, 0)
                elif player.direction.x == 1:
                    self.last_known_direction = (1, 0)
                elif player.direction.y == -1:
                    self.last_known_direction = (0, -1)
                elif player.direction.y == 1:
                    self.last_known_direction = (0, 1)

            for party_member in party_sprites:
                offset_rect = party_member.rect.copy()
                offset_rect.center -= self.offset

                if levelNum == 5: 
                    offset_rect.x += 10
                    offset_rect.y -= 40  
                    party_member.status = "right"
                else:
                    if self.last_known_direction == (-1, 0):
                        offset_rect.x += 20  # Adjust this value to control the horizontal distance
                        offset_rect.y += 10  # Adjust this value to control the vertical distance
                        party_member.status = "left"

                    elif self.last_known_direction == (1, 0):
                        offset_rect.x -= 20  
                        offset_rect.y += 10  
                        party_member.status = "right"

                    elif self.last_known_direction == (0, -1):
                        offset_rect.y += 50  
                        party_member.status = "up"

                    elif self.last_known_direction == (0, 1):
                        offset_rect.y -= 30  
                        party_member.status = "down"

                self.display_surface.blit(party_member.image, offset_rect)
                #print(self.last_known_direction)

