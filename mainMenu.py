import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class MainMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('comicsans', 40)
        self.menu_options = ["New Game", "Load Game", "Quit"]
        self.selected_option = 0

        self.background_image = pygame.image.load("Graphics/start_screen2.png").convert()

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background_image, (0, 0))
        for i, option in enumerate(self.menu_options):
            color = (255, 255, 255) if i == self.selected_option else (128, 128, 128)
            text = self.font.render(option, True, color)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 300 + i * 50))

        pygame.display.update()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option == 0:
                            return "new_game"
                        elif self.selected_option == 1:
                            return "load_game"
                        elif self.selected_option == 2:
                            pygame.quit()
                            quit()

            self.draw_menu()
            self.clock.tick(30)