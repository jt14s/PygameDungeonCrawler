''' Notable Problems:
    -Add a cooldown to the projectiles
'''

import pygame, random, math
from pygame.locals import *
from characters import *
from rooms import *


class GameMain():
    done = False

    def __init__(self, character = 'PL', width=1224, height=952):
        pygame.init()

        # set screen variables
        self.width, self.height = width, height
        pygame.display.set_caption("Maiden Hearts")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # create hero and necessary sprite groups
        if character == 'PL':
            self.hero = Paladin(68, 136, "DOWN", self.screen)
        elif character == 'WZ':
            self.hero = Wizard(68, 136, "DOWN", self.screen)
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
            self.clock.tick(256)

        pygame.quit()

    def draw(self):
        if self.hero.hp <= 0:
            self.all_sprite_list.remove(self.hero)

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

        pygame.display.flip()

    def handle_events(self):
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    self.done = True
                elif event.key == K_r:
                    obj = GameMain()
                    obj.main_loop()
                    
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

                    # fix the attack animation

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

if __name__ == "__main__":
    game = GameMain()
    game.main_loop()
