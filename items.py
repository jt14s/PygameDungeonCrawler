import pygame
from image_loader import *

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

class Bow(Item):
    def __init__(self, name, image, x, y):
        Item.__init__(self, name, image, x, y)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, walls, roofs, mobs):
        pygame.sprite.Sprite.__init__(self)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction

        self.walls = walls
        self.roofs = roofs
        self.mobs = mobs

    def update(self):
        if self.direction == 'right':
            self.rect.x += self.speed
        elif self.direction == 'left':
            self.rect -= self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'up':
            self.rect.y -= self.speed

        projectile = pygame.sprite.GroupSingle(self)
        wall_hit_list = pygame.sprite.groupcollide(self.walls, projectile, False, True)
        roof_hit_list = pygame.sprite.groupcollide(self.roofs, projectile, False, True)
        mob_hit_list = pygame.sprite.groupcollide(self.mobs, projectile, False, True)

        #the rope has hit a mob
        for mob in mob_hit_list:
            print 'hit mob with projectile'

class ThrownRope(Projectile):
    def __init__(self, x, y, direction, walls, roofs, mobs):
        if direction == 'down' or direction == 'up':
            self.image = ThrownRopeDown
        self.speed = 18
        Projectile.__init__(self, x, y, direction, walls, roofs, mobs)

class Arrow(Projectile):
    def __init__(self, x, y, direction, walls, roofs, mobs):
        if direction == 'down' or direction == 'up':
            self.image = ThrownRopeDown
        self.speed = 30
        Projectile.__init__(self, x, y, direction, walls, roofs, mobs)
