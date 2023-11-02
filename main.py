import pygame, sys
from settings import *
from level import Level
from player import PlayerData #added for persistence


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

    def level_change(self, level, player_data):
        self.levelSelect = level
        #persistence
        self.player_data = player_data

        self.level = Level(self.levelSelect, self.player_data)
        self.enemys = self.level.attack_sprites # if = <Group(0 sprites)> then win game
        self.player = self.level.player1 #was self.level.player

        #making doors
        self.doors = self.level.door_sprites

        #making boss
        self.boss = self.level.boss_sprites

        # music
        #self.music = [pygame.mixer.Sound("Audio/Soundtrack1-1.wav"), pygame.mixer.Sound("Audio/Soundtrack2-1.wav")]
        #self.music_index = 0
        #self.music_player = self.music[self.music_index].play(loops=1) #(loops = -1)


    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("First Fantasy 2")
        self.clock = pygame.time.Clock()
        self.levelInt = 5
         #3 is town

        #crl + ] to mass indent highlighted code

        #character persistence
        self.player_data = PlayerData()
        
    
    def run(self):
        self.level_change(self.levelInt, self.player_data) #added player data persistence

        while True:
            #check_controller()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                '''
                # controller
                if event.type == pygame.JOYDEVICEADDED:
                    print(event)
                    joy = pygame.joystick.Joystick(event.device_index)
                    self.level.joysticks.append(joy)
                # end controller
                '''

            dt = self.clock.tick() / 1000

            self.level.run(dt)
            pygame.display.update()

            if len(self.enemys) == 0 and self.levelInt <= 2: #if all enemies die
                    #self.screen
                    #end_text = "PLAYER WINS!"
                    #time_text = "Quiting"
                    #draw_win(end_text, time_text)
                    
                    self.levelInt += 1
                    self.level_change(self.levelInt, self.player_data) #added player data
                    print("level change")


            if len(self.doors) <= 0 and self.levelInt == 3: #3 to 4 shop
                self.levelInt = 4 # self.levelInt += 1
                self.level_change(self.levelInt, self.player_data) #added player data
                print("level change town to shop")

            if len(self.doors) <= 0 and self.levelInt == 4: #4 shop to 3 town
                self.levelInt = 3
                self.level_change(self.levelInt, self.player_data) #added player data
                print("level change shop to town")
                

            #town to boss
            if self.levelInt == 3 and self.player.pos.y <= 473:
                self.levelInt = 5
                self.level_change(self.levelInt, self.player_data) #added player data
                print("level change town to BOSS")


            if self.levelInt == 5:
                if len(self.boss) <= 0:
                    self.levelInt = 3
                    self.level_change(self.levelInt, self.player_data)
                    print("level change BOSS to TOWN")

              
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
