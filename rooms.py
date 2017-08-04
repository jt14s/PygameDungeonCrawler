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
    def __init__(self, x, y, image):
        MapTile.__init__(self, x, y, image)

        self.torch_animation = [TorchImg1, TorchImg2, TorchImg3, TorchImg4, TorchImg5, TorchImg6, TorchImg7, TorchImg8]
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
    def __init__(self, x, y, image, room_x):
        MapTile.__init__(self, x, y, image)
        self.room_x = room_x

class Room(object):
    wall_list = None
    floor_list = None
    roof_list = None
    mob_list = None
    item_list = None
    key_list = None
    lock_list = None
    portal_list = None
    chasm_list = None

    def __init__(self):
        self.wall_list = pygame.sprite.Group()
        self.floor_list = pygame.sprite.Group()
        self.roof_list = pygame.sprite.Group()
        self.mob_list = pygame.sprite.Group()
        self.item_list = pygame.sprite.Group()
        self.key_list = pygame.sprite.Group()
        self.lock_list = pygame.sprite.Group()        
        self.chasm_list = pygame.sprite.Group()

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
                       'RFFRRRRFRRRFFFWTWRx',
                       'RFFRRRRFRRRFFFFFFRx',
                       'RFFTWWTFTWWFFFFFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RFFRRRRFFFFFFFFFFRx',
                       'RFFRRRRFFFFFFFFFFRx',
                       'RRRRRRRRRRRRRRRRRRx', ]
        
        items = [Item('health', HealthPotion, 544, 340), Item('special', SpecialPotion, 136 + 68 * 3, 340)]
        roofs = []
        walls = []
        floors = []
        chasms = []
        portals = [Portal(1224, 68 * 3, WallImg, 1), Portal(1224, 68 * 4, WallImg, 1)]
        x, y = 0, 0
        i = 1

        for section in room_layout:
            for surface in section:
                if surface == 'x':
                    x = 0
                else:
                    if surface == 'R':
                        roofs.append(Wall(x, y, RoofImgCenterCenter))
                    elif surface == 'W':
                        walls.append(Wall(x, y, WallImg))
                    elif surface == 'T':
                        walls.append(TorchBrick(x, y, TorchImg1))
                    elif surface == 'F':
                        floors.append(Floor(x, y, FloorImgCenter))

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


class Room2(Room):
    mobs = [ShrimpMob(68 * 2, 68 * 8, 0), ShrimpMob(816 + (68 * 2), 68 * 8, 1)]

    def __init__(self):
        Room.__init__(self)

        room_layout = ['RRRRRRRRRFRRRRRRRRx',
                       'RWWRWWRWWFWRWWRWWRx',
                       'TFFTFFTFFFFTFFTFFRx',
                       'FFFFFFFFFFFFFFFFFTx',
                       'FFFFFFFFFFFFFFFFFFx',
                       'RFFRFFRFFFFRFFRFFRx',
                       'RFFTFFTFFFFTFFTFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RFFRFFRFFFFRFFRFFRx',
                       'RFFTFFTFFFFTFFTFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RRRRRRRRRFRRRRRRRRx', ]

        items = []
        roofs = []
        walls = []
        floors = []
        chasms = []
        lockeddoors = [MapTile(1224 - 68, 272, LockDoorVImg)]
        portals = [Portal(-68, 204, WallImg, 0), Portal(-68, 272, WallImg, 0), Portal(1224, 204, WallImg, 4), Portal(1224, 272, WallImg, 4), Portal(612, -68, WallImg, 2), Portal(612, 1020, WallImg, 3)]

        x, y = 0, 0
        i = 1

        for section in room_layout:
            for surface in section:
                if surface == 'x':
                    x = 0
                else:
                    if surface == 'R':
                        roofs.append(Wall(x, y, RoofImgCenterCenter))
                    elif surface == 'W':
                        walls.append(Wall(x, y, WallImg))
                    elif surface == 'T':
                        walls.append(TorchBrick(x, y, TorchImg1))
                    elif surface == 'F':
                        floors.append(Floor(x, y, FloorImgCenter))

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

        for lock in lockeddoors:
            self.lock_list.add(lock)

class Room3(Room):
    mobs = [ShrimpMob(68 * 2, 68 * 8, 0, 'key'), ShrimpMob(816 + (68 * 2), 68 * 8, 1, None)]

    def __init__(self):
        Room.__init__(self)

        room_layout = ['RRRRRRRRRRRRRRRRRRx',
                       'RWWRWWRWWWWRWWRWWRx',
                       'RFFTFFTFFFFTFFTFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RFFRFFRFFFFRFFRFFRx',
                       'RFFTFFTFFFFTFFTFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RFFRFFRFFFFRFFRFFRx',
                       'RFFTFFTFFFFTFFTFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RRRRRRRRRFRRRRRRRRx', ]

        items = []
        roofs = []
        walls = []
        floors = []
        chasms = []
        portals = [Portal(612, 1020, WallImg, 1)]
        x, y = 0, 0
        i = 1

        for section in room_layout:
            for surface in section:
                if surface == 'x':
                    x = 0
                else:
                    if surface == 'R':
                        roofs.append(Wall(x, y, RoofImgCenterCenter))
                    elif surface == 'W':
                        walls.append(Wall(x, y, WallImg))
                    elif surface == 'T':
                        walls.append(TorchBrick(x, y, TorchImg1))
                    elif surface == 'F':
                        floors.append(Floor(x, y, FloorImgCenter))

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

