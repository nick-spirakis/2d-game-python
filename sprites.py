import pygame
#from pygame.sprite import _Group
from settings import *
from support import *
from timer import Timez
from player import Player
import math

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

        if distance >= 101:
            self.status = 'down'

    
    def update(self, dt):
        self.move(dt)

        if self.alive:
            self.check_death()
        
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
            
        pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), self.hitbox_rect, 4) #player hitbox

        if self.alive:
            self.check_death()


