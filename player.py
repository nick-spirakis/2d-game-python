import pygame
from settings import *
from support import *
from timer import Timez
import os
#from sprites import Monster #added


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, attack_sprites): #added attack sprites
        super().__init__(group)

        #animations
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.z = LAYERS['main']

        #collisions
        self.hitbox = self.rect.copy() #.inflate(()) #inflate shrinks hitbox
        self.collision_sprites = collision_sprites
        #attacks
        self.attack_sprites = attack_sprites

        self.swing = pygame.mixer.Sound(os.path.join('Audio', 'blast.mp3'))

        # movement attriutes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        #self.speed = 130 #moved to stats
 
        # timers
        self.timers = {
            "item use": Timez(900, self.use_item), #350
            "item switch": Timez(200)
            }

        #items
        self.items = ['sword', 'shield']
        self.items_index = 0
        self.selected_item = self.items[self.items_index]#'sword'

        #inventory
        self.item_inventory = {
            'coin': 0
        }

        #player stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 15, 'magic': 4, 'speed': 130}
        self.health = self.stats['health'] #* 0.6
        self.exp = 0
        self.speed = self.stats['speed']

        # music
        self.music = [pygame.mixer.Sound("Audio/Soundtrack1-1.wav"), pygame.mixer.Sound("Audio/Soundtrack2-1.wav")]
        self.music_index = 0
        self.music_player = self.music[self.music_index].play(loops=1) #(loops = -1)

        '''
        #self.music_playe
                if self.music_index < 1:
                    self.music_player.stop()
                    self.music_index += 1
                    self.music_player = self.music[self.music_index].play(loops=1) #(loops = -1)
                if self.music_index == 1:
                    self.music_player.stop()
                    self.music_index = 0
                    self.music_player = self.music[self.music_index].play(loops=1) #(loops = -1)
        '''

    def add_coins(self):
        self.exp += 5


    def use_item(self):
        print("item used")
        if self.selected_item == 'shield':
            if self.health < 120:
                self.health += 20

        if self.selected_item == 'sword':
            for monster in self.attack_sprites.sprites():
                if monster.rect.collidepoint(self.target_pos):
                    self.swing.play()
                    monster.damage()

        #self.items_index = self.items_index #i made this something that does nothing, can delete later
        #print(self.selected_item)

    def get_target_pos(self):
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]


    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
                           'up_sword': [], 'down_sword': [], 'left_sword': [], 'right_sword': [],
                           'up_shield': [], 'down_shield': [], 'left_shield': [], 'right_shield': []
                           }
        for animation in self.animations.keys():
            full_path = './Assets/character/' + animation
            self.animations[animation] = import_folder(full_path)
        #print(self.animations)


    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]


    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers["item use"].active:

            # keyboard movement
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # keyboard item use
            if keys[pygame.K_SPACE]:
                self.timers["item use"].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            if keys[pygame.K_q] and not self.timers["item switch"].active:
                self.timers["item switch"].activate()
                self.items_index +=1
                self.items_index = self.items_index if self.items_index < len(self.items) else 0
                print(self.items_index)
                self.selected_item = self.items[self.items_index]

            #controller
            '''
            for joystick in Level.joysticks:

                if joystick.get_button(11):
                    self.direction.y = -1
                    self.status = 'up'
                elif joystick.get_button(12):
                    self.direction.y = 1
                    self.status = 'down'
                else:
                    self.direction.y = 0

                if joystick.get_button(14):
                    self.direction.x = 1
                    self.status = 'right'
                elif joystick.get_button(13):
                    self.direction.x = -1
                    self.status = 'left'
                else:
                    self.direction.x = 0

                # controller item use
                if joystick.get_button(0): # x
                    self.timers["item use"].activate()
                    self.direction = pygame.math.Vector2()
                    self.frame_index = 0

                if joystick.get_button[3] and not self.timers["item switch"].active:
                    self.timers["item switch"].activate()
                    self.items_index +=1
                    self.items_index = self.items_index if self.items_index < len(self.items) else 0
                    print(self.items_index)
                    self.selected_item = self.items[self.items_index]
                '''
                

    def get_status(self):
        # idle status
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # items/equipment
        if self.timers["item use"].active:
            #print("tool is being used")
            self.status = self.status.split('_')[0] +'_'+ self.selected_item

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
    
    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox') and not hasattr(sprite, 'invul_timer'):
                if sprite.hitbox.colliderect(self.hitbox):
                    print("wall")
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


    def enemy_collision(self, direction): #added direction
        for sprite in self.attack_sprites.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                print("WALKED INTO AN ENEMY")
                #self.health -=1
                #added this
                #if direction == 'horizontal':
                    #if self.direction.x >0: #player move rigth
                        #self.hitbox.right = sprite.hitbox.left
                    #if self.direction.x<0: #player moving left
                        #self.hitbox.left = sprite.hitbox.right
                    #self.rect.centerx = self.hitbox.centerx
                    #self.pos.x = self.hitbox.centerx
                
                #if direction == 'vertical':
                    #if self.direction.y >0: #player move down
                        #self.hitbox.bottom = sprite.hitbox.top
                   #if self.direction.y <0: #player moving up
                        #self.hitbox.top = sprite.hitbox.bottom
                    #self.rect.centery = self.hitbox.centery
                    #self.pos.y = self.hitbox.centery


    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        #hori movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        
        self.enemy_collision('horizontal') #added this (IT WORKS!!!!)
        self.collision('horizontal')

        #vert movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        
        self.enemy_collision('vertical') #added this
        self.collision('vertical')


    def update(self, dt):
            self.input()
            self.get_status()
            self.update_timers()
            self.get_target_pos()
            self.move(dt)
            self.animate(dt)

            #print('player: ')
            #print(self.pos)
           #not needed i guess #self.enemy_collision()

