import pygame, sys
from pygame.locals import *
from image_loader import *
from game import *
from hud import *

# parent class for all sprite initializations
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# for use in sprite collision on cursor location
class CursorLocation(Sprite):
    def __init__(self, coords):
        Sprite.__init__(self, pygame.image.load('images/interface/cursor.png'), coords[0], coords[1])

# to create menu buttons
class Button(Sprite):
    def __init__(self, image, x, y):
        Sprite.__init__(self, image, x, y)

# to signify what character you have selected
class Selector(Sprite):
    def __init__(self, image, x, y):
        Sprite.__init__(self, image, x, y)

# to show playable characters
class Portrait(Sprite):
    def __init__(self, image, x, y, choice):
        Sprite.__init__(self, image, x, y)
        self.character_choice = choice

# the naimated background
class Splash(Sprite):
    def __init__(self):
        self.animation = [MenuSplash1, MenuSplash2, MenuSplash3, MenuSplash4, MenuSplash5, MenuSplash6]
        Sprite.__init__(self, self.animation[0], 0, 0)

        self.current_frame = 0
        self.ticker = 0

    def update(self):
        self.image = self.animation[self.current_frame]

        self.ticker += 1
        if self.ticker % 20 == 0:
            self.current_frame = (self.current_frame + 1) % 6
            self.ticker = 0

class MainMenu(object):

    def __init__(self, width=1224, height=952):
        pygame.init()

        # misc
        self.done = False
        self.button_down = False
        self.start_game = False
        self.character_choice = 'PL'

        # set screen variables
        self.width, self.height = width, height
        pygame.display.set_caption("Maiden Hearts")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # background group
        self.background = Splash()
        self.logo = Sprite(GameLogo, self.width/6, 0)
        self.background_group = pygame.sprite.GroupSingle(self.background)
        self.logo_group = pygame.sprite.GroupSingle(self.logo)

        # buttons group
        self.single_mode_button = Button(SingleplayerButton, self.width/2.8, self.height/2)
        self.multi_mode_button = Button(MultiplayerButton, self.width/2.8, self.height/2 + 70)
        self.start_game_button = Button(PlayButton, self.width/2.8, self.height - 200)

        self.menu_buttons = pygame.sprite.Group()
        self.menu_buttons.add(self.single_mode_button, self.multi_mode_button)

        # char select group
        self.character_portraits = [Portrait(PaladinPortrait, 80, height/3.5, 'PL'), Portrait(AssassinPortrait, 80 + 270, height/3.5, 'AS'),
                                    Portrait(WizardPortrait, 80 + 270 * 2, height/3.5, 'WZ'), Portrait(AlienPortrait, 80 + 270 * 3, height/3.5, 'AL')]
        self.selector = Selector(PortraitSelector, 80, height/3.5)
        self.selector_group = pygame.sprite.Group()

    def main_loop(self):
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
                if event.button == 1:   # left mouse down
                    
                    self.button_down = True
                    cursor = CursorLocation(event.pos)
                    click = pygame.sprite.GroupSingle(cursor)

                    button_click_list = pygame.sprite.groupcollide(self.menu_buttons, click, False, False)
                    cursor.kill()
                    
                    for button in button_click_list:
                        if self.single_mode_button == button:
                            self.menu_buttons.remove(self.single_mode_button, self.multi_mode_button)
                            self.logo.kill()
                            self.menu_buttons.add(self.start_game_button)

                            self.selector_group.add(self.selector)


                            for portrait in self.character_portraits:
                                self.menu_buttons.add(portrait)

                        if self.start_game_button == button:
                            self.start_game = True

                        if isinstance(button, Portrait):
                            self.character_choice = button.character_choice
                            self.selector.rect.x = button.rect.x
                            print self.character_choice

            if event.type == pygame.MOUSEBUTTONUP and self.button_down:
                self.button_down = False

                if self.start_game:
                    #delete things that wont be used again
                    game = GameMain(self.character_choice)
                    self.clean()
                    game.main_loop()
                    
    def draw(self):
        self.background_group.draw(self.screen)
        self.logo_group.draw(self.screen)
        self.menu_buttons.draw(self.screen)
        self.background_group.update()
        self.selector_group.draw(self.screen)
        
        pygame.display.flip()

    def clean(self):
        del self.background
        del self.logo
        del self.logo_group
        del self.background_group
        del self.single_mode_button
        del self.multi_mode_button
        del self.start_game_button
        del self.menu_buttons    
        del self.character_portraits
        del self.character_choice
        del self.selector
        del self.selector_group

if __name__ == "__main__":
    menu = MainMenu()
    menu.main_loop()
