import pygame
from settings import *
from support import *
from timer import Timez
import os
#from sprites import Monster #added


# adding persistence
class PlayerData:
    def __init__(self):
        self.health = 100
        self.experience = 0

        self.player_level = 1 
        self.max_experience = 50

        self.coin = 0
        self.inventory = []
        self.spell_book = ["spell 1", "Dia", "Hellfire"]
        self.unlocked_spells = ["spell 1", "Dia", "Hellfire", "Metia", "Red Roc"] # added for spell book
        self.levelInt = 1


    def update_coins(self, coins):
        self.coin = coins
        print(f"update coin function: {self.coin}")

    def get_coins(self):
        return self.coin
    
    # added
    def gain_experience(self, amount):
        self.experience += amount

    
    def update_experience(self, exp):
        #print("CALLED")
        self.experience = exp
        #print(f'update experience: {self.experience}')
        return self.experience
    
    def get_exp(self):
        #print(f'get experience: {self.experience}')
        return self.experience

    def get_experience_percentage(self):
        return (self.experience / self.max_experience) * 100
    # -----------------------------------------------------------------
    
    
    def get_health(self):
        return self.health
    
    #adding saves with json ----------------------------------------------------------
    def to_dict(self):
        return {
            "health": self.health,
            "experience": self.experience,
            "coin": self.coin,
            "inventory": self.inventory,
            "spell_book": self.spell_book,
            "leve_int": self.levelInt,
            "player_level": self.player_level
        }

    @classmethod
    def from_dict(cls, data):
        player_data = cls()
        player_data.health = data.get("health", 100)
        player_data.experience = data.get("experience", 0)
        player_data.coin = data.get("coin", 0)
        player_data.inventory = data.get("inventory", [])
        player_data.spell_book = data.get("spell_book", ["spell 1", "Dia", "Hellfire"])
        player_data.levelInt = data.get("levelInt", 1)
        player_data.player_level = data.get("player_level", 1)

        return player_data
    #------------------------------------------------------------------------------------


