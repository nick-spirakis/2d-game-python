import pygame
#from pygame.sprite import _Group
from settings import *
from support import *
from timer import Timez
from player import Player
import math
import random

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

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
    
    '''
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

        if distance >= 101:
            self.status = 'down'
        '''
    
    def update(self, dt):
        #self.move(dt)

        if self.alive:
            self.check_hit()
        
        self.animate(dt)



# NPC GENERIC

class Npc(pygame.sprite.Sprite): #Generic
    def __init__(self, pos, groups, z, npc_name, npc_message, player, player_pos): #added player and player_pos
        super().__init__(groups)

        self.display_surface = pygame.display.get_surface()
        #npc message
        self.npc_message = npc_message
        self.npc_name = npc_name

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
        #self.health -= 1
        self.open_dialog()
        print(self.npc_message)

    # ------------------------------------------------------------------------------------------------------
    def update(self, dt):      
        self.animate(dt)




# Boss GENERIC

class Boss(pygame.sprite.Sprite): #Generic
    def __init__(self, pos, groups, z, player_add, player, player_data, player_pos, max_health, damage, speed): #added speed (for escaping, higher speed = lower escape chance)
        super().__init__(groups)
        self.import_assets()
        self.frame_index = 0
        self.status = 'idle'

        #pos = (370, 300)
        
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

        self.pos = pygame.math.Vector2(self.rect.center) #was self.pos

        self.player_add_boss = player_add
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

        # added
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

        #added speed for escape chances
        self.boss_speed = speed

        
        self.FLASH_EVENT = pygame.USEREVENT + 1
    
    # Choose a random move from the move_list and get its damage
    def calculate_damage(self):
        #print(f'enemy dealt: {damage} damage to player')
        return self.move_list.get(self.current_attack_name, 0)# return damage
    
    #new
    def select_random_attack(self):
        self.current_attack_name = random.choice(list(self.move_list.keys()))
        return self.current_attack_name


    def take_damage(self, damage):
        self.current_health -= damage
        print(f"boss health: {self.current_health}")

    def get_boss_health(self):
        return self.current_health

    def is_defeated(self):
        self.kill()
        #self.player_add_boss('coin') #added
        #self.player.player_data.coin += 5
        return self.current_health <= 0
    

    #HERE IS TURN BASED COMBAT ===============================================================================================================================================
    def player_take_damage_turn_based(self, enemy_damage):
        #if not self.player.timers["item use"].active:  # Check if the player is currently using an item
        self.player.health -= enemy_damage  # Subtract the enemy's damage from the player's health
        self.player_data.health = self.player.health #added
        if self.player.health <= 0:
            self.player.health = 0  # Ensure the player's health doesn't go negative

            # Implement logic for when the player's health reaches 0 (player defeated)
            # You can add a game over state or reset the player's position, etc.

        print(f"Player's health: {self.player.health}")
        self.player.player_data.health = self.player.health #added for health

    def calculate_player_attack_damage(self):
        # Get the player's base attack power
        base_attack = self.player.stats['attack']
        SWORD_DAMAGE = 5

        # Check if the player has a specific weapon equipped
        if self.player.selected_item == 'sword':
            # Apply additional damage for the sword
            base_attack += SWORD_DAMAGE  # You can define SWORD_DAMAGE as a constant

        # You can add more conditions for other equipped items or abilities here
        return base_attack
    

    def calculate_player_magic_damage(self):
        # Get the player's base attack power
        base_attack = self.player.stats['magic']
        WAND_DAMAGE = 6

        # Check if the player has a specific weapon equipped
        if self.player.selected_item == 'sword':
            # Apply additional damage for the sword
            base_attack += WAND_DAMAGE  # You can define SWORD_DAMAGE as a constant

        # You can add more conditions for other equipped items or abilities here
        return base_attack
    
    def calculate_player_item_damage(self):
        # Get the player's base attack power
        base_attack = self.player.stats['item']
        BAG_DAMAGE = 1

        # Check if the player has a specific weapon equipped
        if self.player.selected_item == 'sword':
            # Apply additional damage for the sword
            base_attack += BAG_DAMAGE  # You can define SWORD_DAMAGE as a constant

        # You can add more conditions for other equipped items or abilities here
        return base_attack
    

    def calculate_player_run_chance(self):
        speed_difference = self.player.stats['speed'] - self.boss_speed

        # Adjust success rate based on speed difference
        if speed_difference > 0:
            success_rate = min(50 + speed_difference, 95)  # Maximum success rate of 95%. ensures that the success rate doesn't go below 5% or above 95%.
        else:
            success_rate = max(5 + speed_difference, 15)  # Minimum success rate of 5%

        # Generate a random number between 1 and 100
        random_number = random.randint(1, 100)

        # Check if the random number falls within the success rate
        if random_number <= success_rate:
            return True  # Escape is successful
        else:
            return False  # Escape failed


    def is_player_defeated(self):
        # Check if the player has been defeated
        return self.player.player_data.health <= 0
        
    # END OF TURN BASED COMBAT CODE

    #============================================================================================================================================================================


    def import_assets(self):
        self.animations = {'idle': [], 'attack1': []
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
class Blast:
    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 2, 4)
        self.velocity = velocity

    def update(self):
        self.rect.y += self.velocity


