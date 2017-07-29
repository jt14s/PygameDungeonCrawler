import pygame, math
from image_loader import *
from rooms import *

class Mob(pygame.sprite.Sprite):
    walls = None
    roofs = None

    def __init__(self, image, x, y, hp, damage, knockback, id):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ORIG_X = x
        self.ORIG_Y = y
        self.hp = hp
        self.id = id
        self.damage = damage
        self.knockback = knockback
        self.state = "neutral"

        self.angle = 360
        self.direction_x = None
        self.direction_y = None
        self.DIRECTION = None

    def follow_hero(self, Hero):
        # find direction vector from hero to enemy
        self.direction_x = Hero.rect.x - self.rect.x
        self.direction_y = Hero.rect.y - self.rect.y
        direction = math.hypot(self.direction_x, self.direction_y)
        if direction != 0:
            self.direction_x = int((self.direction_x / direction)*self.speed)
            self.direction_y = int((self.direction_y / direction)*self.speed)
            self.angle = math.degrees(math.atan2(self.direction_y, self.direction_x))

    # does something but not sure what, kind of moves you in a random direction
    def move_to_coordinate(self, destination_x = 0, destination_y = 0):
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
        self.aggro_right = self.rect.x + 300
        self.aggro_left = self.rect.x - 300
        self.aggro_top = self.rect.y - 300
        self.aggro_bottom = self.rect.y + 300

        #this is bounds to check to attack
        self.attack_right = self.rect.x + 80
        self.attack_left = self.rect.x - 80
        self.attack_top = self.rect.y - 80
        self.attack_bottom = self.rect.y + 80

        if Hero.rect.y <= self.attack_bottom and Hero.rect.y >= self.attack_top:
            if Hero.rect.x >= self.attack_left and Hero.rect.x <= self.attack_right:
                self.state = "attack"
                return True
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
        else:
            mob = pygame.sprite.GroupSingle(self)
            if hero.DIRECTION == hero.LEFT:
                for x in range(0, hero.knockback):
                    self.rect.x -= 1

                    interaction = False

                    roof_hit_list = pygame.sprite.groupcollide(mob, self.roofs, False, False, collided=pygame.sprite.collide_rect_ratio(.75))
                    wall_hit_list = pygame.sprite.groupcollide(mob, self.walls, False, False, collided=pygame.sprite.collide_rect_ratio(.75))

                    for wall in wall_hit_list:
                        if not interaction:
                            self.rect.left = wall.rect.right - 55
                            interaction = True
                
                    for roof in roof_hit_list:
                        if not interaction:
                            self.rect.left = roof.rect.right - 55
                            interaction = True
                
                    if interaction == True:
                        break
        
            elif hero.DIRECTION == hero.RIGHT:
                for x in range(0, hero.knockback):
                    self.rect.x += 1

                    interaction = False

                    roof_hit_list = pygame.sprite.groupcollide(mob, self.roofs, False, False,
                                                                           collided=pygame.sprite.collide_rect_ratio(.75))
                    wall_hit_list = pygame.sprite.groupcollide(mob, self.walls, False, False,
                                                               collided=pygame.sprite.collide_rect_ratio(.75))

                    for wall in wall_hit_list:
                        if not interaction:
                            self.rect.right = wall.rect.left + 55
                            interaction = True
                
                    for roof in roof_hit_list:
                        if not interaction:
                            self.rect.right = roof.rect.left + 55
                            interaction = True
                    
                    if interaction == True:
                        break

            elif hero.DIRECTION == hero.UP:
                for y in range(0, hero.knockback):
                    self.rect.y -= 1

                    interaction = False

                    roof_hit_list = pygame.sprite.groupcollide(mob, self.roofs, False, False,
                                                               collided=pygame.sprite.collide_rect_ratio(.52))
                    wall_hit_list = pygame.sprite.groupcollide(mob, self.walls, False, False,
                                                               collided=pygame.sprite.collide_rect_ratio(.52))

                    for wall in wall_hit_list:
                        if not interaction:
                            self.rect.top = wall.rect.bottom - 63
                            interaction = True
                
                    for roof in roof_hit_list:
                        if not interaction:
                            self.rect.top = roof.rect.bottom - 63
                            interaction = True

                    if interaction == True:
                        break
                        
            elif hero.DIRECTION == hero.DOWN:
                for y in range(0, hero.knockback):
                    self.rect.y += 1

                    interaction = False

                    roof_hit_list = pygame.sprite.groupcollide(mob, self.roofs, False, False,
                                                               collided=pygame.sprite.collide_rect_ratio(.52))
                    wall_hit_list = pygame.sprite.groupcollide(mob, self.walls, False, False,
                                                               collided=pygame.sprite.collide_rect_ratio(.52))

                    for wall in wall_hit_list:
                        if not interaction:
                            self.rect.bottom = wall.rect.top + 63
                            interaction = True
                
                    for roof in roof_hit_list:
                        if not interaction:
                            self.rect.bottom = roof.rect.top + 63
                            interaction = True
                
                    if interaction == True:
                        break




