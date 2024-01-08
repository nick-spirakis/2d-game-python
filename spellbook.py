
import pygame
from settings import *

from player import PlayerData

class Spellbook:
    def __init__(self, player_data, overlay):
        self.overlay = overlay

        self.display_surface = pygame.display.get_surface()
        self.player_data = player_data

        self.selected_spells = player_data.spell_book
        self.unlocked_spells = player_data.unlocked_spells

        self.selected_option = 0
        self.font = pygame.font.SysFont('arial', 20)
        self.book_open = False

        self.selected_total_option = 0


    def navigate_options(self, key_events):

        for event in key_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                    print(self.selected_option)

                elif event.key == pygame.K_s:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                    print(self.selected_option)


    def navigate_all_options(self, key_events):

        for event in key_events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.selected_total_option = (self.selected_total_option - 1) % len(self.total_options)
                    print(self.selected_option)

                elif event.key == pygame.K_d:
                    self.selected_total_option = (self.selected_total_option + 1) % len(self.total_options)
                    print(self.selected_total_option)


    def get_selected_item_index(self):
        return self.selected_option
    

    def get_selected_total_item_index(self):
        return self.selected_total_option


    def show_menu(self, options):
        rect_w = 200
        rect_h = 30
        menu_x = self.display_surface.get_size()[0] - 300 - rect_w
        menu_y = self.display_surface.get_size()[1] - 500

        for i, option in enumerate(options):
            text = option

            option_rect = pygame.Rect(
                menu_x,
                menu_y + i * rect_h,
                rect_w,
                rect_h
            )

            text_surf = self.font.render(text, False, 'black')
            text_rect = text_surf.get_rect(center=option_rect.center)

            # Add a blue background and a white border
            pygame.draw.rect(self.display_surface, 'orange', option_rect)
            pygame.draw.rect(self.display_surface, 'white', option_rect, 3)

            if i == self.selected_option:
                pygame.draw.rect(self.display_surface, 'white', option_rect)

            self.display_surface.blit(text_surf, text_rect)


    
    def show_all_spells(self, options):
        rect_w = 200
        rect_h = 30
        menu_x = self.display_surface.get_size()[0] - 100 - rect_w
        menu_y = self.display_surface.get_size()[1] - 500

        for i, option in enumerate(options):
            text = option

            option_rect = pygame.Rect(
                menu_x,
                menu_y + i * rect_h,
                rect_w,
                rect_h
            )

            text_surf = self.font.render(text, False, 'black')
            text_rect = text_surf.get_rect(center=option_rect.center)

            pygame.draw.rect(self.display_surface, 'red', option_rect)
            pygame.draw.rect(self.display_surface, 'white', option_rect, 3)

            if i == self.selected_total_option:
                pygame.draw.rect(self.display_surface, 'white', option_rect)

            self.display_surface.blit(text_surf, text_rect)


    def is_spell_equipped(self, spell):
        return spell in self.selected_spells

    
    def swap_spells(self):
        if self.book_open:
            selected_spell_index = self.get_selected_item_index()
            selected_total_spell_index = self.get_selected_total_item_index()

            if selected_spell_index < len(self.selected_spells) and selected_total_spell_index < len(self.unlocked_spells):
                total_spell = self.unlocked_spells[selected_total_spell_index]

                if not self.is_spell_equipped(total_spell):
                    self.selected_spells[selected_spell_index] = total_spell



    def open_spellbook(self):
        self.options = self.selected_spells

        self.selected_option = 0
        self.show_menu(self.options)


        self.total_options = self.unlocked_spells
        self.selected_total_option = 0
        self.show_all_spells(self.total_options) #2nd menu for all spells

        self.book_open = True


    def close_spellbook(self):
        self.book_open = False


    def is_open(self):
        return self.book_open


