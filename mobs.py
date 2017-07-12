import pygame, math
from image_loader import *
from rooms import *


class Mob(pygame.sprite.Sprite):
    def __init__(self, image, x, y, hp, id):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = hp
        self.id = id
        self.damage = 20

        # this is the bounds to check against
        self.aggro_right = self.rect.x + 400
        self.aggro_left = self.rect.x - 400
        self.aggro_top = self.rect.y - 400
        self.aggro_bottom = self.rect.y + 400

    def follow_hero(self, Hero):
        # find direction vector from hero to enemy
        direction_x = Hero.rect.x - self.rect.x
        direction_y = Hero.rect.y - self.rect.y
        direction = math.hypot(direction_x, direction_y)
        direction_x /= direction
        direction_y /= direction

        self.rect.x += self.speed * direction_x
        self.rect.y += self.speed * direction_y

    # does something but not sure what, kind of moves you in a random direction
    def move_to_coordinate(self, destination_x=0, destination_y=0):
        direction_x = destination_x - self.rect.x
        direction_y = destination_y - self.rect.y
        direction = math.hypot(direction_x, direction_y)
        direction_x /= direction
        direction_y /= direction
        self.rect.x += self.speed * direction_x
        self.rect.y += self.speed * direction_y

    def look_for_hero(self, Hero):
        print "LOOKING FOR HERO"
        if Hero.rect.y <= self.aggro_bottom and Hero.rect.y >= self.aggro_top:
            print "FOUND HERO Y DIRECTION"
            if Hero.rect.x >= self.aggro_left and Hero.rect.x <= self.aggro_right:
                print "FOUND HERO X DIRECTION"
                return True
        return False

    def take_damage(self, damage, hero):
        self.hp -= damage
        print "mob took", damage, "damage"
        if self.hp <= 0:
            self.kill()
            print "mob", self.id, "ded"
            hero.remove_mob_with_id(self.id)


class ShrimpMob(Mob):
    def __init__(self, x, y, id):
        self.walk1 = pygame.image.load('images/mobs/shrimp/left/walk1.png')
        Mob.__init__(self, self.walk1, x, y, 100, id)

        self.walk2 = pygame.image.load('images/mobs/shrimp/left/walk2.png')

        self.aggro1 = pygame.image.load('images/mobs/shrimp/left/aggro1.png')
        self.aggro2 = pygame.image.load('images/mobs/shrimp/left/aggro2.png')

        self.neutral_animation = [self.walk1, self.walk2]
        self.aggro_animation = [self.aggro1, self.aggro2]

        self.speed = 5

        self.current_frame = 0
        self.ticker = 0

    def update(self):
        self.image = self.neutral_animation[self.current_frame]

        self.ticker += 1
        # originally set to mod 15
        if self.ticker % 5 == 0:
            self.current_frame = (self.current_frame + 1) % 2
            self.ticker = 0
