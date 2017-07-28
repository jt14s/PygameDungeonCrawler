import pygame, sys, os
from pygame.locals import *
from image_loader import *
from game import *
from hud import *
from main_menu import Sprite, CursorLocation, Button, Splash, MainMenu

#rename buttons and replace logo with Game Over

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
        self.logo = Sprite(GameLogo, self.width / 6, 0)
        self.background_group = pygame.sprite.GroupSingle(self.background)
        self.logo_group = pygame.sprite.GroupSingle(self.logo)

        # buttons group
        self.single_mode_button = Button(SingleplayerButton, self.width / 2.8, self.height / 2)
        self.multi_mode_button = Button(MultiplayerButton, self.width / 2.8, self.height / 2 + 70)

        self.menu_buttons = pygame.sprite.Group()
        self.menu_buttons.add(self.single_mode_button, self.multi_mode_button)

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
                        if button == self.single_mode_button:
                            self.clean()
                            os.execl(sys.executable, sys.executable, *sys.argv)

                        elif button == self.multi_mode_button:
                            self.clean()
                            pygame.quit()
                            quit()



    def draw(self):
        self.background_group.draw(self.screen)
        self.logo_group.draw(self.screen)
        self.menu_buttons.draw(self.screen)
        self.background_group.update()

        pygame.display.flip()

    def clean(self):
        del self.background
        del self.logo
        del self.logo_group
        del self.background_group
        del self.single_mode_button
        del self.multi_mode_button
        del self.menu_buttons


if __name__ == "__main__":
    gameover = GameOver()
    gameover.game_over_loop()