class Player(pygame.sprite.Sprite):
    def __init__(self, posi, group, collision_sprites, attack_sprites, door_sprites, player_data, npc_sprites, chest_sprites): # added chest_sprites, npc_sprites, added player_data for persistence
        super().__init__(group)

        #moved here - was above self.pos
        self.direction = pygame.math.Vector2()

        self.posi = posi

        #animations
        self.import_assets()

        self.status = 'right_idle'
        self.frame_index = 0

        # general setup

        self.image = self.animations[self.status][self.frame_index]

        self.rect = self.image.get_rect(center = posi)

        print("center")
        print(type(posi))
        self.z = LAYERS['main']

        #collisions
        self.hitbox = self.rect.copy() #.inflate(()) #inflate shrinks hitbox
        self.collision_sprites = collision_sprites
        #attacks
        self.attack_sprites = attack_sprites


        #added door sprites -------------------------------------------------------------------------------------------
        self.door_sprites = door_sprites


        #npc spries
        self.npc_sprites = npc_sprites

        #chest sprites
        self.chest_sprites = chest_sprites

        
        self.swing = pygame.mixer.Sound(os.path.join('Audio', 'blast.mp3'))

        self.hit = pygame.mixer.Sound(os.path.join('Audio', 'clap.mp3'))

        # player movement attriutes
        
        self.pos = pygame.math.Vector2(self.rect.center)

        #party function
        self.party_index = 0

        
 
        # timers
        self.timers = {
            "item use": Timez(600, self.use_item), #900
            "item switch": Timez(200)
            }

        #items
        self.items = ['sword', 'shield']
        self.items_index = 0
        self.selected_item = self.items[self.items_index]#'sword'


        #player stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 15, 'magic': 4, 'speed': 180, 'item': 1}

        #ADDED to persist health and data
        self.player_data = player_data

        self.health = self.player_data.health
        self.exp = self.player_data.experience

        #spell book persist ------------------------------------------------------------------
        self.spell_book = self.player_data.spell_book
        self.spell_index = 0

        self.speed = self.stats['speed']


        # gravity for 2d parts
        self.levelInt = self.player_data.levelInt
        self.gravity = 0.9  # Adjust gravity as needed
        self.vertical_velocity = 0
        self.on_ground = False


    def add_coins(self):
        self.exp += 5


    def use_item(self):
        print("item used")
        if self.selected_item == 'shield':
            if self.health <= 80:
                self.health += 20
            else:
                self.health = 100

        if self.selected_item == 'sword':
            for monster in self.attack_sprites.sprites():
                if monster.rect.collidepoint(self.target_pos):
                    monster.damage()
                    self.swing.play()
                    
            #should kill a door when hit with sword
            for entry in self.door_sprites.sprites():
                if entry.rect.collidepoint(self.target_pos):
                    entry.door_hit()

            for npc in self.npc_sprites.sprites():
                if npc.rect.collidepoint(self.target_pos):
                    npc.play_message()

            for chest in self.chest_sprites.sprites(): #added
                if chest.rect.collidepoint(self.target_pos):
                    chest.interact()


    def get_target_pos(self): #where the sword hits an enemy
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]


    def adjust_left_sword_animation(self):
        if 'left_sword' in self.animations:
            for i in range(len(self.animations['left_sword'])):
                original_frame = self.animations['left_sword'][i]
                flipped_frame = pygame.transform.flip(original_frame, True, False)
                scaled_frame = pygame.transform.scale(flipped_frame, (45, 32))
                self.animations['left_sword'][i] = scaled_frame


    def adjust_left_sheild_animation(self):
        if 'left_shield' in self.animations:
            for i in range(len(self.animations['left_shield'])):
                original_frame = self.animations['left_shield'][i]
                flipped_frame = pygame.transform.flip(original_frame, True, False)
                scaled_frame = pygame.transform.scale(flipped_frame, (45, 32))
                self.animations['left_shield'][i] = scaled_frame


    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
                           'up_sword': [], 'down_sword': [], 'left_sword': [], 'right_sword': [],
                           'up_shield': [], 'down_shield': [], 'left_shield': [], 'right_shield': []
                           }
        for animation in self.animations.keys():
            #full_path = './Assets/character/' + animation
            full_path = './Assets/new_character/' + animation
            self.animations[animation] = import_folder(full_path)

        self.adjust_left_sword_animation()
        self.adjust_left_sheild_animation()



    def animate(self, dt):
        self.frame_index += 4 * dt

        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        else:
            self.image = self.animations[self.status][int(self.frame_index)]
        

# ============================================================================================================================================

# =============================================================================================================================================
    def input(self):
        keys = pygame.key.get_pressed()

        # added for new animations and left sword swing
        if not self.timers["item use"].active:

            # keyboard movement
            if keys[pygame.K_UP] and self.levelInt != 6:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN] and self.levelInt != 6:
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
            if keys[pygame.K_SPACE] and self.levelInt != 6:
                self.timers["item use"].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            if keys[pygame.K_q] and not self.timers["item switch"].active:
                self.timers["item switch"].activate()
                self.items_index +=1
                self.items_index = self.items_index if self.items_index < len(self.items) else 0
                print(self.items_index)
                self.selected_item = self.items[self.items_index]

            # ps4 controller support - work in progress
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
            print("tool is being used")
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


    def enemy_collision(self, direction):
        for sprite in self.attack_sprites.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                print("WALKED INTO AN ENEMY")
                

    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        #hori movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        
        self.enemy_collision('horizontal')
        self.collision('horizontal')

        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        
        self.enemy_collision('vertical')
        self.collision('vertical')

    
    def apply_gravity(self):
        if not self.on_ground:
            print("not on ground")
            self.vertical_velocity += self.gravity
            self.hitbox.centery += self.vertical_velocity
            self.rect.y += self.vertical_velocity


    def handle_jumping(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vertical_velocity = - 6 #-60
            self.on_ground = False

        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox') and not hasattr(sprite, 'invul_timer'):
                if sprite.hitbox.colliderect(self.hitbox):
                        print("on ground")
                        self.on_ground = True

                    
    def update(self, dt):
            self.animate(dt)
            self.input()
            self.get_status()
            self.update_timers()
            self.get_target_pos()
            self.move(dt)

            # updating persistence player
            self.player_data.health = self.health

            if self.levelInt == 6:
                self.apply_gravity()
                self.handle_jumping()

            