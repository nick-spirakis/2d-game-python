import pygame, sys
from settings import *
from level import Level

pygame.font.init()

# FONTS
HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
WINNER_TIME_FONT = pygame.font.SysFont('comicsans', 70)
CONTROLLER_FONT = pygame.font.SysFont('comicsans', 40)

def draw_disconnect(disconnect_text):
    Level.display_surface = pygame.display.get_surface()
    dis_text = CONTROLLER_FONT.render(disconnect_text, 1, 'white')
    Level.display_surface.blit(dis_text, (SCREEN_WIDTH//2 - dis_text.get_width()//2, SCREEN_HEIGHT//2 - dis_text.get_height()//2))
    pygame.display.update()


# controller disconnect check
disconnect = False
def check_controller():
    global disconnect
    disconnect_text = ""

    joystick_counter = pygame.joystick.get_count()
    for i in range(joystick_counter):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

    if not joystick_counter:
        if not disconnect:
            print("RECONNECT CONTROLLER")
            disconnect_text = "RECONNECT CONTROLLER"

            disconnect = True

    if disconnect_text != "":
        draw_disconnect(disconnect_text)

        pygame.time.delay(5000) #5 sec
        check_controller()

    else:
        disconnect = False

#joysticks = [] #adds connected joysticks


# COLORS
BLUE = (90, 250, 250)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)


def draw_win(win_text, time_text):
    display_surface = pygame.display.get_surface()
    draw_text = WINNER_FONT.render(win_text, 1, WHITE)
    display_surface.blit(draw_text, (SCREEN_WIDTH//2 - draw_text.get_width()//2, SCREEN_HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()

    draw_time_text = WINNER_TIME_FONT.render(time_text, 1, WHITE)
    display_surface.blit(draw_time_text, (SCREEN_WIDTH//2 - draw_text.get_width()//2, SCREEN_HEIGHT//2 - draw_text.get_height()//2 + 150))
    pygame.display.update()
    pygame.time.delay(2000) #2 sec


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("First Fantasy 2")
        self.clock = pygame.time.Clock()
        self.level = Level()

        self.enemys = self.level.attack_sprites # if = <Group(0 sprites)> then win game
        self.player = self.level.player
    
    def run(self):
        while True:
            #check_controller()
            for event in pygame.event.get():
                '''
                # controller
                if event.type == pygame.JOYDEVICEADDED:
                    print(event)
                    joy = pygame.joystick.Joystick(event.device_index)
                    self.level.joysticks.append(joy)
                # end controller
                '''

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            self.level.run(dt)
            pygame.display.update()

            if len(self.enemys) == 0: #if all enemies die
                    self.screen
                    end_text = "PLAYER WINS!"
                    time_text = "Quiting"
                    draw_win(end_text, time_text)
                    pygame.quit()
                    sys.exit()

            if self.player.health <= 0: #if all hp gone
                    self.screen
                    end_text = "YOU DIED"
                    time_text = "Quiting"
                    draw_win(end_text, time_text)
                    pygame.quit()
                    sys.exit()
                    

if __name__ == '__main__':
    game = Game()
    game.run()


'''
pygame.font.init() #initializes pygame font library
pygame.mixer.init()
pygame.joystick.init()



pygame.init()

sprite_group = pygame.sprite.Group()

# -----------------------------------------------------------------
joysticks = [] #adds connected joysticks

# cross 0        SHOOT
# circle 1
# sqaure 2
# triangle 3

# share 4
# PS 5
# options 6

# left stick click 7
# right stick click 8

# L1 9          BOOSTER
# R1 10

# up 11         MOVE UP
# down 12       MOVE DOWN
# left 13       MOVE LEFT
# right 14      MOVE RIGHT

# touchpad 15

# analog stick
    # horiz_move = joystick.get_axis(0)
    # verti_move = joystick.get_axis(1)

# --------------------------------------------------------------


# making main surface (a window)
WIDTH, HEIGHT = 1280, 720 # dimensions of screen
# 0,0 is top left
# X goes right
# Y goes down

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # new window of width and height
pygame.display.set_caption("NEW GAME")

# <TiledTileLayer[4]: "border">


#y sort camera
'''



'''
# ---------------------------------------------------
# COLORS
BLUE = (90, 250, 250)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
# ---------------------------------------------------

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# --------------------------------
# VARIABLES
FPS = 60
VELOCITY = 3
BOOSTER_VELOCITY = 15
BLAST_VELOCITY = 20
MAX_BLASTS = 10

GHOST_WIDTH, GHOST_HEIGHT = 32, 32 #30, 45

ENEMY_WIDTH, ENEMY_HEIGHT = 32, 32
# ---------------------------------


#---------------------------------
# SOUNDS
BLAST_HIT = pygame.mixer.Sound(os.path.join('Assets', 'blast.mp3'))
BLAST_FIRE = pygame.mixer.Sound(os.path.join('Assets', 'blast.mp3'))
#-------------------------------

#-----------------------------------
# FONTS
HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
WINNER_TIME_FONT = pygame.font.SysFont('comicsans', 70)
CONTROLLER_FONT = pygame.font.SysFont('comicsans', 40)
#-----------------------------------

# -------------------------------------
# EVENTS
ENEMY_HIT = pygame.USEREVENT + 1 #1 is code for this custon event

PLAYER_HIT = pygame.USEREVENT + 2 
# -------------------------------------

# --------------------------------------------------------------------
# CHARACTERS 
GHOST_IMAGE = pygame.image.load(os.path.join('Assets', 'playerBlue.png')) #ghost2.png  #new_ship.png
# resizing and rotating
GHOST = pygame.transform.scale(GHOST_IMAGE, (GHOST_WIDTH, GHOST_HEIGHT))

#ghost player

class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('Graphics/tree.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.health_image = pygame.image.load('Graphics/tree.png').convert_alpha()
        self.health_rect = self.health_image.get_rect(center = (0, 0)) #NEW HEALTH HERE now

for i in range(5):
    random_x = random.randint(200, 600)
    random_y = random.randint(200, 600)
    Tree((random_x, random_y), camera_group)

#treeX = 200
#treeY = 200
#Tree = ((treeX, treeY), camera_group)

#class Enemy(pygame.sprite.Sprite):
    #def __init__(self, pos, group):
        #super().__init__(group)
        #self.image = pygame.image.load(os.path.join('Assets', 'playerBlue.png')).convert_alpha()
        #self.rect = self.image.get_rect(topleft = pos)

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, group):
        super().__init__(group)

        self.sprites = []
        #self.sprites.append(pygame.image.load(os.path.join('Assets', 'playerBlue.png')))
        #self.sprites.append(pygame.image.load(os.path.join('Assets', 'playerBlueSword.png')))

        self.sprites.append(pygame.image.load(os.path.join('Assets', '11.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets', '12.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets', '13.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets', '14.png')))
        self.sprites.append(pygame.image.load(os.path.join('Assets', '15.png')))
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.is_animating = False

        #BORDER
        self.is_border = False
        self.can_move = True

        #ITEMS
        
        self.has_armor_hat = False

        if self.has_armor_hat:
            self.health = 16
        else:
            self.health = 8

            
        #self.image = pygame.image.load(os.path.join('Assets', 'playerBlue.png')).convert_alpha() #new_ship.png

        #self.rect = self.image.get_rect(center = pos)  #KEEP THIS, COMMENTED FOR COLLISION WHICH IS NOW BELOW posY
    
        
        self.direction = pygame.math.Vector2()
        self.speed = 5

        #moving animation
        self.is_moving_left = False 
        self.is_moving_right = False
        self.is_moving_up = False
        self.is_moving_down = False

        #self.direction.x = pos[0] #needed
        #self.direction.y = pos[1] #needed

        self.posX = 0#0   760
        self.posY = 0#0   360

        self.direction.x = self.posX #new
        self.direction.y = self.posY #new

        self.rect = self.image.get_rect(center = (self.posX, self.posY))


        self.health_sprites = []
        #self.sprites.append(pygame.image.load(os.path.join('Assets', 'playerBlue.png')))
        #self.sprites.append(pygame.image.load(os.path.join('Assets', 'playerBlueSword.png')))

        self.health_sprites.append(pygame.image.load(os.path.join('Assets', 'h1.png')))
        self.health_sprites.append(pygame.image.load(os.path.join('Assets', 'h2.png')))
        self.health_sprites.append(pygame.image.load(os.path.join('Assets', 'h3.png')))
        self.health_sprites.append(pygame.image.load(os.path.join('Assets', 'h4.png')))
        self.health_sprites.append(pygame.image.load(os.path.join('Assets', 'h5.png')))
        self.health_sprites.append(pygame.image.load(os.path.join('Assets', 'h6.png')))
        self.health_sprites.append(pygame.image.load(os.path.join('Assets', 'h7.png')))
        self.health_sprites.append(pygame.image.load(os.path.join('Assets', 'h8.png')))
        self.health_sprites.append(pygame.image.load(os.path.join('Assets', 'h9.png')))
        
        self.health_current_sprite = 0
        self.health_image = self.health_sprites[self.health_current_sprite]
        self.health_rect = self.health_image.get_rect(center = (self.posX, self.posY)) #NEW HEALTH HERE now

        return

    def wearing_hat(self):
        self.has_armor_hat = True

    def animate(self):
        self.is_animating = True

    def border_hit(self):
        self.is_border = True

    def input(self, joysticks, posX, posY):

        if self.can_move == True:
            posX = int()
            posY = int()

            keys_pressed = pygame.key.get_pressed()

            # left
            if keys_pressed[pygame.K_LEFT]:
                self.direction.x = -1
                posX -= self.direction.x
            # right
            elif keys_pressed[pygame.K_RIGHT]:
                self.direction.x = 1
                posX += self.direction.x
            else:
                self.direction.x = 0
                posX += self.direction.x

            # up
            if keys_pressed[pygame.K_UP]:
                self.direction.y = -1
                posY -= self.direction.y
            # down
            elif keys_pressed[pygame.K_DOWN]:
                self.direction.y = 1
                posY += self.direction.y
            else:
                self.direction.y = 0
                posY += self.direction.y


            #controller
            for joystick in joysticks:
            # spawn
                if joystick.get_button(4):
                    if self.posX == 0 and self.posY == 0:
                        self.direction.x = 120
                        self.direction.y = 80
                        posX = self.direction.x *self.speed
                        posY = self.direction.y *self.speed
                    #else:
                        #print("pressed spawn")

            # left
                if joystick.get_button(13):
                    if joystick.get_button(9):
                        self.direction.x = -1
                        posX -= self.direction.x
                        self.is_moving_right = False
                        self.is_moving_left = True
                        self.is_moving_up = False
                        self.is_moving_down = False
                    else:
                        self.direction.x -= 1
                        posX -= self.direction.x
                        self.is_moving_right = False
                        self.is_moving_left = True
                        self.is_moving_up = False
                        self.is_moving_down = False
            
            # right
                if joystick.get_button(14):
                    if joystick.get_button(9):
                        self.direction.x = 1
                        posX += self.direction.x
                        self.is_moving_left = False
                        self.is_moving_right = True
                        self.is_moving_up = False
                        self.is_moving_down = False
                    else:
                        self.direction.x += 1
                        posX += self.direction.x
                        self.is_moving_left = False
                        self.is_moving_right = True
                        self.is_moving_up = False
                        self.is_moving_down = False

            # up
                if joystick.get_button(11):
                    if joystick.get_button(9):
                        self.direction.y = -1
                        posY -= self.direction.y
                        self.is_moving_left = False
                        self.is_moving_right = False
                        self.is_moving_down = False
                        self.is_moving_up = True
                    else:
                        self.direction.y = -1
                        posY -= self.direction.y
                        self.is_moving_left = False
                        self.is_moving_right = False
                        self.is_moving_down = False
                        self.is_moving_up = True

            # down
                if joystick.get_button(12):
                    if joystick.get_button(9):
                        self.direction.y = 1
                        posY += self.direction.y
                        self.is_moving_left = False
                        self.is_moving_right = False
                        self.is_moving_up = False
                        self.is_moving_down = True
                    else:
                        self.direction.y = 1
                        posY += self.direction.y
                        self.is_moving_left = False
                        self.is_moving_right = False
                        self.is_moving_up = False
                        self.is_moving_down = True

                if joystick.get_button(0): #triangle is 3
                    self.animate()
                
                #print((posX, posY))
        return posX, posY
    
    def update(self, joysticks):

        if self.is_animating == True:
            self.current_sprite += 0.3 #1

            if self.current_sprite >= len(self.sprites): #1:
                self.current_sprite = 0
                self.is_animating = False
            self.image = self.sprites[int(self.current_sprite)]



        #default dance

        if self.has_armor_hat == False:
            if self.is_moving_left == False and self.is_moving_right == False:
                self.image = pygame.image.load(os.path.join('Assets', '11-1.png'))

            if self.is_moving_right == True:
                self.image = pygame.image.load(os.path.join('Assets', '11.png'))
            
            if self.is_moving_left == True:
                self.image = pygame.transform.flip(pygame.image.load(os.path.join('Assets', '11.png')), True, False)

            if self.is_moving_up == True:
                self.image = pygame.image.load(os.path.join('Assets', '11-3.png'))

        
        if self.has_armor_hat:
            if self.is_moving_left == False and self.is_moving_right == False:
                self.image = pygame.image.load(os.path.join('Assets', '11-1-hat.png'))

            if self.is_moving_right == True:
                self.image = pygame.image.load(os.path.join('Assets', '11-hat.png'))
            
            if self.is_moving_left == True:
                self.image = pygame.transform.flip(pygame.image.load(os.path.join('Assets', '11-hat.png')), True, False)

            if self.is_moving_up == True:
                self.image = pygame.image.load(os.path.join('Assets', '11-2-hat.png'))
        


        
        if self.is_border != True: #added this
            self.can_move = True
            self.input(joysticks, int(self.direction.x), int(self.direction.y))

            #new
            self.rect.center += self.direction * self.speed
            self.health_rect.center = (self.rect.center[0], self.rect.center[1] -35)
            
            self.posX += self.direction.x
            self.posY += self.direction.y


        if self.is_border:
            if self.is_moving_left:
                print("border left")
                print(self.posX, self.posY)
                self.direction.x += 1 #=1
                self.direction.y += 0 #=1



                self.posX += self.direction.x
                self.posY += self.direction.y

                self.rect.center += self.direction * self.speed
                self.is_border = False


            if self.is_moving_right:
                print("border right")
                print(self.posX, self.posY)
                self.direction.x -= 1
                self.direction.y += 0 #=1

                self.posX += self.direction.x
                self.posY += self.direction.y

                self.rect.center += self.direction * self.speed
                self.is_border = False

            if self.is_moving_up:
                print("border up")
                print(self.posX, self.posY)
                self.direction.x += 0 #=1
                self.direction.y += 1 #=1

                self.posX += self.direction.x
                self.posY += self.direction.y

                self.rect.center += self.direction * self.speed
                self.is_border = False

            if self.is_moving_down:
                print("border down")
                print(self.posX, self.posY)
                self.direction.x += 0 #=1
                self.direction.y -= 1 #=1

                self.posX += self.direction.x
                self.posY += self.direction.y

                self.rect.center += self.direction * self.speed
                self.is_border = False



        #print((self.posX, self.posY)) #coords

        xxx = self.posX * self.speed #indented both
        yyy = self.posY * self.speed

        self.checkColBorder()

        return xxx, yyy

    def checkColBorder(self):
        #added for collision colision
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                if layer.name == "object border group":
                    for obj in layer:
                        #print(x[0])
                        if pygame.Rect(obj.x, obj.y, obj.width, obj.height).colliderect(self.rect) == True: #ghostplayer in mian, self in Player
                            #print("BOREDER PLEASE STOP")
                            self.border_hit() #equivilent of self.is_border = True

                        self.can_move = True
                        #else:
                            #print("")

    def shoot(self, ghost_blasts, joysticks, enemymonster):
        for joystick in joysticks:
            if joystick.get_button(0) and len(ghost_blasts) < MAX_BLASTS:

                posX, posY = self.update(joysticks) #new
                posX = int(posX)
                posY = int(posY)
                #print("shoot: ", posX, posY)

                blast = pygame.Rect(
                    posX, posY, 10, 5)

                ghost_blasts.append(blast)

                print(ghost_blasts) # ex of output: [<rect(45, 68, 10, 5)>]
                #BLAST_FIRE.play() #sound of swinging sword

                for blast in ghost_blasts:
                    blast.x = posX
                    blast.y = posY
                    if enemymonster.colliderect(blast):
                    #new event that I can check for in main
                        print("attack landed")
                        pygame.event.post(pygame.event.Event(ENEMY_HIT))
                        #pygame.time.wait(500) #.5 sec delays whole game
                        ghost_blasts.remove(blast)
                        
                    # removes bullet if goes of screen
                    elif blast.x > WIDTH:
                        ghost_blasts.remove(blast)
                        
                    else:
                        #pygame.time.delay(1000) #1sec
                        ghost_blasts.remove(blast)
                        

            posX, posY = self.update(joysticks)
        
    def get_blast_x(self):
        #print(self.rect.x) #[<rect(30, 43, 10, 5)>] #left top width height
        return posX, posY

        

posX, posY = 0, 0   # = 0, 0
ghostplayer = Player((posX, posY), camera_group)


#posX, posY = Player.get_blast_x(ghostplayer)  
# =================================================================================
# =================================================================================


# enemy character
ENEMY_IMAGE = pygame.image.load(os.path.join('Assets', 'enemy3.png')) #ghost2.png
# resizing and rotating
ENEMY = pygame.transform.rotate(
    pygame.transform.scale(ENEMY_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT)),
    0)
# --------------------------------------------------------------------


# -------------------------------------------------------------------------------------------
# BACKGROUND
#SCENE = pygame.transform.scale(
    #pygame.image.load(os.path.join('Assets', 'park.png')),
      #(WIDTH, HEIGHT)) #was space.png
# --------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------
# draws to window
def draw_window(ghostplayer, enemymonster, ghost_blasts, ghost_health, enemy_health, ship_rotate_val):
    # background color
    #WIN.fill(BLUE)

    # background image
    #WIN.blit(SCENE, (0,0))

    # adds a border in center of screen
    #pygame.draw.rect(WIN, BLACK, BORDER)

    # old health was text
    #ghost_health_display = HEALTH_FONT.render("Nick the Hero: " + str(ghost_health), 1, YELLOW)
    #enemy_health_display = HEALTH_FONT.render("Evilman the Vile: " + str(enemy_health), 1, RED)
    
    # new health is a bar
    #e_back = pygame.Rect(enemymonster.x+10, enemymonster.y-10, 4, 5)
    #e_health = pygame.Rect(enemymonster.x+10, enemymonster.y-10, enemy_health, 5)
    #pygame.draw.rect(WIN, BLACK, e_back)
    #pygame.draw.rect(WIN, RED, e_health)

    
    #WIN.blit(enemy_health_display, (enemymonster.x-10, enemymonster.y-40)) #(WIDTH - enemy_health_display.get_width() - 270, 10))

    #GHOST1 = pygame.transform.rotate(GHOST, ship_rotate_val)                                           #commented!@#!!!@

    # character
    #WIN.blit(GHOST1, (ghostplayer[0], ghostplayer[1]))
    #if enemy_health > 0:

    #player health:

    #enemy health
    WIN.blit(ENEMY, (enemymonster.x,enemymonster.y))
    e_back = pygame.Rect(enemymonster.x+10, enemymonster.y-10, 4, 5)
    e_health = pygame.Rect(enemymonster.x+10, enemymonster.y-10, enemy_health, 5)
    pygame.draw.rect(WIN, BLACK, e_back)
    pygame.draw.rect(WIN, RED, e_health)

    for blast in ghost_blasts:
        pygame.draw.rect(WIN, RED, blast)

    pygame.display.update()

#---------------------------------------------------------------------------------------------------------

#[0] was .x, [1] was .y

def ghost_movement_handler(keys_pressed, ghostplayer):
    # left
    if keys_pressed[pygame.K_LEFT] and ghostplayer[0] - VELOCITY > 0 -7:
        ghostplayer[0] -= VELOCITY
    # right
    if keys_pressed[pygame.K_RIGHT] and ghostplayer[0] + VELOCITY + GHOST_WIDTH < WIDTH: #BORDER.x:      # GHOST_WIDTH was ghostplayer.width
        ghostplayer[0] += VELOCITY
    # up
    if keys_pressed[pygame.K_UP] and ghostplayer[1] - VELOCITY > 0 -5:
        ghostplayer[1] -= VELOCITY
    # down
    if keys_pressed[pygame.K_DOWN] and ghostplayer[1] + VELOCITY + GHOST_HEIGHT < HEIGHT:               # GHOST_HEIGHT was ghostplayer.height
        ghostplayer[1] += VELOCITY

"""
def ghost_controller_movement_handler(joysticks, ghostplayer):
    for joystick in joysticks:
        # left
        if joystick.get_button(13) and ghostplayer.x - VELOCITY > 0 -7:
            if joystick.get_button(9):
                ghostplayer.x -= BOOSTER_VELOCITY
            else:
                ghostplayer.x -= VELOCITY

        # right
        if joystick.get_button(14) and ghostplayer.x + VELOCITY + ghostplayer.width < WIDTH: #BORDER.x:
            if joystick.get_button(9):
                ghostplayer.x += BOOSTER_VELOCITY
            else:
                ghostplayer.x += VELOCITY

        # up
        if joystick.get_button(11) and ghostplayer.y - VELOCITY > 0 -5:
            if joystick.get_button(9):
                ghostplayer.y -= BOOSTER_VELOCITY
            else:
                ghostplayer.y -= VELOCITY

        # down
        if joystick.get_button(12) and ghostplayer.y + VELOCITY + ghostplayer.height < HEIGHT:
            if joystick.get_button(9):
                ghostplayer.y += BOOSTER_VELOCITY
            else:
                ghostplayer.y += VELOCITY

        # boosters (bumber controls)
        #if joystick.get_button(9) and ghostplayer.y - VELOCITY > 0 -5:
            #print("pressed left")
            #ship_rotate_val -= 2
            #ghostplayer.y -= BOOSTER_VELOCITY
            #VELOCITY == BOOSTER_VELOCITY + 10

        #if joystick.get_button(10) and ghostplayer.y + VELOCITY + ghostplayer.height < HEIGHT:
            #print("pressed right")
                #ship_rotate_val += 2
            #ghostplayer.y += BOOSTER_VELOCITY
"""

def ghost_blasts_handler(ghost_blasts, enemymonster, ghostplayer):
    for blast in ghost_blasts:
        #x1, y1 = Player.get_blast_x(ghostplayer)

        x1, y1 = Player.update(ghostplayer, joysticks) #removed joysticks
        #print(x1)
        #print(y1)
        print("GOT x1 y1!!!!!")
        #x1 = int(x1)
        blast.x = x1
        blast.y = y1
        if enemymonster.colliderect(blast):
            #new event that I can check for in main
            print("hit")
            pygame.event.post(pygame.event.Event(ENEMY_HIT))
            ghost_blasts.remove(blast)
        # removes bullet if goes of screen
        elif blast.x > WIDTH:
            ghost_blasts.remove(blast)

# -------------------------------------------------------------------------------------------------------------
# turned off
def monster_mover_handler(enemymonster):
    print("turned off monster mover")
    #move up
    #if enemymonster.y > 0 -5:
        #ENEMY_VELOCITY = random.randrange(1, 3)
        #enemymonster.y -= ENEMY_VELOCITY

    #wrap to bottom
    #if enemymonster.y <= 0:
        #enemymonster.y = HEIGHT

    # left to right
    #if enemymonster.x > WIDTH:
        #enemymonster.x = 0 #BORDER.x

    #wrap to side
    #if enemymonster.x <= WIDTH:
        #ENEMY_VELOCITY = random.randrange(1, 3)
        #enemymonster.x += ENEMY_VELOCITY

# -----------------------------------------------------------------------------------------------------------

def draw_win(win_text, time_text):
    draw_text = WINNER_FONT.render(win_text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()

    draw_time_text = WINNER_TIME_FONT.render(time_text, 1, WHITE)
    WIN.blit(draw_time_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2 + 150))
    pygame.display.update()
    pygame.time.delay(2000) #2 sec

# ----------------------------------------------------------------------------------------------------------
def draw_disconnect(disconnect_text):
    dis_text = CONTROLLER_FONT.render(disconnect_text, 1, WHITE)
    WIN.blit(dis_text, (WIDTH//2 - dis_text.get_width()//2, HEIGHT//2 - dis_text.get_height()//2))
    pygame.display.update()


# controller disconnect check
disconnect = False
def check_controller():
    global disconnect
    disconnect_text = ""

    joystick_counter = pygame.joystick.get_count()
    for i in range(joystick_counter):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

    if not joystick_counter:
        if not disconnect:
            print("RECONNECT CONTROLLER")
            disconnect_text = "RECONNECT CONTROLLER"

            disconnect = True

    if disconnect_text != "":
        draw_disconnect(disconnect_text)

        pygame.time.delay(5000) #5 sec
        check_controller()

    else:
        disconnect = False
# ---------------------------------------------------------------------------------------

tmx_data = load_pygame('map1.tmx')
tile_list = []



# 0,   1408    x left (0) to right (1408)
# 0,   1888    y top (0) to bottom (1888)
# main event loop


scroll_area_width = 200

def main():
    joystick = ""
    
    ghost_blasts = []

    #added ghost player health
    ghost_health = 10 #was 20

    #enemy player
    enemymonster = pygame.Rect(500, 340, GHOST_WIDTH, GHOST_HEIGHT) #500, 420
    enemey_health = 3 #was 4

    ship_rotate_val = 1

    # game clock
    clock = pygame.time.Clock()

    # game loop that terminates when game ends
    run = True
    while run:
        #see if controller plugged in
        check_controller()

        # speed of loop, fps
        clock.tick(FPS)

        # get list of events
        for event in pygame.event.get():
            # controller
            if event.type == pygame.JOYDEVICEADDED:
                print(event)
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks.append(joy)
                ghostplayer.joystick = joy

            # quit on X
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            
            # shoot joystick
            for joystick in joysticks:
                    if event.type == pygame.JOYBUTTONDOWN:
                        if joystick.get_button(0) and len(ghost_blasts) < MAX_BLASTS:     
                            Player.shoot(ghostplayer, ghost_blasts, joysticks, enemymonster) #joysticks

                    if joystick.get_button(6):
                        event.type == pygame.quit()

            if event.type == ENEMY_HIT:
                enemey_health -= 1
                BLAST_HIT.play()

            #added player health
            if event.type == PLAYER_HIT:
                ghost_health -= 1
                BLAST_HIT.play()

        end_text = ""
        time_text = ""

        if enemey_health <= 0:
            end_text = "PLAYER WINS!"
            time_text = "Restarting"

        if ghost_health <= 0:
            end_text = "ENEMIES WIN!"
            time_text = "Restarting"

        if end_text != "":
            draw_win(end_text, time_text)
            break

        # get player input
        keys_pressed = pygame.key.get_pressed()

        #ghost_movement_handler(keys_pressed, ghostplayer)
        #ghost_controller_movement_handler(joysticks, ghostplayer)

        ghost_blasts_handler(ghost_blasts, enemymonster, ghostplayer)

        #monster_mover_handler(enemymonster)


        sprite_group.draw(WIN) #this is what draws in the map, but the map is there still when commented, so i need to move this camera?


        camera_group.update(joysticks)
        camera_group.custom_draw()

        draw_window(ghostplayer, enemymonster, ghost_blasts, ghost_health, enemey_health, ship_rotate_val)
    
    main()


if __name__ == "__main__":
    main()
'''
