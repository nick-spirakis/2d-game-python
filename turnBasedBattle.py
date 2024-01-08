import pygame
import sys
import time #added for animations

class TurnBasedBattle:
    def __init__(self, level, player, player_data, enemy_boss, levelNum, overlay):

        self.level = level
        self.levelNum = levelNum

        self.player = player
        self.enemy_boss = enemy_boss
        
        self.enemy_boss.pos.x = 870 #870
        self.enemy_boss.pos.y = 400 #400

        self.battle_surface = pygame.display.get_surface()
        
        self.menu_options = ["Attack", "Magic", "Item", "Run"]
        self.selected_option = 0
        self.is_player_turn = True

        self.menu_width = 300
        self.menu_height = 200
        self.menu_x = 50
        self.menu_y = 50
        self.option_colors = [(255, 255, 255)] * len(self.menu_options)

        self.current_attck_name = "" #enemy attack name
        self.player_data = player_data
        self.overlay = overlay

        self.main_menu_nav = True
        #----------------------------------------------------------------

        # player attack
        self.draw_attack = False
        self.attack_options = ['Attack 1', 'Attack 2', 'Attack 3']
        self.attack_colors = [(255, 255, 255)] * len(self.attack_options)
        self.selected_attack = 0
        
        self.attack_menu_nav = False
        self.selected_attack_option = ""
        #----------------------------------------------------------------

        # player magic
        self.draw_magic = False
        #self.magic_options = ['Magic 1', 'Magic 2', 'Magic 3']
        self.spell_book = self.player_data.spell_book #ADDED
        self.magic_options = [self.spell_book[0], self.spell_book[1], self.spell_book[2]]

        self.magic_colors = [(255, 255, 255)] * len(self.magic_options)
        self.selected_magic = 0
        
        self.magic_menu_nav = False
        self.selected_magic_option = ""
        #----------------------------------------------------------------

        # player item
        self.draw_item = False
        self.item_options = ['Item 1', 'Item 2', 'Item 3']
        self.item_colors = [(255, 255, 255)] * len(self.item_options)
        self.selected_item = 0
        
        self.item_menu_nav = False
        self.selected_item_option = ""

        self.escape = False

        #flash on hit:
        FLASH_EVENT = pygame.USEREVENT + 1

        self.enemy_image = pygame.image.load('./Assets/boss_image_border.png')
        self.scaled_enemy_image = pygame.transform.scale(self.enemy_image, (int(self.enemy_image.get_width() * 1.8), int(self.enemy_image.get_height() * 1.8)))


    def draw_menu(self, option_colors): #main player menu
        menu_background = pygame.Surface((self.menu_width, self.menu_height))
        menu_background.fill((0, 0, 255))

        pygame.draw.rect(menu_background, (255,255,255), menu_background.get_rect(), 2)

        self.battle_surface.blit(menu_background, (self.menu_x, self.menu_y))

        menu_font = pygame.font.Font(None, 36)
        for i, (option, color) in enumerate(zip(self.menu_options, option_colors)):
            text = menu_font.render(option, True, color)
            text_rect = text.get_rect()
            text_rect.center = (self.menu_x + self.menu_width // 2, self.menu_y + 40 + i * 40)
            self.battle_surface.blit(text, text_rect)


    def handle_input(self, event):
        if self.is_player_turn:

            if event.type == pygame.KEYDOWN:

                if self.main_menu_nav:
                    print("IN MAIN MENU NAV")
                    if event.key == pygame.K_w:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                        print(self.menu_options[self.selected_option])
                        self.update_option_colors()
                    
                    elif event.key == pygame.K_s:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                        print(self.menu_options[self.selected_option])
                        self.update_option_colors()
                    
                    elif event.key == pygame.K_RETURN:
                        selected_action = self.menu_options[self.selected_option]

#------------------------------------------------------------------------------------------------------------------
                        if selected_action == "Attack":
                            self.draw_attack = True

                            self.main_menu_nav = False
                            self.attack_menu_nav = True
                            self.open_attack()
                            self.selected_attack = 0
                            self.attack_colors = [(0,255,255) if i == self.selected_attack else (255,255,255) for i in range(len(self.attack_options))]
#---------------------------------------------------------------------------------------------------------------------
                        elif selected_action == "Magic":
                            self.draw_magic = True
                            self.main_menu_nav = False
                            self.magic_menu_nav = True
                            self.open_magic()
                            self.selected_magic = 0
                            self.magic_colors = [(0,255,255) if i == self.selected_magic else (255,255,255) for i in range(len(self.magic_options))]
                            
# --------------------------------------------------------------------------------------------------------------------
                        elif selected_action == "Item":
                            self.draw_item = True
                            self.main_menu_nav = False
                            self.item_menu_nav = True
                            self.open_item()
                            self.selected_item = 0
                            self.item_colors = [(0,255,255) if i == self.selected_item else (255,255,255) for i in range(len(self.item_options))]
                            
# --------------------------------------------------------------------------------------------------------------------
                        elif selected_action == "Run":
                            if self.enemy_boss.calculate_player_run_chance(): #if it is true
                                #return to level 3 HERE
                                print("ESCAPED")
                                self.escape = True
                            else:
                                print("FAILED")
                                self.enemy_turn()

# -----------------------------------------------------------------------------------------------------------------------------

                elif self.attack_menu_nav:
                    print("ATTACK MENU NAV")
                    if event.key == pygame.K_w:
                        print("Attack w")
                        self.selected_attack = (self.selected_attack - 1) % len(self.attack_options)
                        print(self.attack_options[self.selected_attack])
                        self.attack_colors = [(0,255,255) if i == self.selected_attack else (255,255,255) for i in range(len(self.attack_options))]
                        
#---------------------------------------------------------------------------------------------------------------------
                            
                    elif event.key == pygame.K_s:
                        print("Attack s")
                        self.selected_attack = (self.selected_attack + 1) % len(self.attack_options)
                        print(self.attack_options[self.selected_attack])
                        self.attack_colors = [(0,255,255) if i == self.selected_attack else (255,255,255) for i in range(len(self.attack_options))]
                    
                            
                    elif event.key == pygame.K_RETURN:
                        print("Attack shift")
                        selected_attack_option = self.attack_options[self.selected_attack]
                        self.selected_attack_option = self.attack_options[self.selected_attack]

                        self.draw_attack = False

                        if selected_attack_option == "Attack 1":
                            print("attack 1")
                            self.close_attack()
                            self.is_player_turn = False
                            self.attack_menu_nav = False
                            self.draw_attack = False

                            # Call the attack animation function when an attack is selected
                            self.player_attack() #added for damage
                            self.play_attack_animation()
                        
                            # switch to enemy turn
                            if self.enemy_boss.get_boss_health() > 0:
                                self.enemy_turn()
                            

                        if selected_attack_option == "Attack 2":
                            print("attack 2")
                            self.close_attack()
                            self.is_player_turn = False
                            self.attack_menu_nav = False 
                            self.draw_attack = False

                            # switch to enemy turn
                            self.enemy_turn()
                        
                        if selected_attack_option == "Attack 3":
                            print("attack 3")
                            self.close_attack()
                            self.is_player_turn = False
                            self.attack_menu_nav = False
                            self.draw_attack = False
                        
                            # switch to enemy turn
                            self.enemy_turn()

# magic --------------------------------------------------------------------------------------------------------------------------------------------------
                elif self.magic_menu_nav:
                    print("MAGIC MENU NAV")
                    if event.key == pygame.K_w:
                        print("Magic w")
                        self.selected_magic = (self.selected_magic - 1) % len(self.magic_options)
                        print(self.magic_options[self.selected_magic])
                        self.magic_colors = [(0,255,255) if i == self.selected_magic else (255,255,255) for i in range(len(self.magic_options))]
                        

                    elif event.key == pygame.K_s:
                        print("Magic s")
                        self.selected_magic = (self.selected_magic + 1) % len(self.magic_options)
                        print(self.magic_options[self.selected_magic])
                        self.magic_colors = [(0,255,255) if i == self.selected_magic else (255,255,255) for i in range(len(self.magic_options))]
                    
                            
                    elif event.key == pygame.K_RETURN:
                        print("Magic shift")
                        selected_magic_option = self.magic_options[self.selected_magic]
                        self.selected_magic_option = self.magic_options[self.selected_magic]

                        self.draw_magic = False

                        if selected_magic_option == self.magic_options[0]:
                            #print("magic 1")
                            print(self.magic_options[0])
                            self.close_magic()
                            self.is_player_turn = False
                            self.magic_menu_nav = False
                            self.draw_magic = False
                            self.player_magic() #added for damage

                            self.enemy_turn()

                        if selected_magic_option == self.magic_options[1]:
                            #print("magic 2")
                            print(self.magic_options[1])
                            self.close_magic()
                            self.is_player_turn = False
                            self.magic_menu_nav = False 
                            self.draw_magic = False

                            self.enemy_turn()
                        
                        if selected_magic_option == self.magic_options[2]:
                            #print("magic 3")
                            print(self.magic_options[2])
                            self.close_magic()
                            self.is_player_turn = False
                            self.magic_menu_nav = False
                            self.draw_magic = False

                            self.enemy_turn()

# ITEM ---------------------------------------------------------------------------------------------------------------------------
                elif self.item_menu_nav:
                    print("ITEM MENU NAV")
                    if event.key == pygame.K_w:
                        print("Item w")
                        self.selected_item = (self.selected_item - 1) % len(self.item_options)
                        print(self.item_options[self.selected_item])
                        self.item_colors = [(0,255,255) if i == self.selected_item else (255,255,255) for i in range(len(self.item_options))]
                        

                    elif event.key == pygame.K_s:
                        print("Item s")
                        self.selected_item = (self.selected_item + 1) % len(self.item_options)
                        print(self.item_options[self.selected_item])
                        self.item_colors = [(0,255,255) if i == self.selected_item else (255,255,255) for i in range(len(self.item_options))]
                    
                            
                    elif event.key == pygame.K_RETURN:
                        print("Item enter")
                        selected_item_option = self.item_options[self.selected_item]
                        self.selected_item_option = self.item_options[self.selected_item]

                        self.draw_item = False

                        if selected_item_option == "Item 1":
                            print("item 1")
                            self.close_item()
                            self.is_player_turn = False
                            self.item_menu_nav = False
                            self.draw_item = False
                            self.player_item() #added for damage

                            self.enemy_turn()

                        if selected_item_option == "Item 2":
                            print("item 2")
                            self.close_item()
                            self.is_player_turn = False
                            self.item_menu_nav = False 
                            self.draw_item = False

                            self.enemy_turn()
                        
                        if selected_item_option == "Item 3":
                            print("item 3")
                            self.close_item()
                            self.is_player_turn = False
                            self.item_menu_nav = False
                            self.draw_item = False

                            self.enemy_turn()



    def update_option_colors(self):
        self.option_colors = [(0, 255, 255) if i == self.selected_option else (255, 255, 255) for i in range(len(self.menu_options))]

# --------------------------------------------------------------------------------------------------------------------
    def player_attack(self):
        damage = self.enemy_boss.calculate_player_attack_damage()
        self.enemy_boss.take_damage(damage)
        self.draw_health_bar() #added, updates the boss healthbar

    #*************************************************************************************************
    def play_attack_animation(self):
            
        # player attack animation 
        temp_player_surface = pygame.Surface((40, 40))  # temp surface for the animation
        
        temp_player_surface.fill((0, 0, 0))

        attack = pygame.image.load('Assets/new_character/right_sword/1.png')
        self.player.swing.play()

        temp_player_surface.blit(attack, (0, 0))

        self.copy_battle_surface2 = self.battle_surface.copy()

        # Blit the temporary surface onto the battle surface
        self.battle_surface.blit(temp_player_surface, (620, 340))

        # Display the temporary surface
        temp_player_surface.blit(self.battle_surface, (0, 0))
        pygame.display.flip()

        # Delay for the animation
        time.sleep(0.09)

        # Clear the temporary surface
        temp_player_surface.fill((0, 0, 0, 0))  # ((0,0,0,0)) is to fill with transparant

        # Blit the updated temporary surface onto the battle surface
        self.battle_surface.blit(temp_player_surface, (0, 0))

        # Display the updated battle surface
        self.battle_surface.blit(self.copy_battle_surface2, (0, 0))

        #-----------------------------------------------------------------------------------------------

        # Enemy hit animations
        temp_surface = pygame.Surface((60, 80))  # Temporary surface for the animation
        
        temp_surface.fill((0, 0, 0))

        hit = pygame.image.load('Assets/boss/hit/flashBoss.png')

        temp_surface.blit(hit, (0, 0))

        self.copy_battle_surface = self.battle_surface.copy()

        # Blit the temporary surface onto the battle surface
        self.battle_surface.blit(temp_surface, (900, 300))

        # Display the temporary surface
        temp_surface.blit(self.battle_surface, (0, 0))
        pygame.display.flip()

        # Delay for the animation
        time.sleep(0.09)

        # Clear the temporary surface to reveal the original content
        temp_surface.fill((0, 0, 0, 0)) 

        # Blit the updated temporary surface onto the battle surface
        self.battle_surface.blit(temp_surface, (0, 0))

        # Display the updated battle surface
        self.battle_surface.blit(self.copy_battle_surface, (0, 0))

        pygame.display.flip()

    
    def play_enemy_attack_animation(self):

        #enemy attack animation
        temp_surface = pygame.Surface((80, 80))  # Temporary surface for the animation
        
        temp_surface.fill((0, 0, 0))

        self.copy_battle_surface = self.battle_surface.copy()

        
        attack = pygame.image.load('Assets/boss/attack1/0.png')
        temp_surface.blit(attack, (0, 0))
        self.battle_surface.blit(temp_surface, (880, 300))
        pygame.display.flip()
        time.sleep(0.1)

        attack = pygame.image.load('Assets/boss/attack1/1.png')
        temp_surface.blit(attack, (0, 0))
        self.battle_surface.blit(temp_surface, (880, 300))
        pygame.display.flip()
        time.sleep(0.1)

        attack = pygame.image.load('Assets/boss/attack1/2.png')
        temp_surface.blit(attack, (0, 0))
        # Blit the temporary surface onto the battle surface
        self.battle_surface.blit(temp_surface, (880, 300))


        # Display the temporary surface
        temp_surface.blit(self.battle_surface, (0, 0))
        pygame.display.flip()

        # Delay for the animation
        time.sleep(0.09)

        # Clear the temporary surface to reveal the original content
        temp_surface.fill((0, 0, 0, 0))

        # Blit the updated temporary surface onto the battle surface
        self.battle_surface.blit(temp_surface, (0, 0))

        # Display the updated battle surface
        self.battle_surface.blit(self.copy_battle_surface, (0, 0))

        #-----------------------------------------------------------------------
        # player hit animation 
        temp_player_surface = pygame.Surface((40, 40)) # Temporary surface for the animation
        
        temp_player_surface.fill((0, 0, 0))

        hit = pygame.image.load('Assets/new_character/hit/hit.png')

        temp_player_surface.blit(hit, (0, 0))

        self.copy_battle_surface2 = self.battle_surface.copy()

        # Blit the temporary surface onto the battle surface
        self.battle_surface.blit(temp_player_surface, (620, 340))

        # Display the temporary surface
        temp_player_surface.blit(self.battle_surface, (0, 0))
        pygame.display.flip()

        self.player.hit.play()

        # Delay for the animation
        time.sleep(0.09) 

        # Clear the temporary surface to reveal the original content
        temp_player_surface.fill((0, 0, 0, 0)) 

        # Blit the updated temporary surface onto the battle surface
        self.battle_surface.blit(temp_player_surface, (0, 0))

        # Display the updated battle surface
        self.battle_surface.blit(self.copy_battle_surface2, (0, 0))
        pygame.display.flip()


    def open_attack(self):
        self.attack_options = ['Attack 1', 'Attack 2', 'Attack 3']
        self.selected_attack = 0
        self.main_menu_nav = False


    def close_attack(self):
        self.draw_attack = False
        print("closing attack menu")


    def draw_attack_menu(self, attack_colors):
        if self.draw_attack == True:
            menu_background = pygame.Surface((self.menu_width + 100, self.menu_height - 10))
            menu_background.fill((0, 0, 255))

            pygame.draw.rect(menu_background, (255,255,255), menu_background.get_rect(), 2)

            self.battle_surface.blit(menu_background, (self.menu_x, self.menu_y + 200))

            menu_font = pygame.font.Font(None, 36)
            for i, (option, color) in enumerate(zip(self.attack_options, attack_colors)):
                text = menu_font.render(option, True, color)
                text_rect = text.get_rect()
                text_rect.center = (self.menu_x + self.menu_width // 2, self.menu_y + 250 + i * 40)
                self.battle_surface.blit(text, text_rect)
                
    # ==============================================================================================================

    def player_magic(self):
        damage = self.enemy_boss.calculate_player_magic_damage()
        self.enemy_boss.take_damage(damage)

    def open_magic(self):
        #self.magic_options = ['Magic 1', 'Magic 2', 'Magic 3']
        self.magic_options = [self.spell_book[0], self.spell_book[1], self.spell_book[2]] #added spellbook
        self.selected_magic = 0
        self.main_menu_nav = False


    def close_magic(self):
        self.draw_magic = False
        print("closing magic menu")


    def draw_magic_menu(self, magic_colors):
        if self.draw_magic == True:
            menu_background = pygame.Surface((self.menu_width + 100, self.menu_height - 10))
            menu_background.fill((0, 0, 255))

            pygame.draw.rect(menu_background, (255,255,255), menu_background.get_rect(), 2)

            self.battle_surface.blit(menu_background, (self.menu_x, self.menu_y + 200))

            #old below
            menu_font = pygame.font.Font(None, 36)
            for i, (option, color) in enumerate(zip(self.magic_options, magic_colors)):
                text = menu_font.render(option, True, color)
                text_rect = text.get_rect()
                text_rect.center = (self.menu_x + self.menu_width // 2, self.menu_y + 250 + i * 40)
                self.battle_surface.blit(text, text_rect)

    # ================================================================================================================
    
    def player_item(self):
        damage = self.enemy_boss.calculate_player_item_damage()
        self.enemy_boss.take_damage(damage)

    def open_item(self):
        self.item_options = ['Item 1', 'Item 2', 'Item 3']
        self.selected_item = 0
        self.main_menu_nav = False

    def close_item(self):
        self.draw_item = False
        print("closing item menu")

    def draw_item_menu(self, item_colors):
        if self.draw_item == True:
            menu_background = pygame.Surface((self.menu_width + 100, self.menu_height - 10))
            menu_background.fill((0, 0, 255))

            pygame.draw.rect(menu_background, (255,255,255), menu_background.get_rect(), 2)

            self.battle_surface.blit(menu_background, (self.menu_x, self.menu_y + 200))

            #old below
            menu_font = pygame.font.Font(None, 36)
            for i, (option, color) in enumerate(zip(self.item_options, item_colors)):
                text = menu_font.render(option, True, color)
                text_rect = text.get_rect()
                text_rect.center = (self.menu_x + self.menu_width // 2, self.menu_y + 250 + i * 40)
                self.battle_surface.blit(text, text_rect)
    # ---------------------------------------------------------------------------------------------------------------


    def enemy_turn(self):
        time.sleep(1)
        print("enemy selecting attack")
        self.current_attck_name = (f"Used: {self.enemy_boss.select_random_attack() }")
        
        print(self.current_attck_name)
        print(" enemy attacking ")

        #animate attacks

        self.play_enemy_attack_animation()

        enemy_damage = self.enemy_boss.calculate_damage()

        self.enemy_boss.player_take_damage_turn_based(enemy_damage)
        
        # Check if the battle is over
        if self.enemy_boss.is_player_defeated():
            print("player dead")
            #self.return_to_level()
        else:
            print("back to players turn")
            self.is_player_turn = True
            self.main_menu_nav = True


# ********************************************************************************
    def player_turn(self):
        self.draw_menu(self.option_colors)
        selected_action = self.menu_options[self.selected_option]

        if selected_action == "Attack":
            self.attack_menu_nav = True

        elif selected_action == "Magic":
            self.magic_menu_nav = True
        
        elif selected_action == "Item":
            self.item_menu_nav = True

                    

# ********************************************************************************

    def return_to_level(self):
        if self.level.levelNum == 5:
            if self.level.levelNum != 3:
                self.level.levelNum = None
                
                self.level.collision_sprites.empty()
                self.level.boss_sprites.empty()
                if self.level.boss_bg:
                    self.level.boss_bg.kill()

                self.level.levelNum = 3
                self.level.setupThree()
        else:
            # should do other level transitions here if i want
            pass

    
    def display_attack_name(self, attack_name, enemy_image):
        menu_background = pygame.Surface((self.menu_width, self.menu_height))
        menu_background.fill((0, 0, 255))
        pygame.draw.rect(menu_background, (255,255,255), menu_background.get_rect(), 2)
        self.battle_surface.blit(menu_background, (self.menu_x, self.menu_y - 50))


        #display the attack name on the battle surface
        attack_font = pygame.font.Font(None, 36)
        attack_text = attack_font.render(attack_name, True, (255, 255, 255))

        text_x = self.menu_x + self.menu_width - attack_text.get_width() - 30
        attack_rect = attack_text.get_rect(topleft=(text_x, self.menu_y - 30))
        
        
        self.battle_surface.blit(attack_text, attack_rect)

        #display the enemy image
        enemy_rect = enemy_image.get_rect()
        enemy_rect.topleft = (self.menu_x + 10, self.menu_y - 47)
        self.battle_surface.blit(enemy_image, enemy_rect)


#==================================
    def clear_attack_menu(self):
        clear_surface = pygame.Surface((self.menu_width + 100, self.menu_height - 10))
        clear_surface.fill((0, 0, 0))

        menu_rect = clear_surface.get_rect()
        menu_rect.topleft = (self.menu_x, self.menu_y + 200)

        self.battle_surface.blit(clear_surface, menu_rect)
        pygame.display.update(menu_rect)
    
    def draw_health_bar(self):
        boss_health_percentage = self.enemy_boss.get_boss_health()
        health_bar_width = int((boss_health_percentage/100) * self.enemy_boss.max_health)

        pygame.draw.rect(self.battle_surface, 'gray', (self.enemy_boss.pos.x, self.enemy_boss.pos.y, self.enemy_boss.max_health, 4))
        pygame.draw.rect(self.battle_surface, 'red', (self.enemy_boss.pos.x, self.enemy_boss.pos.y, health_bar_width, 4))

#=====================================

    def run(self):

        while True:  #main battle loop start
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_input(event)

            #update healthbar in battle
            self.player_data.health = self.player.health 
            self.overlay.update_overlay(self.player_data)

            #boss dead
            if self.enemy_boss.is_defeated():
                print("boss defeated returning to map 3")
                break
            #player dead
            if self.enemy_boss.is_player_defeated():
                print("player defeated returning to map 3")
                break
            #escape success
            if self.escape == True:
                print("Escape Success")
                break #this returns to level 3


            if self.draw_attack:
                self.draw_attack_menu(self.attack_colors)

            elif self.draw_attack == False and self.draw_magic == False and self.draw_item == False:
                self.clear_attack_menu()
                self.draw_attack = False
            # -----------------------------------------
            if self.draw_magic:
                self.draw_magic_menu(self.magic_colors)
            elif self.draw_magic == False and self.draw_attack == False and self.draw_item == False:
                self.clear_attack_menu()
                self.draw_magic = False
            # ---------------------------------------
            if self.draw_item:
                self.draw_item_menu(self.item_colors)
            elif self.draw_attack == False and self.draw_magic == False and self.draw_item == False:
                self.clear_attack_menu()
                self.draw_item = False
            # ---------------------------------------

            if self.current_attck_name:
                self.display_attack_name(self.current_attck_name, self.scaled_enemy_image) #added enemy image

            #draw the menu
            self.draw_menu(self.option_colors)

            #update the display
            pygame.display.flip()
        
