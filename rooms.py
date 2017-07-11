import pygame
from items import *
from mobs import *
from image_loader import *

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

class Portal(MapTile):
    def __init__(self, x, y, image, room):
        MapTile.__init__(self, x, y, image)
	self.room = room


class Room(object):
    wall_list = None
    floor_list = None
    roof_list = None
    mob_list = None
    item_list = None
    key_list = None
    lock_list = None
    portal_list = None

    def __init__(self):
        self.wall_list = pygame.sprite.Group()
        self.floor_list = pygame.sprite.Group()
        self.roof_list = pygame.sprite.Group()
        self.mob_list = pygame.sprite.Group()
        self.item_list = pygame.sprite.Group()
        self.key_list = pygame.sprite.Group()
        self.lock_list = pygame.sprite.Group()

	self.portal_list = pygame.sprite.Group()
        
class Room1(Room):

    mobs = [ShrimpMob(816, 136, 0)]

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
        exits = []
        
        items = [Rope('rope', RopeImg, 544, 340), Rope('rope', RopeImg, 136 + 68 * 3, 340), Bow('bow', BowImg, 68 * 2, 340)]
        roofs = []
        walls = []
        floors = []

	portals = []
        x, y = 0, 0
        i = 1        
        
            
        
        
        for wall in walls:
            self.wall_list.add(wall)
            
        for roof in roofs:
            self.roof_list.add(roof)

        for floor in floors:
            self.floor_list.add(floor)
            
        for item in items:
            self.item_list.add(item)

        for mob in self.mobs:
            self.mob_list.add(mob)

class Room2(Room):
    
    mobs = [ShrimpMob(68 * 2, 68 * 8, 0), ShrimpMob(816 + (68 * 2),68 * 8, 1)]

    def __init__(self):
        Room.__init__(self)

        room_layout = ['RRRRRRRRRRRRRRRRRRx',
                       'RWWRWWRWWWWRWWRWWRx',
                       'TFFTFFTFFFFTFFTFFTx',
                       '1FFFFFFFFFFFFFFFFFx',
                       '1FFFFFFFFFFFFFFFFFx',
                       'RFFRFFRFFFFRFFRFFRx',
                       'RFFTFFTFFFFTFFTFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RFFRFFRFFFFRFFRFFRx',
                       'RFFTFFTFFFFTFFTFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RRRRRRRRRRRRRRRRRRx',]

        items = []
        roofs = []
        walls = []
        floors = []
	portals = []
        x, y = 0, 0
        i = 1
        
        for section in room_layout:
            for surface in section:                
		if surface == 'x':
                    x = 0
                else:
		    if surface == 'R':
                        roofs.append(Wall(x,y,RoofImgCenterCenter))
                    elif surface == 'W':
                        walls.append(Wall(x,y,WallImg))
                    elif surface == 'T':
		        walls.append(TorchBrick(x,y,TorchImg1))
                    elif surface == 'F':
                        floors.append(Floor(x,y,FloorImgCenter))
		    elif surface == '1':
                        floors.append(Floor(x,y,FloorImgCenter))
	       	        portals.append(Portal(x, y, ThrownRopeDown, Room1()))
		    elif surface == '2':
                        floors.append(Floor(x,y,FloorImgCenter))
	    	        portals.append(Portal(x, y, ThrownRopeDown, Room2()))    
		
		    x += 68
            y += 68
            
        
        for wall in walls:
            self.wall_list.add(wall)
            
        for roof in roofs:
            self.roof_list.add(roof)

        for floor in floors:
            self.floor_list.add(floor)
            
        for item in items:
            self.item_list.add(item)

        for mob in self.mobs:
            self.mob_list.add(mob)

	for portal in portals:
	    self.portal_list.add(portal)
