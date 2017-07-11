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
        self.hero = Hero(68,136,"DOWN", self.screen)
        self.all_sprite_list = pygame.sprite.Group()
        self.all_room_tiles = pygame.sprite.Group()

        #room variables
        self.rooms = [Room2(),Room1()]
        self.current_x = 0
        self.current_room = self.rooms[self.current_x]

        #access room entities
        self.hero.items = self.current_room.item_list
        self.hero.walls = self.current_room.wall_list
        self.hero.roofs = self.current_room.roof_list
        self.hero.mobs = self.current_room.mob_list

	self.hero.portals = self.current_room.portal_list
	self.hero.current_room = self.rooms[self.current_x]

        #load sprite groups accordingly
        self.all_room_tiles.add(self.current_room.floor_list,self.current_room.wall_list,self.current_room.item_list)
        self.all_sprite_list.add(self.hero.mobs, self.hero)

        self.ui = pygame.sprite.GroupSingle(self.hero.ui)
        self.inv = pygame.sprite.GroupSingle(self.hero.inventory)

        self.projectiles = pygame.sprite.Group()

        
    def main_loop(self):
        while not self.done:
	    if self.current_room != self.hero.current_room:

		    #CHANGE THIS WHEN PORTALS ARE ON WALL
	            self.hero.rect.x = 68
		    self.hero.rect.y = 136

		    #WHY WON'T SHE SPAWN LOOKING DOWN?????
		    self.hero.DIRECTION = "DOWN"
		    self.current_room = self.hero.current_room

		    self.hero.image = self.hero.walk_down_animation[0]
		    
		    #access room entities
		    self.hero.items = self.current_room.item_list
		    self.hero.walls = self.current_room.wall_list
		    self.hero.roofs = self.current_room.roof_list
		    self.hero.mobs = self.current_room.mob_list

		    self.hero.portals = self.current_room.portal_list

		    #load sprite groups accordingly
		    self.all_room_tiles.empty()
		    self.all_sprite_list.empty()		

		    self.all_room_tiles.add(self.current_room.floor_list,self.current_room.wall_list,self.current_room.item_list)
		    self.all_sprite_list.add(self.hero.mobs, self.hero)

            self.handle_events()
            self.all_sprite_list.update()
            self.draw()
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
            if mob.look_for_hero(self.hero) == True:
                mob.follow_hero(self.hero)
        
        
        self.projectiles.draw(self.screen)
        self.projectiles.update()
        
	self.current_room.portal_list.draw(self.screen)

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
            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    self.done = True
                elif event.key == K_r:
                    obj = GameMain()
                    obj.main_loop()
		elif self.hero.can_move == True:
		        #directionals
		        if event.key == K_UP:
		            self.hero.upKeyPressed = True
		            self.hero.downKeyPressed = False
		            self.hero.DIRECTION = self.hero.UP
		        if event.key == K_DOWN:
		            self.hero.downKeyPressed = True
		            self.hero.upKeyPressed = False
		            self.hero.DIRECTION = self.hero.DOWN
		        if event.key == K_LEFT:
		            self.hero.leftKeyPressed = True
		            self.hero.rightKeyPressed = False
		            self.hero.DIRECTION = self.hero.LEFT
		        if event.key == K_RIGHT:
		            self.hero.rightKeyPressed = True
		            self.hero.leftKeyPressed = False
		            self.hero.DIRECTION = self.hero.RIGHT

                #fix the attack animation
                if self.hero.can_attack == True:
			#physical attack
			if event.key == K_SPACE:
	                    self.hero.spacePressed = True
			    self.hero.initiate_attack()

		        #items
		        elif event.key == K_1 and self.hero.inventory.slots[0][1] != 'empty':
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
			    
		            elif self.hero.inventory.slots[1][0].item_name == 'bow':
		                shot_arrow = Arrow(self.hero.rect.x + 30, self.hero.rect.y + 30, self.hero.DIRECTION, self.hero.walls, self.hero.roofs, self.hero.mobs)
		                self.projectiles.add(shot_arrow)
		                
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

	                if event.key == K_1:
	                    self.hero.oneKeyPressed = False

	                if event.key == K_2:
	                    self.hero.twoKeyPressed = False

    def next_room(self):
	self.current_x += 1
	self.current_room = self.rooms[current_x]

if __name__ == "__main__":
    game = GameMain()
    game.main_loop()
