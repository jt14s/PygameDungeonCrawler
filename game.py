import pygame,random,math
from pygame.locals import *

#wall images
WallImg = pygame.image.load('images/level1/wallbrickpattern.png')

#floor images
FloorImgCenter = pygame.image.load('images/level1/floors/floortile/floortile1.png')
FloorImgTop = pygame.image.load('images/level1/floors/floortile/floortile2.png')
FloorImgRight = pygame.image.load('images/level1/floors/floortile/floortile3.png')
FloorImgLeft = pygame.image.load('images/level1/floors/floortile/floortile5.png')
FloorImgTopRight = pygame.image.load('images/level1/floors/floortile/floortile6.png')
FloorImgTopLeft = pygame.image.load('images/level1/floors/floortile/floortile9.png')
FloorImgVerticalTunnel = pygame.image.load('images/level1/floors/floortile/floortile11.png')
FloorImgTopDeadEnd = pygame.image.load('images/level1/floors/floortile/floortile12.png')

#roof images
RoofImgCenter = pygame.image.load('images/level1/rooftile/roof1.png')
RoofImgCenterCenter = pygame.image.load('images/level1/rooftile/roof12.png')

#torch images
TorchImg1 = pygame.image.load('images/level1/wall_torch/walltorch1.png')
TorchImg2 = pygame.image.load('images/level1/wall_torch/walltorch2.png')
TorchImg3 = pygame.image.load('images/level1/wall_torch/walltorch3.png')
TorchImg4 = pygame.image.load('images/level1/wall_torch/walltorch2.png')
TorchImg5 = pygame.image.load('images/level1/wall_torch/walltorch1.png')
TorchImg6 = pygame.image.load('images/level1/wall_torch/walltorch4.png')
TorchImg7 = pygame.image.load('images/level1/wall_torch/walltorch5.png')
TorchImg8 = pygame.image.load('images/level1/wall_torch/walltorch4.png')

RopeImg = pygame.image.load('images/items/rope.png')
InvImg = pygame.image.load('images/inventory.png')
UiImg = pygame.image.load('images/hud.png')

class Hero(pygame.sprite.Sprite):

    #other entities associated with sprite
    walls = None
    floors = None
    roofs = None
    mobs = None
    items = None
    keys = None
    locks = None
        
    def __init__(self, x, y,DIRECTION,upKeyPressed,downKeyPressed,leftKeyPressed,rightKeyPressed, spacePressed, screen_h, screen_w):
        #init self as a srpite object
        pygame.sprite.Sprite.__init__(self)

        #images and animation lists
        self.image = pygame.image.load('images/pink/right/right1.png')
        self.right_1 = pygame.image.load('images/pink/right/right1.png')
        self.right_2 = pygame.image.load('images/pink/right/right2.png')
        self.right_3 = pygame.image.load('images/pink/right/right3.png')

        self.left_1 = pygame.image.load('images/pink/left/left1.png')
        self.left_2 = pygame.image.load('images/pink/left/left2.png')
        self.left_3 = pygame.image.load('images/pink/left/left3.png')

        self.up_1 = pygame.image.load('images/pink/up/up1.png')
        
        self.down_1 = pygame.image.load('images/pink/down/down1.png')
        self.down_2 = pygame.image.load('images/pink/down/down2.png')
        self.down_3 = pygame.image.load('images/pink/down/down3.png')

        self.walk_right_animation = [self.right_1,self.right_2,self.right_1,self.right_3]
        self.walk_left_animation = [self.left_1,self.left_2,self.left_1,self.left_3]
        self.walk_down_animation = [self.down_1,self.down_2,self.down_1,self.down_3]

        #frame info
        self.ticker = 0
        self.current_frame = 0

        #character hitbox
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.inv_x = (screen_w / 2) + 75
        self.inv_y = screen_h / 1.5 + 55
        self.inventory = Inventory(InvImg, self.inv_x, self.inv_y)

        self.ui = None

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

    def walk(self):
        pass
    
    def update(self):
        #instance of the player in a group to check against collisions
        player = pygame.sprite.GroupSingle(self)
        
        if self.downKeyPressed:
            self.rect.y += 5
            self.image = self.walk_down_animation[self.current_frame]

            item_hit_list = pygame.sprite.groupcollide(self.items, player, True, False)
            roof_hit_list = pygame.sprite.groupcollide(player, self.roofs, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))

            for roof in roof_hit_list:
                self.rect.bottom = roof.rect.top + 63

            for item in item_hit_list:
                print('picked up item')

                for slot in self.inventory.slots:
                    if slot[1] == 'empty':
                        slot[0].update_image(item.image, self.inventory.rect.x + 20 + ( slot[0].index * 60), self.inv_y + 20)
                        slot[1] = 'used'
                        break
                    
        elif self.upKeyPressed:
            self.rect.y -= 5
            self.image = self.up_1

            item_hit_list = pygame.sprite.groupcollide(self.items, player, True, False)
            wall_hit_list = pygame.sprite.groupcollide(player, self.walls, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))

            for wall in wall_hit_list:
                self.rect.top = wall.rect.bottom - 63

            for item in item_hit_list:
                print('picked up item')

                for slot in self.inventory.slots:
                    if slot[1] == 'empty':
                        slot[0].update_image(item.image, self.inventory.rect.x + 20 + ( slot[0].index * 60), self.inv_y + 20)
                        slot[1] = 'used'
                        break
            
        elif self.leftKeyPressed:
            self.rect.x -= 5
            self.image = self.walk_left_animation[self.current_frame]

            item_hit_list = pygame.sprite.groupcollide(self.items, player, True, False)
            roof_hit_list = pygame.sprite.groupcollide(player, self.roofs, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
            wall_hit_list = pygame.sprite.groupcollide(player, self.walls, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))

            for wall in wall_hit_list:
                self.rect.left = wall.rect.right - 63

            for roof in roof_hit_list:
                self.rect.left = roof.rect.right - 63

            for item in item_hit_list:
                print('picked up item')

                for slot in self.inventory.slots:
                    if slot[1] == 'empty':
                        slot[0].update_image(item.image, self.inventory.rect.x + 20 + ( slot[0].index * 60), self.inv_y + 20)
                        slot[1] = 'used'
                        break
                
        elif self.rightKeyPressed:
            self.rect.x += 5
            self.image = self.walk_right_animation[self.current_frame]

            item_hit_list = pygame.sprite.groupcollide(self.items, player, True, False)
            roof_hit_list = pygame.sprite.groupcollide(player, self.roofs, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
            wall_hit_list = pygame.sprite.groupcollide(player, self.walls, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))

            for wall in wall_hit_list:
                self.rect.right = wall.rect.left + 63

            for roof in roof_hit_list:
                self.rect.right = roof.rect.left + 63

            for item in item_hit_list:
                print('picked up item')

                for slot in self.inventory.slots:
                    if slot[1] == 'empty':
                        slot[0].update_image(item.image, self.inventory.rect.x + 20 + ( slot[0].index * 60), self.inv_y + 20)
                        slot[1] = 'used'
                        break

        #advance the current frame based on FPS
        self.ticker += 1
        if self.ticker % 8 == 0:
            self.current_frame = (self.current_frame + 1) % 4
            self.ticker = 0

