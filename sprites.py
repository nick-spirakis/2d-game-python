import pygame
#from pygame.sprite import _Group
from settings import *
from support import *
from timer import Timez
from player import Player
import math
import random

import time

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)


# animated water generic
class Water(Generic):
    def __init__(self,pos,frames,groups):

        #animation setup for water
        self.frames = frames
        self.frame_index = 0

        super().__init__(pos, 
                         self.frames[self.frame_index], 
                         groups, 
                         z = LAYERS['water'])
        
    def animate(self, dt):
        self.frame_index += 5 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)


# basic enemy generic
class Monster(pygame.sprite.Sprite): #Generic
    def __init__(self, pos, groups, z, player_add, player, player_pos): #added player and player_pos
        super().__init__(groups) #pos, surf, groups, z)
        self.import_assets()
        self.frame_index = 0
        self.status = 'down'

        #self.surf = pygame.image.load('./Assets/enemy/down/0.png')
        self.image = self.animations[self.status][self.frame_index] #self.surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

        #self.pos = pos
        self.pos = pygame.math.Vector2(self.rect.center)

        self.player_add = player_add
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)
         
        #enemy stats
        self.stats = enemy_data['green_helmet']

        self.health = self.stats['health'] #* 0.6

        self.alive = True
        self.invul_timer = Timez(200)

        # getting the player
        self.player = player
        self.speed = 20
        self.player_pos = player_pos
    

    def damage(self):
        print("e health -1")
        self.health -= 1
        print(self.health)

    def check_death(self):
        if self.health <= 0:
            print("dead")
            self.kill()
            self.player_add('coin')


    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                            'walking_up': [], 'walking_down': [], 'walking_left': [], 'walking_right': []
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
        
    def move(self, dt):
        distance = math.sqrt((self.player.pos.x - self.pos.x)**2 + (self.player.pos.y - self.pos.y)**2)
        if distance <= 100:
            print("ENEMY MOVING")
            self.status = 'walking_left'
            self.animate(dt)
            direction = math.atan2(self.player.pos.y - self.pos.y, self.player.pos.x - self.pos.x)
            self.pos.x += self.speed * math.cos(direction) *dt
            self.pos.y += self.speed * math.sin(direction) *dt

            self.hitbox.centerx = round(self.pos.x)
            self.rect.centerx = self.hitbox.centerx
            self.hitbox.centery = round(self.pos.y)
            self.rect.centery = self.hitbox.centery
        if distance <= 10:
            self.player.health -= 0.1
            print("DAMAGIG PLAYER - line 114 of sprites")

        if distance >= 101:
            self.status = 'down'

    
    def update(self, dt):
        self.move(dt)

        if self.alive:
            self.check_death()
        
        self.animate(dt)
# ===============================================================================================================


# door generic
class Entry(pygame.sprite.Sprite): #Generic
    def __init__(self, pos, groups, z, player, player_pos): #added player and player_pos
        super().__init__(groups) #pos, surf, groups, z)

        self.import_assets()
        self.frame_index = 0
        self.status = 'closed'

        #self.surf = pygame.image.load('./Assets/enemy/down/0.png')
        self.image = self.animations[self.status][self.frame_index] #self.surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

        #self.pos = pos
        self.pos = pygame.math.Vector2(self.rect.center)

        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)
         
        self.alive = True
        self.invul_timer = Timez(200)

        self.stats = enemy_data['green_helmet']
        self.health = 1

        # getting the player
        self.player = player
        self.speed = 20
        self.player_pos = player_pos
    

    def door_hit(self):
        #print("e health -1")
        self.health -= 1
        #print(self.health)

    def check_hit(self):
        if self.health <= 0:
            print("door opened")
            self.kill()


    def import_assets(self):
        self.animations = {'closed': [], 'open': []}
        
        for animation in self.animations.keys():
            full_path = './Assets/door/' + animation
            self.animations[animation] = import_folder(full_path)
        #print(self.animations)

    def animate(self, dt):
        self.frame_index += 2 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]
    
    
    def update(self, dt):
        #self.move(dt)

        if self.alive:
            self.check_hit()
        
        self.animate(dt)



