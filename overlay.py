import pygame
from settings import *

class Overlay:
    def __init__(self, player):

        #general overlay
        self.display_surface = pygame.display.get_surface()
        self.player = player
        
        #new UI
        self.font = pygame.font.SysFont('arial', 20) #pygame.font.Font(UI_FONT, UI_FONT_SIZE)  
        #bar setup
        self.health_bar_rect = pygame.Rect(70, SCREEN_HEIGHT-40, HEALTH_BAR_WIDTH, BAR_HEIGHT)


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


    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, 'black')
        text_rect = text_surf.get_rect(bottomright= (self.display_surface.get_size()[0] -20, self.display_surface.get_size()[1] -20))

        pygame.draw.rect(self.display_surface, 'gold', text_rect.inflate(10, 10))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(10, 10), 3)
        self.display_surface.blit(text_surf, text_rect)

    def show_coins(self, coin):
        text_surf = self.font.render(str(int(coin)), False, 'black')
        text_rect = text_surf.get_rect(bottomright= (self.display_surface.get_size()[0] -50, self.display_surface.get_size()[1] -20))

        pygame.draw.rect(self.display_surface, 'gold', text_rect.inflate(10, 10))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(10, 10), 3)
        self.display_surface.blit(text_surf, text_rect)


    def display_items(self):
        #health
        self.show_bars(self.player.health, self.player.stats['health'], self.health_bar_rect, HEALTH_COLOR)

        #item
        item_surf = self.items_surf[self.player.selected_item]
        item_rect = item_surf.get_rect(midbottom = OVERLAY_POSITIONS['item'])

        #added bg
        pygame.draw.rect(self.display_surface, 'gray', item_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, item_rect, 3)

        self.display_surface.blit(item_surf, item_rect)

        self.show_exp(self.player.exp)

        self.show_coins(self.player.item_inventory['coin'])