class UI(pygame.sprite.Sprite):
    def __init__(self, x, y, hp, sp):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = UiImg
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.MAX_HP = 100
        self.MAX_SP = 100
        self.curr_hp = hp
        self.curr_sp = sp

        self.hp_bar = HpBar()
        self.sp_bar = SPBar()

class UIBar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        

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


class Inventory(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
       pygame.sprite.Sprite.__init__(self)

       self.image = image
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y

        #change this to a list
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
                       'WTWWTWWTWWTWWTWWTWx',
                       'FFFFFFFFFFFFFFFFFFx',
                       'FFFFFFFFFFFFFFFFFFx',
                       'RRFFRRRRFFRRFFFFFFx',
                       'RRFFRRRRFFRRFFFFFFx',
                       'RRFFTWWTFFRRFFFFFFx',
                       'WWFFFFFFFFWWFFFFFFx',
                       'FFFFFFFFFFFFFFFFFFx',
                       'FFFFFFFFFFFFFFFFFFx',
                       'FFFFFFFFFFFFFFFFFFx',
                       'FFFFFFFFFFFFFFFFFFx',
                       'FFFFFWFFFFFFFFFFFFx',
                       'FFFFFFFFFFFFFFFFFFx',]
        
        items = [Rope('rope', RopeImg, 544, 340), Rope('rope', RopeImg, 136, 340)]
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
            
class GameMain():
    done = False
   
    def __init__(self,width = 1224, height = 952):
        pygame.init()
        
        self.color_x = 252
        self.color_y = 216
        self.color_z = 168
        
        self.width, self.height = width, height
        pygame.display.set_caption("Maiden Hearts")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        
        self.hero = Hero(68,136,"UP",False,False,False,False,False, self.width, self.height)        
        self.all_sprite_list = pygame.sprite.Group()
        self.all_sprite_list.add(self.hero)
        
        self.rooms = [Room1()]
        self.current_x = 0
        self.current_room = self.rooms[self.current_x]
        
        self.hero.items = self.rooms[self.current_x].item_list
        self.hero.walls = self.rooms[self.current_x].wall_list
        self.hero.roofs = self.rooms[self.current_x].roof_list
        self.inv = pygame.sprite.GroupSingle(self.hero.inventory)
        self.inv_slots = pygame.sprite.Group()

        self.hero.ui = UI((width/6) + 15, 10, 100, 100)
        self.ui = pygame.sprite.GroupSingle(self.hero.ui)        

        #self.check = False
        
    def main_loop(self):
        while not self.done:

            #this may not be the best place to put this, maybe move it to a method
            #if not self.check:
            for slot in self.hero.inventory.slots:
                if hasattr(slot[0], 'image'):
                    self.inv_slots.add(slot[0])
            
            self.handle_events()
            self.draw()
            self.all_sprite_list.update()            
            self.clock.tick(60)
        
        pygame.quit()
        
    def draw(self):
        self.screen.fill((self.color_x, self.color_y, self.color_z))

        #move this to a function
        self.current_room.floor_list.draw(self.screen)
        self.current_room.wall_list.draw(self.screen)
        self.current_room.item_list.draw(self.screen)
        self.all_sprite_list.draw(self.screen)
        self.current_room.roof_list.draw(self.screen)
        


        self.inv.draw(self.screen)
        self.ui.draw(self.screen)
        self.inv_slots.draw(self.screen)
        self.current_room.wall_list.update()

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