# NPC GENERIC
class Npc(pygame.sprite.Sprite):
    def __init__(self, pos, groups, z, npc_name, npc_message, player, player_pos):
        super().__init__(groups)

        self.display_surface = pygame.display.get_surface()

        #npc message
        self.npc_message = npc_message
        self.npc_name = npc_name

        #animations
        self.import_assets()
        self.frame_index = 0
        self.status = 'standing'

        self.image = self.animations[self.status][self.frame_index] 
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

        #self.pos = pos
        self.pos = pygame.math.Vector2(self.rect.center)

        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)
         
        self.alive = True
        self.invul_timer = Timez(200)

        self.stats = enemy_data['green_helmet']
        self.health = 100
        
        self.selected_dialog = 0
        self.font = pygame.font.SysFont('arial', 20)
        self.dialog_open = False

        self.player = player
        self.player_pos = player_pos

        self.moving_right = True  # Flag to track movement direction
        self.pause_time = 1  # Define the pause time
        self.last_pause_time = time.time()  # Initialize the last pause time

        self.radius = 40
        self.center = pygame.math.Vector2(750,960) #710, 920
        self.destination = None

        self.willCenter = pygame.math.Vector2(510, 755)
        self.willRadius = 30

        self.moving = False
        self.delay_timer = 0
        self.delay_duration = 85 #60
        self.speed = 1  # Speed of movement
    

    def import_assets(self):
        self.animations = {'standing': [], 'walking': []}
        
        for animation in self.animations.keys():
            full_path = './Assets/npc/' + self.npc_name + '/' + animation
            self.animations[animation] = import_folder(full_path)
        print("NPC ANIMATION")
        print(self.animations)


    def animate(self, dt):
        self.frame_index += 2 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]


    def walk(self):
        if self.npc_name == "Nick":
            if not self.moving:
                # Choose a random spot
                
                random_angle = random.uniform(0, 2 * math.pi)
                random_distance = random.uniform(0, self.radius)
                self.destination = pygame.math.Vector2(
                    self.center.x + random_distance * math.cos(random_angle),
                    self.center.y + random_distance * math.sin(random_angle)
                )
                self.moving = True

            if self.moving:
                # Move to spot
                direction = (self.destination - self.pos).normalize()
                self.pos += direction * self.speed
                self.pos = pygame.math.Vector2(round(self.pos.x), round(self.pos.y))  # Round the position
                self.rect.center = self.pos

                # Check if at spot then wait
                if self.pos.distance_to(self.destination) <= 1:
                    self.delay_timer += 1
                    if self.delay_timer >= self.delay_duration:
                        self.delay_timer = 0
                        self.moving = False

        if self.npc_name == "Will":
            if not self.moving:
                # Choose a random spot
                
                random_angle = random.uniform(0, 2 * math.pi)
                random_distance = random.uniform(0, self.willRadius)
                self.destination = pygame.math.Vector2(
                    self.willCenter.x + random_distance * math.cos(random_angle),
                    self.willCenter.y + random_distance * math.sin(random_angle)
                )
                self.moving = True

            if self.moving:
                # Move to spot
                direction = (self.destination - self.pos).normalize()
                self.pos += direction * self.speed
                self.pos = pygame.math.Vector2(round(self.pos.x), round(self.pos.y))  # Round the position
                self.rect.center = self.pos

                # Check if at spot then wait
                if self.pos.distance_to(self.destination) <= 1:
                    self.delay_timer += 1
                    if self.delay_timer >= self.delay_duration:
                        self.delay_timer = 0
                        self.moving = False
            

    #----------------------------------------------------------------------------------
    def show_dialog(self, dialogs):
        rect_w = 200
        rect_h = 30

        for i, dialog in enumerate(dialogs):
            text = f"{dialog}"
        
            dialog_rect = pygame.Rect(
                self.display_surface.get_size()[0] -300 - rect_w,
                self.display_surface.get_size()[1] - 500 + i * rect_h,
                rect_w,
                rect_h
            )
       
            text_surf = self.font.render(text, False, 'white')
            text_rect = text_surf.get_rect(center=dialog_rect.center)

            pygame.draw.rect(self.display_surface, 'blue', dialog_rect)
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, dialog_rect, 3)

            if i == self.selected_text:
                pygame.draw.rect(self.display_surface, 'blue', dialog_rect)

            self.display_surface.blit(text_surf, text_rect)


    def open_dialog(self):
        self.text = [f'Hi my name is {self.npc_name}.', f'{self.npc_message}', 'Goodbye!']
        self.selected_text = 0
        self.show_dialog(self.text)
        self.dialog_open = True


    def close_dialog(self):
        self.dialog_open = False


    def dialog_is_open(self):
        return self.dialog_open
    
    def play_message(self):
        self.open_dialog()
        print(self.npc_message)

    # ------------------------------------------------------------------------------------------------------
    def update(self, dt):      
        self.animate(dt)
        #walking
        self.walk()


