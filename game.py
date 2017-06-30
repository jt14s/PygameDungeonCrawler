import random,math
from image_loader import *
from pygame.locals import *

class Hero(pygame.sprite.Sprite):

    #all characters will share these attrivutes
    walls = None
    floors = None
    roofs = None
    mobs = None
    items = None
    keys = None
        
    def __init__(self, x, y,DIRECTION,upKeyPressed,downKeyPressed,leftKeyPressed,rightKeyPressed, spacePressed, screen):
        #init self as a srpite object
        pygame.sprite.Sprite.__init__(self)

        #images and animation lists
        self.image = PinkD1
        self.up_1 = PinkU1
        self.walk_right_animation = [PinkR1,PinkR2, PinkR1, PinkR3]
        self.walk_left_animation = [PinkL1, PinkL2, PinkL1, PinkL3]
        self.walk_down_animation = [PinkD1, PinkD2, PinkD1, PinkD3]

        #character hitbox
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #frame info
        self.ticker = 0
        self.current_frame = 0
        
        #inv and ui
        self.ui = UI((screen.get_width()/6)+10, 10, 100, 100, screen)
        self.inventory = Inventory(InvImg, (screen.get_width()/2)-70, (screen.get_height()/1.1))

        self.item_slot_group = pygame.sprite.Group()

        #key variables
        self.DIRECTION = DIRECTION
        self.upKeyPressed = upKeyPressed
        self.downKeyPressed = downKeyPressed
        self.leftKeyPressed = leftKeyPressed
        self.rightKeyPressed = rightKeyPressed
        self.spacePressed = spacePressed

        #misc
        self.RIGHT, self.LEFT, self.UP, self.DOWN = "right left up down".split()
        self.action = 'walking'
        self.can_move = True
        self.walk_rate = 7
        self.invuln_frames = 0

        #hp vars
        self.hp = 100
        self.MAX_HP = 100
        self.MIN_HP = 0

        #sp vars
        self.sp = 100
        self.MAX_SP = 100
        self.MIN_SP = 0
    
    def update(self):
        #instance of the player in a group to check against collisions
        player = pygame.sprite.GroupSingle(self)
        
        if self.downKeyPressed:
            self.rect.y += self.walk_rate
            self.image = self.walk_down_animation[self.current_frame]

            #this is how you calculate collisions between two sprite groups, then all collided are stored in list
            item_hit_list = pygame.sprite.groupcollide(self.items, player, True, False)
            roof_hit_list = pygame.sprite.groupcollide(player, self.roofs, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
            mob_hit_list = pygame.sprite.groupcollide(self.mobs, player, False, False)

            #check trhough all calculated collisions
            for roof in roof_hit_list:
                self.rect.bottom = roof.rect.top + 63

            for item in item_hit_list:
                print('picked up item')

                for slot in self.inventory.slots:
                    if slot[1] == 'empty':
                        #update slot info and then add to be drawn to screen
                        slot[0].update_image(item.image, self.inventory.rect.x + 21 + ( slot[0].index * 60), self.inventory.rect.y + 23)
                        slot[1] = 'used'
                        self.item_slot_group.add(slot[0])
                        break
                    
            for mob in mob_hit_list:
                if self.invuln_frames == 0:
                    print('hit mob')
                    self.ui.hp_bar.updateHealth(mob.damage, self.hp, self.MAX_HP)
                    self.ui.sp_bar.updateSpecial(mob.damage, self.sp, self.MAX_SP)

                    self.sp -= mob.damage
                    self.hp -= mob.damage
                    if self.hp <= self.MIN_HP:
                        print 'ded'

                    self.invuln_frames = 20
                    
        elif self.upKeyPressed:
            self.rect.y -= self.walk_rate
            self.image = self.up_1

            item_hit_list = pygame.sprite.groupcollide(self.items, player, True, False)
            wall_hit_list = pygame.sprite.groupcollide(player, self.walls, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
            mob_hit_list = pygame.sprite.groupcollide(self.mobs, player, False, False)

            for wall in wall_hit_list:
                self.rect.top = wall.rect.bottom - 63

            for item in item_hit_list:
                print('picked up item')

                for slot in self.inventory.slots:
                    if slot[1] == 'empty':
                        slot[0].update_image(item.image, self.inventory.rect.x + 21 + ( slot[0].index * 60), self.inventory.rect.y + 23)
                        slot[1] = 'used'
                        self.item_slot_group.add(slot[0])
                        break

            for mob in mob_hit_list:
                if self.invuln_frames == 0:
                    print('hit mob')
                    self.ui.hp_bar.updateHealth(mob.damage, self.hp, self.MAX_HP)
                    self.ui.sp_bar.updateSpecial(mob.damage, self.sp, self.MAX_SP)

                    self.sp -= mob.damage
                    self.hp -= mob.damage
                    if self.hp <= self.MIN_HP:
                        print 'ded'

                    self.invuln_frames = 20
            
        elif self.leftKeyPressed:
            self.rect.x -= self.walk_rate
            self.image = self.walk_left_animation[self.current_frame]

            item_hit_list = pygame.sprite.groupcollide(self.items, player, True, False)
            roof_hit_list = pygame.sprite.groupcollide(player, self.roofs, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
            wall_hit_list = pygame.sprite.groupcollide(player, self.walls, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
            mob_hit_list = pygame.sprite.groupcollide(self.mobs, player, False, False)

            for wall in wall_hit_list:
                self.rect.left = wall.rect.right - 63

            for roof in roof_hit_list:
                self.rect.left = roof.rect.right - 63

            for item in item_hit_list:
                print('picked up item')

                for slot in self.inventory.slots:
                    if slot[1] == 'empty':
                        slot[0].update_image(item.image, self.inventory.rect.x + 21 + ( slot[0].index * 60), self.inventory.rect.y + 23)
                        slot[1] = 'used'
                        self.item_slot_group.add(slot[0])
                        break
                    
            for mob in mob_hit_list:
                if self.invuln_frames == 0:
                    print('hit mob')
                    self.ui.hp_bar.updateHealth(mob.damage, self.hp, self.MAX_HP)
                    self.ui.sp_bar.updateSpecial(mob.damage, self.sp, self.MAX_SP)

                    self.sp -= mob.damage
                    self.hp -= mob.damage
                    if self.hp <= self.MIN_HP:
                        print 'ded'

                    self.invuln_frames = 20
                
        elif self.rightKeyPressed:
            self.rect.x += self.walk_rate
            self.image = self.walk_right_animation[self.current_frame]

            item_hit_list = pygame.sprite.groupcollide(self.items, player, True, False)
            roof_hit_list = pygame.sprite.groupcollide(player, self.roofs, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
            wall_hit_list = pygame.sprite.groupcollide(player, self.walls, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
            mob_hit_list = pygame.sprite.groupcollide(self.mobs, player, False, False)

            for wall in wall_hit_list:
                self.rect.right = wall.rect.left + 63

            for roof in roof_hit_list:
                self.rect.right = roof.rect.left + 63

            for item in item_hit_list:
                print('picked up item')

                for slot in self.inventory.slots:
                    if slot[1] == 'empty':
                        slot[0].update_image(item.image, self.inventory.rect.x + 21 + ( slot[0].index * 60), self.inventory.rect.y + 23)
                        slot[1] = 'used'
                        self.item_slot_group.add(slot[0])
                        break

            for mob in mob_hit_list:
                if self.invuln_frames == 0:
                    print('hit mob')
                    self.ui.hp_bar.updateHealth(mob.damage, self.hp, self.MAX_HP)
                    self.ui.sp_bar.updateSpecial(mob.damage, self.sp, self.MAX_SP)

                    self.sp -= mob.damage
                    self.hp -= mob.damage
                    if self.hp <= self.MIN_HP:
                        print 'ded'

                    self.invuln_frames = 20



        if self.invuln_frames != 0:
            self.invuln_frames -= 1
            print 'invulnerable'

        #advance the current frame based on FPS
        self.ticker += 1
        if self.ticker % 8 == 0:
            self.current_frame = (self.current_frame + 1) % 4
            self.ticker = 0


class UI(pygame.sprite.Sprite):
    def __init__(self, x, y, hp, sp, screen):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = UiImg
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.MAX_HP = 100
        self.MAX_SP = 100
        self.curr_hp = hp
        self.curr_sp = sp

        #we need to pass in an x and y coordinate, so pass in the x and y of the UI
        self.hp_bar = HPBar(HealthBar, x, y, screen)
        self.sp_bar = SPBar(SpecialBar, x, y, screen)
       
class HPBar(pygame.sprite.Sprite):
    def __init__(self, image, x, y, screen):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x + 20
        self.rect.y = y + 15

        self.orig_image = self.image
        self.orig_x = self.rect.x
        self.orig_width = self.rect.width

        self.bar_group = pygame.sprite.Group()
        self.bar_group.add(self)
        self.bar_group.draw(screen)

    def updateHealth(self, damage, hp, maxhp):
        damage_percent = (hp - damage) / float(maxhp)
        chop_area = (0,0, self.orig_width * (1 - damage_percent),0)
        self.rect.x = self.orig_x + (self.orig_width * (1 - damage_percent))
        self.image = pygame.transform.chop(self.orig_image, chop_area)


class SPBar(pygame.sprite.Sprite):
    def __init__(self, image, x, y, screen):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x + 424
        self.rect.y = y + 15

        self.orig_image = self.image
        self.orig_x = self.rect.x
        self.orig_width = self.rect.width

        self.bar_group = pygame.sprite.Group()
        self.bar_group.add(self)
        self.bar_group.draw(screen)

    def updateSpecial(self, damage, sp, maxsp):
        damage_percent = (sp - damage) / float(maxsp)
        chop_area = (0,0, self.orig_width * (1 - damage_percent),0)
        self.image = pygame.transform.chop(self.orig_image, chop_area)

class Inventory(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
       pygame.sprite.Sprite.__init__(self)

       self.image = image
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y

       self.slots = [[ItemSlot(0), 'empty'], [ItemSlot(1), 'empty']]

class ItemSlot(pygame.sprite.Sprite):
    def __init__(self, index):
        pygame.sprite.Sprite.__init__(self)
        self.index = index

    def update_image(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        
class Item(pygame.sprite.Sprite):
    def __init__(self, name, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.name = name
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tier = 1

class Rope(Item):
    def __init__(self, name, image, x, y):
        Item.__init__(self, name, image, x, y)
        

class Mob(pygame.sprite.Sprite):
    def __init__(self, image, x, y, hp):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = hp
        self.damage = 20

class ShrimpMob(Mob):
    def __init__(self, x, y):
        self.walk1 = pygame.image.load('images/mobs/shrimp/left/walk1.png')
        Mob.__init__(self, self.walk1, x, y, 100)

        self.walk2 = pygame.image.load('images/mobs/shrimp/left/walk2.png')

        self.aggro1 = pygame.image.load('images/mobs/shrimp/left/aggro1.png')
        self.aggro2 = pygame.image.load('images/mobs/shrimp/left/aggro2.png')

        self.neutral_animation = [self.walk1, self.walk2]
        self.aggro_animation = [self.aggro1, self.aggro2]

        self.current_frame = 0
        self.ticker = 0

    def update(self):
        self.image = self.neutral_animation[self.current_frame]

        self.ticker += 1
        if self.ticker % 15 == 0:
            self.current_frame = (self.current_frame + 1) % 2
            self.ticker = 0


class MapTile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Wall(MapTile):
    def __init__(self, x, y, image):
        MapTile.__init__(self, x, y, image)

class Floor(MapTile):
    def __init__(self, x, y, image):
        MapTile.__init__(self, x, y, image)

class Roof(MapTile):
    def __init__(self, x, y, image):
        MapTile.__init__(self, x, y, image)

class TorchBrick(MapTile):
    def __init__(self,x,y,image):
        MapTile.__init__(self, x, y, image)        

        self.torch_animation = [TorchImg1,TorchImg2,TorchImg3,TorchImg4,TorchImg5,TorchImg6,TorchImg7,TorchImg8]
        self.current_frame = 0
        self.ticker = 0

    def update(self):
        self.image = self.torch_animation[self.current_frame]

        self.ticker += 1
        if self.ticker % 64 == 0:
            self.current_frame = 0
        elif self.ticker % 8 == 0:
            self.current_frame += 1


class Room(object):
    wall_list = None
    floor_list = None
    item_list = None
    mob_list = None

    def __init__(self):
        self.wall_list = pygame.sprite.Group()
        self.floor_list = pygame.sprite.Group()
        self.roof_list = pygame.sprite.Group()
        self.mob_list = pygame.sprite.Group()
        self.item_list = pygame.sprite.Group()
        self.key_list = pygame.sprite.Group()
        self.lock_list = pygame.sprite.Group()
        
class Room1(Room):
    def __init__(self):
        Room.__init__(self)

        room_layout = ['RRRRRRRRRRRRRRRRRRx',
                       'RTWRTWWTWWRWWTWWTRx',
                       'RFFRFFFFFFRFFFFFFWx',
                       'RFFRFFFFFFRFFFFFFFx',
                       'RFFRFFFFFFRFFFFFFFx',
                       'RFFRFFFFFFRFFFRRRRx',
                       'RFFRFFFFFFRFFFRRRRx',
                       'RFFRRRRFRRRFFFWWWRx',
                       'RFFRRRRFRRRFFFFFFRx',
                       'RFFTWWTFTWWFFFFFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RFFRRRRFFFFFFFFFFRx',
                       'RFFRRRRFFFFFFFFFFRx',
                       'RRRRRRRRRRRRRRRRRRx',]
        
        items = [Rope('rope', RopeImg, 544, 340), Rope('rope', RopeImg, 136 + 68 * 3, 340)]
        mobs = [ShrimpMob(816, 136)]
        roofs = []
        walls = []
        floors = []
        x, y = 0, 0
        i = 1
        
        for section in room_layout:
            for surface in section:
                if surface == 'R':
                    roofs.append(Wall(x,y,RoofImgCenterCenter))
                if surface == 'W':
                    walls.append(Wall(x,y,WallImg))
                if surface == 'T':
                    walls.append(TorchBrick(x,y,TorchImg1))
                if surface == 'F':
                    floors.append(Floor(x,y,FloorImgCenter))
                if surface == 'x':
                    x = 0
                else: x += 68
            y += 68
            
        
        for wall in walls:
            self.wall_list.add(wall)
            
        for roof in roofs:
            self.roof_list.add(roof)

        for floor in floors:
            self.floor_list.add(floor)
            
        for item in items:
            self.item_list.add(item)

        for mob in mobs:
            self.mob_list.add(mob)

            
class GameMain():
    done = False
   
    def __init__(self,width = 1224, height = 952):
        pygame.init()

        #background color
        self.color_x = 252
        self.color_y = 216
        self.color_z = 168

        #set screen variables
        self.width, self.height = width, height
        pygame.display.set_caption("Maiden Hearts")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        #create hero and necessary sprite groups
        self.hero = Hero(68,136,"UP",False,False,False,False,False, self.screen)        
        self.all_sprite_list = pygame.sprite.Group()
        self.all_room_tiles = pygame.sprite.Group()

        #room variables
        self.rooms = [Room1()]
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

                elif event.key == K_r:
                    obj = GameMain()
                    obj.main_loop()
                        
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
               
if __name__ == "__main__":
    game = GameMain()
    game.main_loop()
