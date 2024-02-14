import pygame, sys, json, os
from settings import *
from level import Level
from player import PlayerData #added for persistence

from party import Party #added for party system
from partyMembers import PartyMember

from mainMenu import MainMenu

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
    #pygame.time.delay(2000) #2 sec


class Game:

    def level_change(self, level, player_data):
        self.levelSelect = level
        #persistence
        self.player_data = player_data

        self.level = Level(self.levelSelect, self.player_data)
        self.enemys = self.level.attack_sprites # if = <Group(0 sprites)> then win game
        self.player = self.level.player1

        #making doors
        self.doors = self.level.door_sprites

        #making boss
        self.boss = self.level.boss_sprites


    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("First Fantasy 2")
        self.clock = pygame.time.Clock()

        #self.levelInt = 1
        #3 is town, 5 is a boss fight
       
        #crl + ] to mass indent highlighted code

        # load the player data
        loaded_data = self.load_player_data()

        # set loaded data to be player_data
        if loaded_data:
           self.player_data = PlayerData.from_dict(loaded_data)
           self.levelInt = self.player_data.levelInt

        else:
            self.levelInt = 1
            self.player_data = PlayerData()
            pass

        #main menu
        self.main_menu = MainMenu()
        
    #-------------------------------------------------------------------------------------------------------------------


    def save_player_data(self, player_data):
        folder_path = './Saves/'
        file_path = os.path.join(folder_path, 'player_data.json')

        # convert player data to a dictionary
        data = {
            'health': player_data.health,
            'experience': player_data.experience,
            'coin': player_data.coin,
            'inventory': player_data.inventory,
            'spell_book': player_data.spell_book,
            'levelInt': player_data.levelInt
        }

        # save data to a JSON
        with open(file_path, 'w') as file:
            json.dump(data, file)

        print(f"Player data saved to: {file_path}")


    def load_player_data(self):

        folder_path = './Saves/'
        file_path = os.path.join(folder_path, 'player_data.json')

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print("File not found.")
            return None
        except json.JSONDecodeError:
            print("Error decoding JSON.")
            return None
        

    def delete_player_data(self):
        folder_path = './Saves/'
        file_path = os.path.join(folder_path, 'player_data.json')

        try:
            os.remove(file_path)
            print(f"Player data deleted: {file_path}")
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"Error deleting player data: {e}")

    #-------------------------------------------------------------------------------------------------------------------
        
    def menu(self):
        while True:
            self.music = [pygame.mixer.Sound("Audio/Menu2.wav")]
            self.music_index = 0
            self.music_player = self.music[self.music_index].play(loops=-1) #(loops = -1)

            menu_result = self.main_menu.run()

            if menu_result == "new_game":
                self.delete_player_data()
                self.music_player.pause()
                game = Game()
                game.run()

            elif menu_result == "load_game":
                loaded_data = self.load_player_data()
                if loaded_data:
                    self.music_player.pause()
                    game = Game()
                    game.run()
        
    
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

                    elif event.key == pygame.K_n:
                        # trying to add a manual save option here
                        print("N PRESSED")
                        self.save_player_data(self.player_data)
                        # so saved does not always work, maybe because of how events are tracked
                        draw_win("Saving", "Save Complete")


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

            if len(self.enemys) == 0 and self.levelInt <= 2: #if all enemies defeated
                    #self.screen
                    #end_text = "PLAYER WINS!"
                    #time_text = "Quiting"
                    #draw_win(end_text, time_text)
                    
                    self.levelInt += 1
                    self.player_data.levelInt += 1
                    
                    #adding a save here
                    self.save_player_data(self.player_data)

                    self.level_change(self.levelInt, self.player_data)
                    print("level change")


            if len(self.doors) <= 0 and self.levelInt == 3: #3 to 4 shop
                self.levelInt = 4 
                self.player_data.levelInt = 4 #added 12/26

                #adding a save here
                self.save_player_data(self.player_data)

                self.level_change(self.levelInt, self.player_data)
                print("level change town to shop")

            if len(self.doors) <= 0 and self.levelInt == 4: #4 shop to 3 town
                self.levelInt = 3
                self.player_data.levelInt = 3 #added 12/26

                #adding a save here
                self.save_player_data(self.player_data)
                
                self.level_change(self.levelInt, self.player_data) 
                print("level change shop to town")
                

            #town to boss
            if self.levelInt == 3 and self.player.pos.y <= 473:
                self.levelInt = 5
                self.player_data.levelInt = 5 #added 12/26

                #adding a save here
                self.save_player_data(self.player_data)
                
                self.level_change(self.levelInt, self.player_data) 
                print("level change town to BOSS")


            if self.levelInt == 5:
                if len(self.boss) <= 0:
                    self.levelInt = 3
                    self.player_data.levelInt = 3 #added 12/26

                    #adding a save here
                    self.save_player_data(self.player_data)
                    
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
    #game.run()
    game.menu()