class ShrimpMob(Mob):
    def __init__(self, x, y, id):
        Mob.__init__(self, ShrimpWalkL1, x, y, 100, 20, 30, id)

        self.walk_animation_left = [ShrimpWalkL1,ShrimpWalkL2,ShrimpWalkL1,ShrimpWalkL2]
        self.walk_animation_right = [ShrimpWalkR1,ShrimpWalkR2,ShrimpWalkR1,ShrimpWalkR2]
        self.walk_animation_up = [ShrimpWalkU1,ShrimpWalkU2,ShrimpWalkU1,ShrimpWalkU2]
        self.walk_animation_down = [ShrimpWalkD1,ShrimpWalkD2,ShrimpWalkD1,ShrimpWalkD2]

        self.aggro_animation_left = [ShrimpAggroLeft1, ShrimpAggroLeft2,ShrimpAggroLeft1, ShrimpAggroLeft2]
        self.aggro_animation_right = [ShrimpAggroRight1, ShrimpAggroRight2,ShrimpAggroRight1, ShrimpAggroRight2]
        self.aggro_animation_down = [ShrimpAggroDown1, ShrimpAggroDown2,ShrimpAggroDown1, ShrimpAggroDown2]

        self.attack_animation_left = [ShrimpAttackL1, ShrimpAttackL2, ShrimpAttackL3, ShrimpAttackL3]
        self.attack_animation_right = [ShrimpAttackR1, ShrimpAttackR2, ShrimpAttackR3, ShrimpAttackR3]
        self.attack_animation_up = [ShrimpAttackU1, ShrimpAttackU2, ShrimpAttackU3, ShrimpAttackU3]
        self.attack_animation_down = [ShrimpAttackD1, ShrimpAttackD2, ShrimpAttackD3, ShrimpAttackD3]

        self.speed = 4

        self.current_frame = 0
        self.ticker = 0
        self.attack_timer = 0

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
                self.attack_timer = 0
                if self.DIRECTION == "left":
                    self.image = self.walk_animation_left[self.current_frame]
                elif self.DIRECTION == "right":
                    self.image = self.walk_animation_right[self.current_frame]
                elif self.DIRECTION == "up":
                    self.image = self.walk_animation_up[self.current_frame]
                elif self.DIRECTION == "down":
                    self.image = self.walk_animation_down[self.current_frame]
            elif self.state == "attack":
                if self.DIRECTION == "left":
                    if self.attack_timer != 0 and self.attack_timer % 3 == 0:
                        self.rect.x = self.rect.x + 21
                    self.rect.x = self.rect.x - 7
                    self.image = self.attack_animation_left[self.current_frame]
                elif self.DIRECTION == "right":
                    if self.attack_timer != 0 and self.attack_timer % 3 == 0:
                        self.rect.x = self.rect.x - 21
                    self.rect.x = self.rect.x + 7
                    self.image = self.attack_animation_right[self.current_frame]
                elif self.DIRECTION == "up":
                    if self.attack_timer != 0 and self.attack_timer % 3 == 0:
                        self.rect.y = self.rect.y + 21
                    self.rect.y = self.rect.y - 7
                    self.image = self.attack_animation_up[self.current_frame]
                elif self.DIRECTION == "down":
                    if self.attack_timer != 0 and self.attack_timer % 3 == 0:
                        self.rect.y = self.rect.y - 21
                    self.rect.y = self.rect.y + 7
                    self.image = self.attack_animation_down[self.current_frame]
                self.attack_timer += 1
            elif self.state == "aggro":
                self.attack_timer = 0
                if self.DIRECTION == "left":
                    self.image = self.aggro_animation_left[self.current_frame]
                elif self.DIRECTION == "right":
                    self.image = self.aggro_animation_right[self.current_frame]
                elif self.DIRECTION == "up":
                    self.image = self.walk_animation_up[self.current_frame]
                    #cant see aggro face when up so used walk instead
                elif self.DIRECTION == "down":
                    self.image = self.aggro_animation_down[self.current_frame]

                shrimp = pygame.sprite.GroupSingle(self)

                interaction_x = False
                interaction_y = False

                counter_x = 0
                counter_y = 0
                
                if self.roofs != None and self.walls != None:
                    while not((interaction_x or counter_x == self.direction_x) and (interaction_y or counter_y == self.direction_y)):
                        if self.direction_x < 0 and not interaction_x:
                            if counter_x > self.direction_x:
                                self.rect.x -= 1

                                interaction_x = False

                                roof_hit_list = pygame.sprite.groupcollide(shrimp, self.roofs, False, False, collided=pygame.sprite.collide_rect_ratio(.52))
                                wall_hit_list = pygame.sprite.groupcollide(shrimp, self.walls, False, False, collided=pygame.sprite.collide_rect_ratio(.52))

                                for wall in wall_hit_list:
                                    if not interaction_x:
                                        self.rect.left = wall.rect.right - 55
                                        interaction_x = True
                            
                                for roof in roof_hit_list:
                                    if not interaction_x:
                                        self.rect.left = roof.rect.right - 55
                                        interaction_x = True
                            
                                counter_x -= 1
                        elif self.direction_x > 0 and not interaction_x:
                            if counter_x < self.direction_x:
                                self.rect.x += 1

                                interaction_x = False

                                roof_hit_list = pygame.sprite.groupcollide(shrimp, self.roofs, False, False,
                                                                           collided=pygame.sprite.collide_rect_ratio(.52))
                                wall_hit_list = pygame.sprite.groupcollide(shrimp, self.walls, False, False,
                                                                           collided=pygame.sprite.collide_rect_ratio(.52))

                                for wall in wall_hit_list:
                                    if not interaction_x:
                                        self.rect.right = wall.rect.left + 55
                                        interaction_x = True
                            
                                for roof in roof_hit_list:
                                    if not interaction_x:
                                        self.rect.right = roof.rect.left + 55
                                        interaction_x = True
                            
                                counter_x += 1

                        if self.direction_y > 0 and not interaction_y:
                            if counter_y < self.direction_y:
                                self.rect.y += 1

                                interaction_y = False

                                roof_hit_list = pygame.sprite.groupcollide(shrimp, self.roofs, False, False,
                                                                           collided=pygame.sprite.collide_rect_ratio(.52))
                                wall_hit_list = pygame.sprite.groupcollide(shrimp, self.walls, False, False,
                                                                           collided=pygame.sprite.collide_rect_ratio(.52))

                                for wall in wall_hit_list:
                                    if not interaction_y:
                                        self.rect.bottom = wall.rect.top + 63
                                        interaction_y = True
                            
                                for roof in roof_hit_list:
                                    if not interaction_y:
                                        self.rect.bottom = roof.rect.top + 63
                                        interaction_y = True
                            
                                counter_y += 1

                        elif self.direction_y < 0 and not interaction_y:
                            if counter_y > self.direction_y:
                                self.rect.y -= 1

                                interaction_y = False

                                roof_hit_list = pygame.sprite.groupcollide(shrimp, self.roofs, False, False,
                                                                           collided=pygame.sprite.collide_rect_ratio(.52))
                                wall_hit_list = pygame.sprite.groupcollide(shrimp, self.walls, False, False,
                                                                           collided=pygame.sprite.collide_rect_ratio(.52))

                                for wall in wall_hit_list:
                                    if not interaction_y:
                                        self.rect.top = wall.rect.bottom - 63
                                        interaction_y = True
                            
                                for roof in roof_hit_list:
                                    if not interaction_y:
                                        self.rect.top = roof.rect.bottom - 63
                                        interaction_y = True
                            
                                counter_y -= 1


        self.ticker += 1
        if self.ticker % 5 == 0:
            self.current_frame = (self.current_frame+1) % 4
            self.ticker = 0