class Brute(pygame.sprite.Sprite): #Generic
    def __init__(self, pos, groups, z, player_add, player, player_pos): #, surface): #added player and player_pos, and surface
        super().__init__(groups) #pos, surf, groups, z)
        self.import_assets()
        self.frame_index = 0
        self.status = 'down_idle'

        #self.surf = pygame.image.load('./Assets/enemy/down/0.png')
        self.image = self.animations[self.status][self.frame_index] #self.surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

        #self.pos = pos
        self.pos = pygame.math.Vector2(self.rect.center)

        self.player_add = player_add
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)
         
        #enemy stats
        self.stats = enemy_data['brute']

        self.health = self.stats['health'] #* 0.6

        self.alive = True
        self.invul_timer = Timez(200)

        # getting the player
        self.player = player
        self.speed = 10
        self.player_pos = player_pos

        #attack

        self.surface = pygame.display.get_surface()#surface
        self.blast_list = []
        self.blast_max = 1

        #pllayer offset:
        self.offset = pygame.math.Vector2()
        self.offset.x = self.player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = self.player.rect.centery - SCREEN_HEIGHT / 2
        self.hitbox_rect = player.hitbox.copy()
        self.hitbox_rect.center -= self.offset


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
            #self.status = 'attack'
            self.animate(dt)

            if len(self.blast_list) < self.blast_max:

                self.status = 'attack'

                bullet = Blast(self.pos.x + 20, self.pos.y + 110, 1)

                self.blast_list.append(bullet)
                #print("bullet pos")
                if len(self.blast_list) > 0:
                    for bullet in self.blast_list:
                        print("BULLET: ", bullet.x, bullet.y) #for accuravy
                        print("PLAYER: ", self.player.pos.x, self.player.pos.y)
                        print(" ")

                self.stats = 'down_idle'
                

            for shot in self.blast_list:

                if self.hitbox_rect.colliderect(shot.rect): #if self.player.hitbox.colliderect(shot.rect):
                    print("IMPACT")
                    self.player.health -=1
                    self.blast_list.remove(shot)

                elif shot.rect.y >= SCREEN_HEIGHT:
                    self.blast_list.remove(shot)


        if distance <= 120:
            self.satus = 'down_idle'
            #print(self.status)
            direction = math.atan2(self.player.pos.y - self.pos.y, self.player.pos.x - self.pos.x)
            self.pos.x += self.speed * math.cos(direction) *dt
            self.pos.y += self.speed * math.sin(direction) *dt

            self.hitbox.centerx = round(self.pos.x)
            self.rect.centerx = self.hitbox.centerx
            self.hitbox.centery = round(self.pos.y)
            self.rect.centery = self.hitbox.centery
            
            print("enemy pos: ")
            print(self.pos)
            
        if distance <= 10:
            self.status = 'down_idle'
            #print(self.status)
            self.player.health -= 0.1

    
    def update(self, dt):
        self.move(dt)
        #self.draw(self.surface)

        for blast in self.blast_list:
            blast.update()

        for bullet in self.blast_list:
            pygame.draw.rect(pygame.display.get_surface(), (249, 254, 178), bullet.rect) #bullet
            
        #pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), self.hitbox_rect, 4) #player hitbox red

        if self.alive:
            self.check_death()


