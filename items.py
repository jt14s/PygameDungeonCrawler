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
        if self.direction == 'RIGHT':
            self.rect.x += self.speed
        elif self.direction == 'LEFT':
            self.rect.x -= self.speed
        elif self.direction == 'DOWN':
            self.rect.y += self.speed
        elif self.direction == 'UP':
            self.rect.y -= self.speed

        if self.rect.x < 0 or self.rect.x > 1224 or self.rect.y < 0 or self.rect.y > 952:
            self.kill()

        projectile = pygame.sprite.GroupSingle(self)
        wall_hit_list = pygame.sprite.groupcollide(self.walls, projectile, False, True)
        roof_hit_list = pygame.sprite.groupcollide(self.roofs, projectile, False, True)
        mob_hit_list = pygame.sprite.groupcollide(self.mobs, projectile, False, True)

        #the rope has hit a mob
        for mob in mob_hit_list:
            print 'hit mob with projectile'

class ThrownRope(Projectile):
    def __init__(self, x, y, direction, walls, roofs, mobs):
        if direction == 'DOWN' or direction == 'UP':
            self.image = ThrownRopeDown

        elif direction == 'LEFT' or direction == 'RIGHT':
            self.image = ThrownRopeDown

        self.speed = 18

        if direction == 'UP':
            Projectile.__init__(self, x, y - 60, direction, walls, roofs, mobs)
        else:
            Projectile.__init__(self, x, y, direction, walls, roofs, mobs)    
