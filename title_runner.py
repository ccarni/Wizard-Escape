import pygame
import sys
import art


class TitleRunner():
    def __init__(self):
        self.display = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((self.display.get_height(), self.display.get_height()))
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.titlescreen = art.draw_title_screen(self.screen)
        self.running = True

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    #start the real game
                    self.running = False
                    
    def draw(self):
        self.screen.blit(self.titlescreen, (0, 0))
        pygame.display.update()