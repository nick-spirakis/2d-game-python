import pygame
from settings import *

from player import PlayerData

class Shop:
    def __init__(self, player_data, overlay):
        self.overlay = overlay

        self.display_surface = pygame.display.get_surface()
        self.player_data = player_data

        self.item_prices = {
            'merchants shop': 0, 
            'hat': 10, 
            'potion': 5
            }
        
        self.selected_option = 0
        self.font = pygame.font.SysFont('arial', 20)
        self.shop_open = False


    def navigate_options(self, key_events):

        for event in key_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    #print("w press")
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                    print(self.selected_option) #merchant shop 0, hat is 1, potion is 2
            
                elif event.key == pygame.K_s:
                    #print("k press")
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                    print(self.selected_option)


    def get_selected_item_index(self):
        return self.selected_option


    def show_menu(self, options):
        rect_w = 200
        rect_h = 30
        menu_x = self.display_surface.get_size()[0] - 300 - rect_w
        menu_y = self.display_surface.get_size()[1] - 500

        for i, option in enumerate(options):
            text = f"{option} - {self.item_prices.get(option, 'N/A')} coins"
            if option == "merchants shop":
                text = "merchant's shop"

            option_rect = pygame.Rect(
                menu_x,
                menu_y + i * rect_h,
                rect_w,
                rect_h
            )

            text_surf = self.font.render(text, False, 'black')
            text_rect = text_surf.get_rect(center=option_rect.center)

            # Add a blue background and a white border
            pygame.draw.rect(self.display_surface, 'blue', option_rect)
            pygame.draw.rect(self.display_surface, 'white', option_rect, 3)

            if i == self.selected_option:
                pygame.draw.rect(self.display_surface, 'white', option_rect)

            self.display_surface.blit(text_surf, text_rect)


    def open_shop1(self):
        self.options = ['merchants shop', 'hat', 'potion']
        self.selected_option = 0
        self.show_menu(self.options)
        self.shop_open = True


    def close_shop1(self):
        self.shop_open = False


    def is_open(self):
        return self.shop_open


    def buy_item(self, item, player_data):

        pd = player_data

        if item == "merchants shop":
            print("you tried to buy merchants shop")
            return False

        if item in self.item_prices:
            price = self.item_prices[item]

            if pd.get_coins() >= price:

                pd.update_coins(pd.get_coins() - price)
                print("item purchased")

                #add to inv
                self.player_data.inventory.append(item)

            else:
                print("Not enough coins to purchase")
        else:
            print("Item not in shop")

