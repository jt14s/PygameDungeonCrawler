''' Notable Problems:
    -If character does not move, then no damage will be dealt
    -Add a cooldown to the projectiles
'''

import pygame,random,math
from pygame.locals import *
from characters import *
from rooms import *

class GameMain():
    done = False
   
    def __init__(self,width = 1224, height = 952):
        pygame.init()

        #background color
        self.color_x = 0
        self.color_y = 0
        self.color_z = 0

        #set screen variables
        self.width, self.height = width, height
        pygame.display.set_caption("Maiden Hearts")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        #create hero and necessary sprite groups
        self.hero = Hero(68,136,"UP", self.screen)        
        self.all_sprite_list = pygame.sprite.Group()
        self.all_room_tiles = pygame.sprite.Group()

        #room variables
        self.rooms = [Room1(),Room2()]
        self.current_x = 0
        self.current_room = self.rooms[self.current_x]

        #access room entities
        self.hero.items = self.current_room.item_list
        self.hero.walls = self.current_room.wall_list
        self.hero.roofs = self.current_room.roof_list
        self.hero.mobs = self.current_room.mob_list

        #load sprite groups accordingly
        self.all_room_tiles.add(self.current_room.floor_list,self.current_room.wall_list,self.current_room.item_list)
        self.all_sprite_list.add(self.hero.mobs, self.hero)

        self.ui = pygame.sprite.GroupSingle(self.hero.ui)
        self.inv = pygame.sprite.GroupSingle(self.hero.inventory)

        self.projectiles = pygame.sprite.Group()
        
    def main_loop(self):
        while not self.done:       
            self.handle_events()
            self.draw()
            self.all_sprite_list.update()
            self.clock.tick(60)
        
        pygame.quit()
        
    def draw(self):
        if self.hero.hp <= 0:
            self.all_sprite_list.remove(self.hero)
        
        self.screen.fill((self.color_x, self.color_y, self.color_z))

        self.all_room_tiles.draw(self.screen)
        self.current_room.item_list.draw(self.screen)
        self.all_sprite_list.draw(self.screen)

        for mob in self.current_room.mob_list:
            mob.follow_hero(self.hero)

        ##
        self.projectiles.draw(self.screen)
        self.projectiles.update()
        
        self.current_room.roof_list.draw(self.screen)

        self.current_room.wall_list.update()
        
        self.hero.ui.hp_bar.bar_group.draw(self.screen)
        self.hero.ui.sp_bar.bar_group.draw(self.screen)
        self.ui.draw(self.screen)

        self.inv.draw(self.screen)
        self.hero.item_slot_group.draw(self.screen)

        pygame.display.flip()
            
    def handle_events(self):
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == KEYDOWN and self.hero.can_move == True:
                if event.key == K_ESCAPE:
                    self.done = True
                elif event.key == K_r:
                    obj = GameMain()
                    obj.main_loop()

                #directionals
                elif event.key == K_UP:
                    self.hero.upKeyPressed = True
                    self.hero.downKeyPressed = False
                    self.hero.DIRECTION = self.hero.UP
                elif event.key == K_DOWN:
                    self.hero.downKeyPressed = True
                    self.hero.upKeyPressed = False
                    self.hero.DIRECTION = self.hero.DOWN
                    self.hero.change_y = 5
                elif event.key == K_LEFT:
                    self.hero.leftKeyPressed = True
                    self.hero.rightKeyPressed = False
                    self.hero.DIRECTION = self.hero.LEFT
                elif event.key == K_RIGHT:
                    self.hero.rightKeyPressed = True
                    self.hero.leftKeyPressed = False
                    self.hero.DIRECTION = self.hero.RIGHT

                #fix the attack animation
                elif event.key == K_SPACE:
                    print 'space pressed'
                    self.hero.spacePressed = True
                    self.hero.can_move = False

                    old_rect = self.hero.rect
                    old_rect_x = self.hero.rect.x
                    old_rect_y = self.hero.rect.y
                    print self.hero.DIRECTION

                    if self.hero.DIRECTION == self.hero.RIGHT:
                        print 'here'
                        self.hero.image = self.hero.attack_right_animation[2]
                        self.hero.rect = self.hero.image.get_rect()
                        self.hero.rect.x = old_rect_x
                        self.hero.rect.y = old_rect_y

                        frame = 0

                        for x in range(1,128):
                            if x % 42 == 0:
                                print x
                                self.hero.image = self.hero.attack_right_animation[frame]
                                frame += 1

                        mob_hit_list = pygame.sprite.spritecollide(self.hero, self.hero.mobs, False)

                        for mob in mob_hit_list:
                            print 'hit mob'

                        self.hero.image = self.hero.walk_right_animation[0]
                        self.hero.rect = old_rect
                        self.hero.rect.x = old_rect_x
                        self.hero.rect.y = old_rect_y
                    
                    self.hero.can_move = True

                #items
                if event.key == K_1 and self.hero.inventory.slots[0][1] != 'empty':
                    self.hero.oneKeyPressed = True
                    
                    if self.hero.inventory.slots[0][0].item_name == 'rope':
                        thrown_rope = ThrownRope(self.hero.rect.x + 30, self.hero.rect.y + 30, self.hero.DIRECTION, self.hero.walls, self.hero.roofs, self.hero.mobs)
                        self.projectiles.add(thrown_rope)

                    elif self.hero.inventory.slots[0][0].item_name == 'bow':
                        shot_arrow = Arrow(self.hero.rect.x + 30, self.hero.rect.y + 30, self.hero.DIRECTION, self.hero.walls, self.hero.roofs, self.hero.mobs)
                        self.projectiles.add(shot_arrow)

                elif event.key == K_2 and self.hero.inventory.slots[1][1] != 'empty':
                    self.hero.twoKeyPressed = True
                    if self.hero.inventory.slots[1][0].item_name == 'rope':
                        thrown_rope = ThrownRope(self.hero.rect.x + 30, self.hero.rect.y + 30, self.hero.DIRECTION, self.hero.walls, self.hero.roofs, self.hero.mobs)
                        self.projectiles.add(thrown_rope)
                        
            elif event.type == KEYUP:
                if event.key == K_UP:
                    self.hero.upKeyPressed = False
                    
                    if self.hero.rightKeyPressed:
                        self.hero.DIRECTION = self.hero.RIGHT
                        
                    elif self.hero.leftKeyPressed:
                        self.hero.DIRECTION = self.hero.LEFT
                        
                elif event.key == K_DOWN:
                    self.hero.downKeyPressed = False
                    if self.hero.rightKeyPressed:
                        self.hero.DIRECTION = self.hero.RIGHT
                        
                    elif self.hero.leftKeyPressed:
                        self.hero.DIRECTION = self.hero.LEFT
                        
                elif event.key == K_LEFT:
                    self.hero.image = self.hero.walk_left_animation[0]
                    self.hero.leftKeyPressed = False
                    
                    if self.hero.upKeyPressed:
                        self.hero.DIRECTION = self.hero.UP
                        
                    elif self.hero.downKeyPressed:
                        self.hero.image = self.hero.walk_down_animation[0]
                        self.hero.DIRECTION = self.hero.DOWN
                        
                elif event.key == K_RIGHT:                   
                    self.hero.image = self.hero.walk_right_animation[0]                  
                    self.hero.rightKeyPressed = False
                    
                    if self.hero.upKeyPressed:
                        self.hero.DIRECTION = self.hero.UP
                        
                    elif self.hero.downKeyPressed:
                        self.hero.DIRECTION = self.hero.DOWN

                elif event.key == K_SPACE:
                    self.hero.spacePressed = False

                if event.key == K_1:
                    self.hero.oneKeyPressed = False

                if event.key == K_2:
                    self.hero.twoKeyPressed = False
               
if __name__ == "__main__":
    game = GameMain()
    game.main_loop()
