import pygame
from image_loader import *

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
        self.item_name = ''

    def addToInventory(self, name, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.item_name = name
