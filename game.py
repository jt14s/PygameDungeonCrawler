''' Notable Problems:
    -Add a cooldown to the projectiles
'''

import pygame, random, math
from pygame.locals import *
from characters import *
from rooms import *
from game_over import *



class GameMain():
    done = False

    def __init__(self, character = 'PL', width=1224, height=700):
        pygame.init()
        #initialize joystick input
        pygame.joystick.init()
        joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

        # set screen variables
        self.width, self.height = width, height
        pygame.display.set_caption("Maiden Hearts")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.pause = False

        # create hero and necessary sprite groups
        if character == 'PL':
            self.hero = Paladin(68, 136, "DOWN", self.screen)
        elif character == 'MG':
            self.hero = Mage(68, 136, "DOWN", self.screen)
        elif character == 'AL':
            self.hero = Alien(68, 136, "DOWN", self.screen)
        elif character == 'AS':
            self.hero = Assassin(68, 136, "DOWN", self.screen)

        self.all_sprite_list = pygame.sprite.Group()
        self.all_room_tiles = pygame.sprite.Group()

        # room variables
        self.rooms = [Room1(), Room2(), Room2(), Room2(), Room2()]
        self.current_x = 1
        self.current_room = self.rooms[self.current_x]

        self.hero.current_room = self.current_room

        # access room entities
        self.hero.items = self.current_room.item_list
        self.hero.walls = self.current_room.wall_list
        self.hero.roofs = self.current_room.roof_list
        self.hero.mobs = self.current_room.mob_list
        self.hero.portals = self.current_room.portal_list

        for mob in self.current_room.mob_list:
            mob.walls = self.hero.walls
            mob.roofs = self.hero.roofs

        # load sprite groups accordingly
        self.all_room_tiles.add(self.current_room.floor_list, self.current_room.wall_list, self.current_room.item_list)
        self.all_sprite_list.add(self.hero.mobs, self.hero)

        self.ui = pygame.sprite.GroupSingle(self.hero.ui)
        self.inv = pygame.sprite.GroupSingle(self.hero.inventory)

        self.ui_font = pygame.font.SysFont(None, 20)
    
    def main_loop(self):
        while not self.done:
            if self.current_x != self.hero.current_x:
                self.current_x = self.hero.current_x

                for mob in self.current_room.mob_list:
                    mob.rect.x = mob.ORIG_X
                    mob.rect.y = mob.ORIG_Y
                
                self.current_room = self.rooms[self.current_x]
                self.hero.current_room = self.current_room
                self.hero.projectiles.empty()

                # access room entities
                self.hero.items = self.current_room.item_list
                self.hero.walls = self.current_room.wall_list
                self.hero.roofs = self.current_room.roof_list
                self.hero.portals = self.current_room.portal_list
        
                self.hero.mobs = self.current_room.mob_list
                self.hero.mobs.roofs = self.hero.roofs
                self.hero.mobs.walls = self.hero.walls

                for mob in self.current_room.mob_list:
                    mob.roofs = self.hero.mobs.roofs
                    mob.walls = self.hero.mobs.walls
                
                # load sprite groups accordingly
                self.all_room_tiles.empty()
                self.all_sprite_list.empty()

                self.all_room_tiles.add(self.current_room.floor_list, self.current_room.wall_list,
                                        self.current_room.item_list)
                self.all_sprite_list.add(self.hero.mobs, self.hero)

            self.handle_events()
            self.all_sprite_list.update()
            self.draw()
            self.clock.tick(64)

        pygame.quit()

    def clean(self):
        del self.hero
        del self.rooms

    def draw(self):

        self.all_room_tiles.draw(self.screen)
        self.current_room.item_list.draw(self.screen)
        self.all_sprite_list.draw(self.screen)

        for mob in self.current_room.mob_list:
            if mob.look_for_hero(self.hero) == True:
                mob.follow_hero(self.hero)

        self.hero.projectiles.draw(self.screen)
        self.hero.projectiles.update()

        self.current_room.portal_list.draw(self.screen)

        self.current_room.roof_list.draw(self.screen)

        self.current_room.wall_list.update()

        self.hero.ui.hp_bar.bar_group.draw(self.screen)
        self.hero.ui.sp_bar.bar_group.draw(self.screen)
        self.ui.draw(self.screen)

        health_text = self.ui_font.render(str(self.hero.hp) + "/" + str(self.hero.MAX_HP), 0, (88,88,88))
        self.screen.blit(health_text, (self.hero.ui.hp_bar.rect.x + self.hero.ui.hp_bar.image.get_width() - 80 , self.hero.ui.hp_bar.rect.y + 13))

        special_text = self.ui_font.render(str(self.hero.sp) + "/" + str(self.hero.MAX_SP), 0, (88,88,88))
        self.screen.blit(special_text, (self.hero.ui.sp_bar.rect.x + 30, self.hero.ui.sp_bar.rect.y + 13))

        self.inv.draw(self.screen)
        self.hero.item_slot_group.draw(self.screen)

        if self.hero.hp <= 0:
            self.all_sprite_list.remove(self.hero)
            self.clean()
            game_over = GameOver()
            game_over.game_over_loop()


        pygame.display.flip()

    def handle_events(self):

        events = pygame.event.get()
        keys = pygame.key.get_pressed()

        for event in events:
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.pause = True
                    self.pause_game()
                    
                elif self.hero.can_move == True:

                    # directionals
                    if event.key == K_UP:
                        self.hero.upKeyPressed = True
                        self.hero.downKeyPressed = False
                    if event.key == K_DOWN:
                        self.hero.downKeyPressed = True
                        self.hero.upKeyPressed = False
                    if event.key == K_LEFT:
                        self.hero.leftKeyPressed = True
                        self.hero.rightKeyPressed = False
                    if event.key == K_RIGHT:
                        self.hero.rightKeyPressed = True
                        self.hero.leftKeyPressed = False

                else:
                    self.hero.buffer = event.key
                    self.hero.buffer_type = event.type
                    
                if self.hero.can_attack == True:
                    # physical attack
                    if event.key == K_SPACE:
                        self.hero.spacePressed = True
                        self.hero.initiate_attack()
                    #special attack
                    elif event.key == K_u:
                        self.hero.specialPressed = True
                    # items
                    elif event.key == K_1 and self.hero.inventory.slots[0][1] != 'empty':
                        self.hero.oneKeyPressed = True

                    elif event.key == K_2 and self.hero.inventory.slots[1][1] != 'empty':
                        self.hero.twoKeyPressed = True

                else:
                    self.hero.buffer = event.key
                    self.hero.buffer_type = event.type

            elif event.type == KEYUP:

                if event.key == K_UP:
                    self.hero.upKeyPressed = False

                elif event.key == K_DOWN:
                    self.hero.downKeyPressed = False

                elif event.key == K_LEFT:
                    self.hero.leftKeyPressed = False

                elif event.key == K_RIGHT:
                    self.hero.rightKeyPressed = False

                if event.key == K_SPACE:
                    self.hero.spacePressed = False

                if event.key == K_u:
                    self.hero.specialPressed = False    

                if event.key == K_1:
                    self.hero.oneKeyPressed = False

                if event.key == K_2:
                    self.hero.twoKeyPressed = False

                if self.hero.can_attack == False or self.hero.can_move == False:
                    self.hero.buffer = event.key
                    self.hero.buffer_type = event.type

            # joystick code added
            joystick_count = pygame.joystick.get_count()
            #print(joystick_count)
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
                buttons = joystick.get_numbuttons()

                if event.type == pygame.JOYBUTTONDOWN:
                    print("Joystick button pressed.")
                    if self.hero.can_move == True:
                        if event.button == 0:
                            print ("Up pressed")
                            self.hero.upKeyPressed = True
                            self.hero.downKeyPressed = False
                        if event.button == 1:
                            print("Down pressed")
                            self.hero.downKeyPressed = True
                            self.hero.upKeyPressed = False
                        if event.button == 2:
                            print ("Left pressed")
                            self.hero.leftKeyPressed = True
                            self.hero.rightKeyPressed = False
                        if event.button == 3:
                            print ("Right pressed")
                            self.hero.rightKeyPressed = True
                            self.hero.leftKeyPressed = False
                        if event.button == 4:
                            print ("Pause pressed")
                            self.pause = True
                            self.pause_game()
                    else:
                        keyPressed = None
                        if event.button == 0:
                            keyPressed = K_UP
                        if event.button == 1:
                            keyPressed = K_DOWN
                        if event.button == 2:
                            keyPressed = K_LEFT
                        if event.button == 3:
                            keyPressed = K_RIGHT
                        if keyPressed is not None:
                            self.hero.buffer = keyPressed
                            self.hero.buffer_type = KEYDOWN

                    if self.hero.can_attack == True:
                        # physical attack
                        print(event.button)
                        if event.button == 11:
                            print ("A button pressed")
                            self.hero.spacePressed = True
                            self.hero.initiate_attack()
                        # special attack
                        elif event.button == 12:
                            print ("B button pressed")
                            self.hero.specialPressed = True
                        # items
                        elif event.button == 13 and self.hero.inventory.slots[0][1] != 'empty':
                            self.hero.oneKeyPressed = True

                        elif event.button == 14 and self.hero.inventory.slots[1][1] != 'empty':
                            self.hero.twoKeyPressed = True
                    else:
                        keyPressed = None
                        if event.button == 11:
                            keyPressed = K_SPACE
                        if event.button == 12:
                            keyPressed = K_u
                        if event.button == 13:
                            keyPressed = K_1
                        if event.button == 14:
                            keyPressed = K_2
                        if keyPressed is not None:
                            self.hero.buffer = keyPressed
                            self.hero.buffer_type = KEYDOWN

                if event.type == pygame.JOYBUTTONUP:
                    if event.button == 0:
                        print("Joystick button released.")
                        self.hero.upKeyPressed = False
                    if event.button == 1:
                        print("Joystick button released.")
                        self.hero.downKeyPressed = False
                    if event.button == 2:
                        print("Joystick button released.")
                        self.hero.leftKeyPressed = False
                    if event.button == 3:
                        print("Joystick button released.")
                        self.hero.rightKeyPressed = False
                    if event.button == 11:
                        self.hero.spacePressed = False
                    if event.button == 12:
                        self.hero.specialPressed = False
                    if event.button == 13:
                        self.hero.oneKeyPressed = False
                    if event.button == 14:
                        self.hero.twoKeyPressed = False
                    if self.hero.can_attack == False or self.hero.can_move == False:
                        keyPressed = None
                        if event.button == 0:
                            keyPressed = K_UP
                        if event.button == 1:
                            keyPressed = K_DOWN
                        if event.button == 2:
                            keyPressed = K_LEFT
                        if event.button == 3:
                            keyPressed = K_RIGHT
                        if event.button == 11:
                            keyPressed = K_SPACE
                        if event.button == 12:
                            keyPressed = K_u
                        if event.button == 13:
                            keyPressed = K_1
                        if event.button == 14:
                            keyPressed = K_2
                        if keyPressed is not None:
                            self.hero.buffer = keyPressed
                            self.hero.buffer_type = KEYUP
            # end of joystick code added

    def pause_game(self):
        self.hero.upKeyPressed = False
        self.hero.downKeyPressed = False
        self.hero.leftKeyPressed = False
        self.hero.rightKeyPressed = False

        quit_button = Button(SingleplayerButton, self.screen.get_width()/2.8, self.screen.get_height()/2.5)
        resume_button = Button(PlayButton, self.screen.get_width()/2.8, self.screen.get_height()/2.5 + 70)

        button_group = pygame.sprite.Group()
        button_group.add(quit_button, resume_button)

        pause_font1 = pygame.font.SysFont(None, 60)
        pause_font2 = pygame.font.SysFont(None, 25)
        pause_text = pause_font1.render('- PAUSED -', 0, (255,255,255))
        #pause_text_sub = pause_font2.render('PRESS START BUTTON', 0, (255,255,255))

        while self.pause:    
            
            self.screen.blit(pause_text, (self.screen.get_width()/2.8 + 70, self.screen.get_height()/2.5 - 70))
            #self.screen.blit(pause_text_sub, (self.screen.get_width()/2.8 + 75, self.screen.get_height()/2.5 - 10))

            for event in pygame.event.get():
                joystick_count = pygame.joystick.get_count()
                # print(joystick_count)
                for i in range(joystick_count):
                    joystick = pygame.joystick.Joystick(i)
                    joystick.init()
                    buttons = joystick.get_numbuttons()
                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == 4:
                            self.pause = False

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.pause = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        cursor = CursorLocation(event.pos)
                        click = pygame.sprite.GroupSingle(cursor)
                        button_click_list = pygame.sprite.groupcollide(button_group, click, False, False)
                        cursor.kill()

                        for button in button_click_list:
                            if button == quit_button:
                                pygame.quit()
                                quit()
                            elif button == resume_button:
                                self.pause = False

            button_group.draw(self.screen)
            pygame.display.update()
            self.clock.tick(15)


if __name__ == "__main__":
    game = GameMain()
    game.main_loop()
