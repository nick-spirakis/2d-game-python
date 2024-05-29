import pygame
from settings import *

from shop import Shop
from player import PlayerData

class Overlay:
    def __init__(self, player, player_data): #was player

        #general overlay
        self.display_surface = pygame.display.get_surface()
        self.player_data = player_data  
        self.player = player
        
        #new UI
        self.font = pygame.font.SysFont('arial', 20) #pygame.font.Font(UI_FONT, UI_FONT_SIZE)  
        #bar setup
        self.health_bar_rect = pygame.Rect(70, SCREEN_HEIGHT-40, HEALTH_BAR_WIDTH + 5, BAR_HEIGHT + 5)


        #imports
        overlay_path = './Graphics/Overlay/'
        self.items_surf = {item:pygame.image.load(f'{overlay_path}{item}.png').convert_alpha() for item in player.items}
        print(self.items_surf)

    def show_bars(self, current_amount, max_amount, bg_rect, color):
        # background
        pygame.draw.rect(self.display_surface, 'gray', bg_rect)

        # convert stats to pixel
        ratio = current_amount / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        # hearts
        self.heart_image = pygame.image.load('./Assets/empty_health_bar_heart_10.png') #3
        self.scaled_heart_image = pygame.transform.scale(self.heart_image, (int(self.heart_image.get_width() * 0.91), int(self.heart_image.get_height() * 0.8))) #(*1, *0.8)

        heart_rect = self.heart_image.get_rect(bottomleft= (self.display_surface.get_size()[0] - 1210, self.display_surface.get_size()[1]- 10))

        self.display_surface.blit(self.scaled_heart_image, heart_rect)

    '''
    def show_exp(self): #, exp):
        
        exp = self.player_data.experience
        
        text_surf = self.font.render(f"Exp: {int(exp)}", False, 'black')
        
        #text_surf = self.font.render(f"Exp: {int(self.player_data.experience)}", False, 'black')

        #text_surf = self.font.render(str(int(exp)), False, 'black')
        text_rect = text_surf.get_rect(bottomright=(self.display_surface.get_size()[0] - 20, self.display_surface.get_size()[1] - 70))

        pygame.draw.rect(self.display_surface, 'gold', text_rect.inflate(10, 10))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(10, 10), 3)
        self.display_surface.blit(text_surf, text_rect)

        # Calculate the level based on experience
        level = self.player_data.player_level
        level_text = self.font.render(f"Level: {level}", False, 'black')
        level_rect = level_text.get_rect(bottomright=(text_rect.topleft[0] - 10, text_rect.bottom))

        pygame.draw.rect(self.display_surface, 'gold', level_rect.inflate(10, 10))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, level_rect.inflate(10, 10), 3)
        self.display_surface.blit(level_text, level_rect)

    '''
    def show_exp(self):

        if self.player_data.experience >= self.player_data.max_experience:
            self.player_data.player_level += 1
            self.player_data.experience -= self.player_data.max_experience
            
        exp = self.player_data.experience

        self.display_exp(exp)

        level = self.player_data.player_level
        self.display_level(level)

    def display_exp(self, exp):
        text_surf = self.font.render(f"Exp: {int(exp)} /50", False, 'black')
        text_rect = text_surf.get_rect(bottomright=(self.display_surface.get_size()[0] - 20, self.display_surface.get_size()[1] - 70))

        pygame.draw.rect(self.display_surface, 'gold', text_rect.inflate(10, 10))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(10, 10), 3)
        self.display_surface.blit(text_surf, text_rect)

    def display_level(self, level):
        text_surf = self.font.render(f"Lvl: {level}", False, 'black')
        text_rect = text_surf.get_rect()
        text_rect.bottomright = (self.display_surface.get_size()[0] - 110, self.display_surface.get_size()[1] - 70)

        pygame.draw.rect(self.display_surface, 'gold', text_rect.inflate(10, 10))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(10, 10), 3)
        self.display_surface.blit(text_surf, text_rect)



    def show_coins(self, coin):
        #text_surf = self.font.render(str(int(coin)), False, 'black')
        text_surf = self.font.render(f"Coins: {int(coin)}", False, 'black')
        text_rect = text_surf.get_rect(bottomright= (self.display_surface.get_size()[0] -20, self.display_surface.get_size()[1] -20))

        pygame.draw.rect(self.display_surface, 'gold', text_rect.inflate(10, 10))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(10, 10), 3)
        self.display_surface.blit(text_surf, text_rect)

    def show_inventory(self, player_data):
        pd = player_data
        self.potion_count = 0
        self.hat_count = 0
        for i in pd.inventory:
            #print(i)
            if i == "hat":
                self.hat_count += 1
            elif i == "potion":
                self.potion_count += 1


        #hat
        text_surf = self.font.render(str(int(self.hat_count)), False, 'white')
        text_rect = text_surf.get_rect(bottomright= (self.display_surface.get_size()[0] -110, self.display_surface.get_size()[1] -20))
        pygame.draw.rect(self.display_surface, 'red', text_rect.inflate(10, 10))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(10, 10), 3)
        self.display_surface.blit(text_surf, text_rect)

        #potions
        text_surf2 = self.font.render(str(int(self.potion_count)), False, 'black')
        text_rect2 = text_surf2.get_rect(bottomright= (self.display_surface.get_size()[0] -140, self.display_surface.get_size()[1] -20))
        pygame.draw.rect(self.display_surface, 'green', text_rect2.inflate(10, 10))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect2.inflate(10, 10), 3)
        self.display_surface.blit(text_surf2, text_rect2)


    def display_items(self):
        #health
        #self.show_bars(self.player.health, self.player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        MAX_HEALTH = 100
        self.show_bars(self.player_data.health, MAX_HEALTH, self.health_bar_rect, HEALTH_COLOR)

        #item
        item_surf = self.items_surf[self.player.selected_item]
        item_rect = item_surf.get_rect(midbottom = OVERLAY_POSITIONS['item'])

        #added bg
        pygame.draw.rect(self.display_surface, 'gray', item_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, item_rect, 3)

        self.display_surface.blit(item_surf, item_rect)

        self.show_exp() #(self.player_data.experience)

        self.show_coins(self.player_data.coin)
        self.show_inventory(self.player_data)


    def update_overlay(self, player_data):
        current_coins = player_data.coin
        self.show_coins(current_coins)

        current_health = player_data.health
        self.show_bars(current_health, 100, self.health_bar_rect, HEALTH_COLOR)