# Boss GENERIC for turn based battle
class Boss(pygame.sprite.Sprite): #Generic
    def __init__(self, pos, groups, z, player_add, player, player_data, player_pos, max_health, damage, speed): #added speed (for escaping, higher speed = lower escape chance)
        super().__init__(groups)
        self.import_assets()
        self.frame_index = 0
        self.status = 'idle'

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

        self.pos = pygame.math.Vector2(self.rect.center)

        self.player_add_boss = player_add
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

        # boss stats
        self.max_health = max_health
        self.current_health = max_health
        self.damage = damage

        self.alive = True
        self.invul_timer = Timez(200)

        # getting the player
        self.player = player
        self.speed = 20
        self.player_pos = player_pos

        self.move_list = {"Swipe": 3, "Crush": 5, "Devastate": 10}
        self.current_attack_name = ""

        self.player_data = player_data

        # new for player spellbook
        self.spell_book = self.player_data.spell_book
        
        # added speed for escape chances
        self.boss_speed = speed

        
        self.FLASH_EVENT = pygame.USEREVENT + 1
    
    # get a random move from the move_list
    def calculate_damage(self):
        return self.move_list.get(self.current_attack_name, 0) #return damage boss will do to player
    
    #selectes a random attack for boss to do to player
    def select_random_attack(self):
        self.current_attack_name = random.choice(list(self.move_list.keys()))
        return self.current_attack_name

    # boss takes damage
    def take_damage(self, damage):
        self.current_health -= damage
        print(f"boss health: {self.current_health}")

    def get_boss_health(self):
        return self.current_health

    def is_defeated(self):
        self.kill()
        #self.player_add_boss('coin') # feature to add coins upon boss defeat
        #self.player.player_data.coin += 5
        return self.current_health <= 0
    

    #HERE IS TURN BASED COMBAT ===============================================================================================================================================
    def player_take_damage_turn_based(self, enemy_damage):
        self.player.health -= enemy_damage  # subtract boss damage from the player health
        self.player_data.health = self.player.health
        if self.player.health <= 0:
            self.player.health = 0

        print(f"Player's health: {self.player.health}")
        self.player.player_data.health = self.player.health #added for health

    
    def calculate_player_attack_damage(self):
        base_attack = self.player.stats['attack']
        SWORD_DAMAGE = 5

        # add so i can make other weapons for the player to equip besides the sword
        if self.player.selected_item == 'sword':
            base_attack += SWORD_DAMAGE

        return base_attack
    

    #here i will add player spell book

    def calculate_player_magic_damage(self):
        base_attack = self.player.stats['magic']
        WAND_DAMAGE = 6

        # this is still sword because that is the only weapon I have implemeneted at the time, 
        # will most likely update this where magic does less damage if weapon is a sword, but does more damage if weapon is a wand or something
        if self.player.selected_item == 'sword':
            base_attack += WAND_DAMAGE

        return base_attack
    
    def calculate_player_item_damage(self):
        base_attack = self.player.stats['item']
        BAG_DAMAGE = 1

        # Check player selected item
        if self.player.selected_item == 'sword':
            base_attack += BAG_DAMAGE

        return base_attack
    

    def calculate_player_run_chance(self):
        speed_difference = self.player.stats['speed'] - self.boss_speed

        # adjust run success rate based on speed difference
        if speed_difference > 0:
            success_rate = min(50 + speed_difference, 95)  # max success rate of 95%. ensures that the success rate doesn't go below 5% or above 95%.
        else:
            success_rate = max(5 + speed_difference, 15)  # min success rate of 5%

        # Generate a random number between 1 and 100
        random_number = random.randint(1, 100)

        # check if the random number is within the success rate
        if random_number <= success_rate:
            return True # escaped
        else:
            return False # did not


    def is_player_defeated(self):
        # Check if player defeated
        return self.player.player_data.health <= 0
        
    # END OF TURN BASED COMBAT LOGIC CODE

    #============================================================================================================================================================================


    def import_assets(self):
        self.animations = {'idle': [], 'attack1': [], 'attack2': []
                           }
        for animation in self.animations.keys():
            full_path = './Assets/boss/' + animation
            self.animations[animation] = import_folder(full_path)
        #print(self.animations)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]
        

    def update(self, dt):
        self.animate(dt)