class Room4(Room):
    mobs = [ShrimpMob(68 * 2, 68 * 8, 0), ShrimpMob(816 + (68 * 2), 68 * 8, 1)]

    def __init__(self):
        Room.__init__(self)

        room_layout = ['RRRRRRRRRFRRRRRRRRx',
                       'RWWRWWRWWFWRWWRWWRx',
                       'RFFTFFTFFFFTFFTFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RFFRFFRFFFFRFFRFFRx',
                       'RFFTFFTFFFFTFFTFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RFFRFFRFFFFRFFRFFRx',
                       'RFFTFFTFFFFTFFTFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RRRRRRRRRRRRRRRRRRx', ]

        items = []
        roofs = []
        walls = []
        floors = []
        chasms = []
        portals = [Portal(612, -68, WallImg, 1)]
        x, y = 0, 0
        i = 1

        for section in room_layout:
            for surface in section:
                if surface == 'x':
                    x = 0
                else:
                    if surface == 'R':
                        roofs.append(Wall(x, y, RoofImgCenterCenter))
                    elif surface == 'W':
                        walls.append(Wall(x, y, WallImg))
                    elif surface == 'T':
                        walls.append(TorchBrick(x, y, TorchImg1))
                    elif surface == 'F':
                        floors.append(Floor(x, y, FloorImgCenter))

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

class Room5(Room):
    mobs = [ShrimpMob(68 * 5, 68 * 6, 0), ShrimpMob(68 * 8, 68 * 8, 1), ShrimpMob(68 * 11, 68 * 6, 2), ShrimpMob(68 * 14, 68 * 8, 3)]
    def __init__(self):
        Room.__init__(self)

        room_layout = ['RRRRRRRRRRRRRRRRRRx',
                       'RRRBBBBBBBBBBBBBBRx',
                       'RWT              Rx',
                       'TFF              Rx',
                       'FFF              Rx',
                       'RFF              Wx',
                       'RFFFFFFFFFFFFFFFFFx',
                       'RFFFFFFFFFFFFFFFFFx',
                       'RFFFFFFFFFFFFFFFFFx',
                       'RBBBBBBBBBBBBBBBBRx',
                       'R                Rx',
                       'R                Rx',
                       'R                Rx',
                       'RRRRRRRRRRRRRRRRRRx', ]

        items = []
        roofs = []
        walls = []
        floors = []
        chasms = []
        portals = [Portal(-68, 204, WallImg, 1), Portal(-68, 272, WallImg, 1), Portal(1224, 408, WallImg, 5), Portal(1224, 476, WallImg, 5), Portal(1224, 544, WallImg, 5)]
        x, y = 0, 0
        i = 1

        for section in room_layout:
            for surface in section:
                if surface == 'x':
                    x = 0
                else:
                    if surface == 'R':
                        roofs.append(Wall(x, y, RoofImgCenterCenter))
                    elif surface == 'W':
                        walls.append(Wall(x, y, WallImg))
                    elif surface == 'T':
                        walls.append(TorchBrick(x, y, TorchImg1))
                    elif surface == 'F':
                        floors.append(Floor(x, y, FloorImgCenter))
                    elif surface == ' ':
                        walls.append(Wall(x, y, ChasmImgTop))
                    elif surface == 'B':
                        chasms.append(Wall(x, y, ChasmImgBottom))

                    x += 68
            y += 68

        for wall in walls:
            self.wall_list.add(wall)

        for roof in roofs:
            self.roof_list.add(roof)

        for floor in floors:
            self.floor_list.add(floor)

        for chasm in chasms:
            self.chasm_list.add(chasm)

        for item in items:
            self.item_list.add(item)

        for mob in self.mobs:
            self.mob_list.add(mob)

        for portal in portals:
            self.portal_list.add(portal)


class Room6(Room):
    mobs = [ShrimpMob(68 * 5, 68 * 3, 0), ShrimpMob(68 * 8, 68 * 5, 1), ShrimpMob(68 * 11, 68 * 3, 2), ShrimpMob(68 * 14, 68 * 5, 3), ShrimpMob(68 * 5, 68 * 7, 4), ShrimpMob(68 * 8, 68 * 9, 5), ShrimpMob(68 * 11, 68 * 7, 6), ShrimpMob(68 * 14, 68 * 9, 7)]
    def __init__(self):
        Room.__init__(self)

        room_layout = ['RRRRRRRRRRRRRRRRRRx',
                       'RRRWTWWWTWWWTWWRRRx',
                       'RWWFFFFFFFFFFFFWWRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'WFFFFFFFFFFFFFFFFRx',
                       'FFFFFFFFFFFFFFFFFRx',
                       'FFFFFFFFFFFFFFFFFRx',
                       'FFFFFFFFFFFFFFFFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RFFFFFFFFFFFFFFFFRx',
                       'RRRRFFFFFFFFFFRRRRx',
                       'RRRRRRRRRRRRRRRRRRx',
                       'RRRRRRRRRRRRRRRRRRx', ]

        items = []
        roofs = []
        walls = []
        floors = []
        chasms = []
        portals = []
        x, y = 0, 0
        i = 1

        for section in room_layout:
            for surface in section:
                if surface == 'x':
                    x = 0
                else:
                    if surface == 'R':
                        roofs.append(Wall(x, y, RoofImgCenterCenter))
                    elif surface == 'W':
                        walls.append(Wall(x, y, WallImg))
                    elif surface == 'T':
                        walls.append(TorchBrick(x, y, TorchImg1))
                    elif surface == 'F':
                        floors.append(Floor(x, y, FloorImgCenter))

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
