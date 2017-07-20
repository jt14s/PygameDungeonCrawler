import pygame, math
from image_loader import *
from rooms import *

#Add knockback on player after being hit and try to isolate bug where enemy keeps moving
#Add attack animations, whenever collide do attack


class Mob(pygame.sprite.Sprite):
    walls = None
    roofs = None

    def __init__(self, image, x, y, hp, id):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ORIG_X = x
        self.ORIG_Y = y
        self.hp = hp
        self.id = id
        self.damage = 20
        self.state = "neutral"

        self.angle = 360

        self.DIRECTION = None

        # this is the bounds to check against
        self.aggro_right = self.rect.x + 300
        self.aggro_left = self.rect.x - 300
        self.aggro_top = self.rect.y - 300
        self.aggro_bottom = self.rect.y + 300

    def follow_hero(self, Hero):
        # find direction vector from hero to enemy
        direction_x = Hero.rect.x - self.rect.x
        direction_y = Hero.rect.y - self.rect.y
        direction = math.hypot(direction_x, direction_y)
        if direction != 0:
            direction_x /= direction
            direction_y /= direction
            self.angle = math.degrees(math.atan2(direction_y, direction_x))
            self.rect.x += self.speed * direction_x
            self.rect.y += self.speed * direction_y

    # does something but not sure what, kind of moves you in a random direction
    def move_to_coordinate(self, destination_x=0, destination_y=0):
        direction_x = destination_x - self.rect.x
        direction_y = destination_y - self.rect.y
        direction = math.hypot(direction_x, direction_y)
        self.angle = math.degrees(math.atan2(direction_y, direction_x))

        if direction != 0:
            direction_x /= direction
            direction_y /= direction
            self.rect.x += self.speed * direction_x
            self.rect.y += self.speed * direction_y

    def look_for_hero(self, Hero):
        # print "LOOKING FOR HERO"
        if Hero.rect.y <= self.aggro_bottom and Hero.rect.y >= self.aggro_top:
            if Hero.rect.x >= self.aggro_left and Hero.rect.x <= self.aggro_right:
                self.state = "aggro"
                return True
        self.state = "neutral"
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
        self.walk1 = ShrimpWalkL1
        Mob.__init__(self, self.walk1, x, y, 100, id)

        self.walk_animation_left = [ShrimpWalkL1,ShrimpWalkL2]
        self.walk_animation_right = [ShrimpWalkR1,ShrimpWalkR2]
        self.walk_animation_up = [ShrimpWalkU1,ShrimpWalkU2]
        self.walk_animation_down = [ShrimpWalkD1,ShrimpWalkD2]

        self.aggro_animation_left = [ShrimpAggroLeft1, ShrimpAggroLeft2]

        self.speed = 4

        self.current_frame = 0
        self.ticker = 0

    def update(self):
        if self.angle <= 45 and self.angle > -45:
            self.DIRECTION = "right"
        elif self.angle <= 135 and self.angle > 45:
            self.DIRECTION = "down"
        elif self.angle > -135 and self.angle <= -45:
            self.DIRECTION = "up"
        elif self.angle > 135 and self.angle <= 180 or self.angle < -135 and self.angle >= -180:
            self.DIRECTION = "left"


        if self.DIRECTION != None:
            if self.state == "neutral":
                if self.DIRECTION == "left":
                    self.image = self.walk_animation_left[self.current_frame]
                elif self.DIRECTION == "right":
                    self.image = self.walk_animation_right[self.current_frame]
                elif self.DIRECTION == "up":
                    self.image = self.walk_animation_up[self.current_frame]
                elif self.DIRECTION == "down":
                    self.image = self.walk_animation_down[self.current_frame]
            elif self.state == "aggro":
                if self.DIRECTION == "left":
                    self.image = self.aggro_animation_left[self.current_frame]
                elif self.DIRECTION == "right":
                    self.image = self.walk_animation_right[self.current_frame]
                elif self.DIRECTION == "up":
                    self.image = self.walk_animation_up[self.current_frame]
                elif self.DIRECTION == "down":
                    self.image = self.walk_animation_down[self.current_frame]

            shrimp = pygame.sprite.GroupSingle(self)

            interaction = False

            if self.roofs != None and self.walls != None:
                if self.DIRECTION == "up":
                    for y in range(0, self.speed):
                        self.rect.y -= 1

                        interaction = False

                        roof_hit_list = pygame.sprite.groupcollide(shrimp, self.roofs, False, False,
                                                                   collided=pygame.sprite.collide_rect_ratio(.52))
                        wall_hit_list = pygame.sprite.groupcollide(shrimp, self.walls, False, False,
                                                                   collided=pygame.sprite.collide_rect_ratio(.52))

                        for wall in wall_hit_list:
                            self.rect.top = wall.rect.bottom - 63
                            interaction = True
                            print "hit"
                        for roof in roof_hit_list:
                            self.rect.top = roof.rect.bottom - 63
                            interaction = True
                            print "hit"

                        if interaction == True:
                            break

                elif self.DIRECTION == "down":

                    for y in range(0, self.speed):
                        self.rect.y += 1

                        interaction = False

                        roof_hit_list = pygame.sprite.groupcollide(shrimp, self.roofs, False, False,
                                                                   collided=pygame.sprite.collide_rect_ratio(.52))
                        wall_hit_list = pygame.sprite.groupcollide(shrimp, self.walls, False, False,
                                                                   collided=pygame.sprite.collide_rect_ratio(.52))

                        for roof in roof_hit_list:
                            self.rect.bottom = roof.rect.top + 63
                            interaction = True
                            print "hit"
                        for wall in wall_hit_list:
                            self.rect.bottom = wall.rect.top + 63
                            interaction = True
                            print "hit"


                        if interaction == True:
                            break

                elif self.DIRECTION == "left":

                    for x in range(0, self.speed):
                        self.rect.x -= 1

                        interaction = False

                        roof_hit_list = pygame.sprite.groupcollide(shrimp, self.roofs, False, False,
                                                                   collided=pygame.sprite.collide_rect_ratio(.52))
                        wall_hit_list = pygame.sprite.groupcollide(shrimp, self.walls, False, False,
                                                                   collided=pygame.sprite.collide_rect_ratio(.52))

                        for wall in wall_hit_list:
                            self.rect.left = wall.rect.right - 63
                            interaction = True
                            print "hit"

                        for roof in roof_hit_list:
                            self.rect.left = roof.rect.right - 63
                            interaction = True
                            print "hit"

                        if interaction == True:
                            break

                elif self.DIRECTION == "right":
                    for x in range(0, self.speed):
                        self.rect.x += 1

                        interaction = False

                        roof_hit_list = pygame.sprite.groupcollide(shrimp, self.roofs, False, False,
                                                                   collided=pygame.sprite.collide_rect_ratio(.52))
                        wall_hit_list = pygame.sprite.groupcollide(shrimp, self.walls, False, False,
                                                                   collided=pygame.sprite.collide_rect_ratio(.52))

                        for wall in wall_hit_list:
                            self.rect.right = wall.rect.left + 63
                            interaction = True
                            print "hit"

                        for roof in roof_hit_list:
                            self.rect.right = roof.rect.left + 63
                            interaction = True
                            print "hit"

                        if interaction == True:
                            break

        self.ticker += 1
        # originally set to mod 15
        if self.ticker % 5 == 0:
            self.current_frame = (self.current_frame + 1) % 2
            self.ticker = 0