# ================================================================================================================
# Brutes

class Blast: # updated the blast class so Brutes can shoot players - they currently cannot miss but this will be updated
    def __init__(self, enemy_pos, velocity, player_pos):

        self.rect = pygame.Rect(enemy_pos[0], enemy_pos[1], 10, 4)
        self.velocity = velocity

        self.image = pygame.Surface((10,4))
        self.image.fill((249, 254, 178))

        self.player_pos = player_pos
        

    def update_velocity(self, player_pos):
        blast_direction = math.atan2(player_pos[1] - self.rect.y, player_pos[0] - self.rect.x)
        self.velocity_x = math.cos(blast_direction) * self.velocity
        self.velocity_y = math.sin(blast_direction) * self.velocity


    def update(self):
        self.update_velocity(self.player_pos)
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def get_position(self):
        return self.rect.topleft


class Brute(pygame.sprite.Sprite):
    def __init__(self, pos, groups, z, player_add, player, player_pos):
        super().__init__(groups)
        self.import_assets()
        self.frame_index = 0
        self.status = 'down_idle'

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

        self.pos = pygame.math.Vector2(self.rect.center)

        self.player_add = player_add
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)
         
        #enemy stats
        self.stats = enemy_data['brute']
        self.health = self.stats['health']

        self.alive = True
        self.invul_timer = Timez(200)

        # getting the player
        self.player = player
        self.speed = 10
        self.player_pos = player_pos

        #attack
        self.surface = pygame.display.get_surface()
        self.blast_list = [] #list of blasts
        self.blast_max = 1

        #player offset:
        self.offset = pygame.math.Vector2()
        self.half_width = self.surface.get_size()[0] // 2
        self.half_height = self.surface.get_size()[1] // 2
        self.offset.x = player.hitbox.centerx - self.half_width 
        self.offset.y = player.hitbox.centery - self.half_height

        self.hitbox_rect = player.hitbox
        self.hitbox_rect.center -= self.offset
        self.green_box = self.hitbox_rect.copy()


    def get_blasts(self):
        return self.blast_list

    def damage(self):
        print("e health -1")
        self.health -= 0.5

    def check_death(self):
        if self.health <= 0:
            print("dead")
            self.kill()
            self.player_add('coin')

    def import_assets(self):
        self.animations = {'attack': [], 'down_idle': []
                           }
        for animation in self.animations.keys():
            full_path = './Assets/enemy2/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]
        
    def move(self, dt):
        distance = math.sqrt((self.player.pos.x - self.pos.x)**2 + (self.player.pos.y - self.pos.y)**2)
        if distance <= 180 and distance >= 121:
            self.status = 'attack'
            self.animate(dt)

            if len(self.blast_list) < self.blast_max:

                self.status = 'attack'
                
                #create the blast if player is close enough, add to list
                velocity = 1
                blast = Blast(self.rect.center, velocity, (self.player_pos.x, self.player_pos.y))

                self.blast_list.append(blast)

                self.status = 'down_idle'


        if distance <= 120:
            self.status = 'down_idle'

            direction = math.atan2(self.player.pos.y - self.pos.y, self.player.pos.x - self.pos.x)
            self.pos.x += self.speed * math.cos(direction) *dt
            self.pos.y += self.speed * math.sin(direction) *dt

            self.hitbox.centerx = round(self.pos.x)
            self.rect.centerx = self.hitbox.centerx
            self.hitbox.centery = round(self.pos.y)
            self.rect.centery = self.hitbox.centery
            
        if distance <= 10:
            # damage player
            self.status = 'down_idle'
            self.player.health -= 0.1

        # update bullet to track player
        for shot in self.blast_list:
            shot.player_pos = (self.player.pos.x, self.player.pos.y)
            
            shot.update_velocity((self.player.pos.x, self.player.pos.y))
            shot.update()

            if self.hitbox_rect.colliderect(shot.rect):
                print("IMPACT")
                self.player.health -= 1
                self.blast_list.remove(shot)
            
            elif shot.rect.x > SCREEN_WIDTH *32 or shot.rect.y > SCREEN_HEIGHT*32:
                self.blast_list.remove(shot)


    def update(self, dt):
        #pygame.draw.rect(self.surface, 'green', self.green_box, 5) # player hitbox visual
        self.move(dt)

        for blast in self.blast_list:
            blast.update()

        if self.alive:
            self.check_death()

