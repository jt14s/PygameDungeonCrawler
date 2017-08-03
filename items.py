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

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed, walls, roofs, mobs, hero):
        pygame.sprite.Sprite.__init__(self)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.original_x = x
        self.original_y = y
        self.direction = direction
        self.speed = speed

        self.walls = walls
        self.roofs = roofs
        self.mobs = mobs
        self.hero = hero
        self.bolt_timer = -1
        self.max_range_reached = False

    def update(self):
        if self.direction == 'RIGHT':
            if self.max_range_reached == False:
                self.rect.x += self.speed
            if self.original_x + 400 <= self.rect.x and self.max_range_reached == False:
                self.image = self.projectile_right[1]
                self.bolt_timer = 5
                self.max_range_reached = True
        elif self.direction == 'LEFT':
            if self.max_range_reached == False:
                self.rect.x -= self.speed
            if self.original_x - 400 >= self.rect.x and self.max_range_reached == False:
                self.image = self.projectile_right[1]
                self.bolt_timer = 5
                self.max_range_reached = True
        elif self.direction == 'DOWN':
            if self.max_range_reached == False:
                self.rect.y += self.speed
            if self.original_y + 362 <= self.rect.y and self.max_range_reached == False:
                self.image = self.projectile_right[1]
                self.bolt_timer = 5
                self.max_range_reached = True
        elif self.direction == 'UP':
            if self.max_range_reached == False:
                self.rect.y -= self.speed
            if self.original_y - 380 >= self.rect.y and self.max_range_reached == False:
                self.image = self.projectile_right[1]
                self.bolt_timer = 5
                self.max_range_reached = True

        if self.rect.x < 0 or self.rect.x > 1224 or self.rect.y < 0 or self.rect.y > 952:
            self.kill()

        projectile = pygame.sprite.GroupSingle(self)
        wall_hit_list = pygame.sprite.groupcollide(self.walls, projectile, False, True)
        roof_hit_list = pygame.sprite.groupcollide(self.roofs, projectile, False, True)
        mob_hit_list = pygame.sprite.groupcollide(self.mobs, projectile, False, True)

        #the rope has hit a mob
        for mob in mob_hit_list:
            mob.take_damage(self.damage, self.hero)
            
        if self.bolt_timer > 0:
            self.image = self.projectile_right[1]
            self.bolt_timer -= 1
        elif self.bolt_timer == 0:
            self.kill()
            self.bolt_timer = -1
            
class Bolt(Projectile):
    def __init__(self, x, y, direction, walls, roofs, mobs, hero):
        self.projectile_up = [MageProjectileU1, MageProjectileU2]
        self.projectile_down = [MageProjectileD1, MageProjectileD2]
        self.projectile_left = [MageProjectileL1, MageProjectileL2]
        self.projectile_right = [MageProjectileR1, MageProjectileR2]

        self.damage = 17

        if direction == 'RIGHT':
            self.image = MageProjectileR1
            Projectile.__init__(self, x + 64, y + 10, direction, 8, walls, roofs, mobs, hero)
        if direction == 'LEFT':
            self.image = MageProjectileL1
            Projectile.__init__(self, x + 34, y + 15, direction, 8, walls, roofs, mobs, hero)
        if direction == 'UP':
            self.image = MageProjectileU1
            Projectile.__init__(self, x + 8, y - 20, direction, 8, walls, roofs, mobs, hero)
        if direction == 'DOWN':
            self.image = MageProjectileD1
            Projectile.__init__(self, x + 50, y + 38, direction, 8, walls, roofs, mobs, hero)
