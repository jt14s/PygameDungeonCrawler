import pygame, sys, os
from pygame.locals import *
from image_loader import *
from game import *
from hud import *
from main_menu import Sprite, CursorLocation, Button, Splash, MainMenu

class GameOver(object):
    def __init__(self, width=1224, height=952):
        pygame.init()

        # misc
        self.done = False
        self.button_down = False

        # set screen variables
        self.width, self.height = width, height
        pygame.display.set_caption("Maiden Hearts")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # background group
        self.background = Splash()
        self.background_group = pygame.sprite.GroupSingle(self.background)
      
        # buttons group
        self.main_menu_button = Button(MainMenuButton, self.width / 2.8, self.height / 2)
        self.quit_game_button = Button(QuitGameButton, self.width / 2.8, self.height / 2 + 70)

        self.menu_buttons = pygame.sprite.Group()
        self.menu_buttons.add(self.main_menu_button, self.quit_game_button)

        game_over_font1 = pygame.font.SysFont(None, 150)
        self.game_over_text = game_over_font1.render('GAME OVER', 0, (255,255,255))

    def game_over_loop(self):
        
        while not self.done:
            self.handle_events()
            self.draw()

            
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.done = True

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left mouse down

                    self.button_down = True
                    cursor = CursorLocation(event.pos)
                    click = pygame.sprite.GroupSingle(cursor)

                    button_click_list = pygame.sprite.groupcollide(self.menu_buttons, click, False, False)
                    cursor.kill()

                    for button in button_click_list:
                        if button == self.main_menu_button:
                            self.clean()
                            os.execl(sys.executable, sys.executable, *sys.argv)

                        elif button == self.quit_game_button:
                            self.clean()
                            pygame.quit()
                            quit()



    def draw(self):
        self.background_group.draw(self.screen)
        self.menu_buttons.draw(self.screen)
        self.background_group.update()
        
        self.screen.blit(self.game_over_text, (self.width/2.8 - 110, self.height/2.5 - 70))

        pygame.display.flip()

    def clean(self):
        del self.background
        del self.background_group
        del self.main_menu_button
        del self.quit_game_button
        del self.menu_buttons


if __name__ == "__main__":
    gameover = GameOver()
    gameover.game_over_loop()
