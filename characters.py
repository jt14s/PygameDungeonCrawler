import pygame, sys
from image_loader import *
from items import *
from hud import *
from game import *

class Sprite(pygame.sprite.Sprite):
    ''' Creates a sprite object '''
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Hero(Sprite):
    ''' Defines attributes and methods shared by all classes '''

    # attributes to be shared by all instances of Hero
    current_room = None
    current_x = 0

    walls = None
    floors = None
    roofs = None
    mobs = None
    portals = None

    def __init__(self, image, x, y, DIRECTION, screen):
        ''' Initialize all of the attributes '''
        Sprite.__init__(self, image, x, y)
        
        # frame info
        self.ticker = 0
        self.current_frame = 0
        
        # hud elements
        self.screen = screen
        self.ui = UI((screen.get_width() / 6) + 10, 10, self.hp, self.sp, screen)
        self.inventory = Inventory(InvImg, (screen.get_width() / 2) - 70, (screen.get_height() / 1.1))
        self.item_slot_group = pygame.sprite.Group()

        # movement info
        self.can_move = True
        self.DIRECTION = DIRECTION
        self.RIGHT, self.LEFT, self.UP, self.DOWN = "RIGHT LEFT UP DOWN".split()
        
        self.upKeyPressed = False
        self.downKeyPressed = False
        self.leftKeyPressed = False
        self.rightKeyPressed = False

        # attack info
        self.can_attack = True
        self.attack_timer = -1
        self.invuln_frames = 0

        self.spacePressed = False
        self.specialPressed = False
        
        # items info
        self.items = None
        self.oneKeyPressed = False
        self.twoKeyPressed = False

        # input info
        self.buffer = None
        self.buffer_type = None

        # misc
        self.projectiles = pygame.sprite.Group()

    def update(self):
        ''' Updates the hero every frame '''
        player = pygame.sprite.GroupSingle(self)

        # calculate collision groups
        #
        # prevents damage taken on attack hitbox
        if self.attack_timer >= 0:
            if self.DIRECTION == self.LEFT:
                mob_hit_list = pygame.sprite.groupcollide(self.mobs, player, False, False, collided=pygame.sprite.collide_rect_ratio(self.attack_left_ratio))
            elif self.DIRECTION == self.UP:
                mob_hit_list = pygame.sprite.groupcollide(self.mobs, player, False, False, collided=pygame.sprite.collide_rect_ratio(self.attack_up_ratio))
            else:
                mob_hit_list = pygame.sprite.groupcollide(self.mobs, player, False, False)
        else:
            mob_hit_list = pygame.sprite.groupcollide(self.mobs, player, False, False)

        item_hit_list = pygame.sprite.groupcollide(self.items, player, True, False)

        # actions on collision
        #
        # add items to inventory
        for item in item_hit_list:
            for slot in self.inventory.slots:
                if slot[1] == 'empty':
                    slot[0].addToInventory(item.name, item.image, self.inventory.rect.x + 21 + (slot[0].index * 60), self.inventory.rect.y + 23)
                    slot[1] = 'used'
                    self.item_slot_group.add(slot[0])
                    break

        # mob collision
        for mob in mob_hit_list:
            if self.invuln_frames == 0:
                self.ui.hp_bar.updateHealth(mob.damage, self.hp, self.MAX_HP)
                self.hp -= mob.damage
                self.invuln_frames = 20
                
                # knock hero back
                ''' For loop up to how many pixels hero should be knocked back. Stop knockback on collision '''
                if mob.DIRECTION == "left":
                    for x in range(0, mob.knockback):
                        self.rect.x -= 1
                        interaction = False

                        roof_hit_list = pygame.sprite.groupcollide(player, self.roofs, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
                        wall_hit_list = pygame.sprite.groupcollide(player, self.walls, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
                        portal_hit_list = pygame.sprite.groupcollide(self.portals, player, False, False, collided=pygame.sprite.collide_rect_ratio(1))                        

                        for wall in wall_hit_list:
                            self.rect.left = wall.rect.right - 63
                            interaction = True

                        for roof in roof_hit_list:
                            self.rect.left = roof.rect.right - 63
                            interaction = True

                        for portal in portal_hit_list:
                            self.rect.y = portal.rect.y
                            self.rect.x = self.screen.get_width() - 68
                            self.current_x = portal.room_x
                            interaction = True

                        if interaction == True:
                            break
                        
                elif mob.DIRECTION == "right":
                    for x in range(0, mob.knockback):
                        self.rect.x += 1
                        interaction = False

                        roof_hit_list = pygame.sprite.groupcollide(player, self.roofs, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
                        wall_hit_list = pygame.sprite.groupcollide(player, self.walls, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
                        portal_hit_list = pygame.sprite.groupcollide(self.portals, player, False, False, collided=pygame.sprite.collide_rect_ratio(1))

                        for wall in wall_hit_list:
                            self.rect.right = wall.rect.left + 63
                            interaction = True

                        for roof in roof_hit_list:
                            self.rect.right = roof.rect.left + 63
                            interaction = True

                        for portal in portal_hit_list:
                            self.rect.y = portal.rect.y
                            self.rect.x = 0
                            self.current_x = portal.room_x
                            interaction = True

                        if interaction == True:
                            break

                elif mob.DIRECTION == "up":
                    for y in range(0, mob.knockback):
                        self.rect.y -= 1
                        interaction = False

                        wall_hit_list = pygame.sprite.groupcollide(player, self.walls, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
                        portal_hit_list = pygame.sprite.groupcollide(self.portals, player, False, False, collided=pygame.sprite.collide_rect_ratio(1))

                        for wall in wall_hit_list:
                            self.rect.top = wall.rect.bottom - 63
                            interaction = True

                        for portal in portal_hit_list:
                            self.rect.y = self.screen.get_height() - 68
                            self.rect.x = portal.rect.x
                            self.current_x = portal.room_x
                            interaction = True

                        if interaction == True:
                            break
                            
                elif mob.DIRECTION == "down":
                    for y in range(0, mob.knockback):
                        self.rect.y += 1
                        interaction = False

                        roof_hit_list = pygame.sprite.groupcollide(player, self.roofs, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
                        portal_hit_list = pygame.sprite.groupcollide(self.portals, player, False, False, collided=pygame.sprite.collide_rect_ratio(1))

                        for roof in roof_hit_list:
                            self.rect.bottom = roof.rect.top + 63
                            interaction = True

                        for portal in portal_hit_list:
                            self.rect.y = 0
                            self.rect.x = portal.rect.x
                            self.current_x = portal.room_x
                            interaction = True

                        if interaction == True:
                            break
                
        # if attacking
        if self.attack_timer >= 0:
            self.attack()

        # movement and actions
        if self.upKeyPressed and self.can_move:
            self.DIRECTION = self.UP
            self.image = self.walk_up_animation[self.current_frame]

            for y in range(0, self.walk_rate):
                self.rect.y -= 1
                interaction = False

                wall_hit_list = pygame.sprite.groupcollide(player, self.walls, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
                portal_hit_list = pygame.sprite.groupcollide(self.portals, player, False, False,  collided=pygame.sprite.collide_rect_ratio(1))
            
                for wall in wall_hit_list:
                    self.rect.top = wall.rect.bottom - 63
                    interaction = True

                for portal in portal_hit_list:
                    self.rect.y = self.screen.get_height() - 68
                    self.rect.x = portal.rect.x
                    self.current_x = portal.room_x
                    interaction = True

                if interaction == True:
                    break

        if self.downKeyPressed and self.can_move:
            self.DIRECTION = self.DOWN
            self.image = self.walk_down_animation[self.current_frame]

            for y in range(0, self.walk_rate):
                self.rect.y += 1

                interaction = False

                roof_hit_list = pygame.sprite.groupcollide(player, self.roofs, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
                portal_hit_list = pygame.sprite.groupcollide(self.portals, player, False, False, collided=pygame.sprite.collide_rect_ratio(1))

                for roof in roof_hit_list:
                    self.rect.bottom = roof.rect.top + 63
                    interaction = True

                for portal in portal_hit_list:
                    self.rect.y = 0
                    self.rect.x = portal.rect.x
                    self.current_x = portal.room_x
                    interaction = True

                if interaction == True:
                    break

        if self.leftKeyPressed and self.can_move:
            self.DIRECTION = self.LEFT
            self.image = self.walk_left_animation[self.current_frame]
            
            for x in range(0, self.walk_rate):
                self.rect.x -= 1
                interaction = False

                roof_hit_list = pygame.sprite.groupcollide(player, self.roofs, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
                wall_hit_list = pygame.sprite.groupcollide(player, self.walls, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
                portal_hit_list = pygame.sprite.groupcollide(self.portals, player, False, False, collided=pygame.sprite.collide_rect_ratio(1))

                for wall in wall_hit_list:
                    self.rect.left = wall.rect.right - 63
                    interaction = True

                for roof in roof_hit_list:
                    self.rect.left = roof.rect.right - 63
                    interaction = True

                for portal in portal_hit_list:
                    self.rect.y = portal.rect.y
                    self.rect.x = self.screen.get_width() - 68
                    self.current_x = portal.room_x
                    interaction = True

                if interaction == True:
                    break

        if self.rightKeyPressed and self.can_move:
            self.DIRECTION = self.RIGHT
            self.image = self.walk_right_animation[self.current_frame]

            for x in range(0, self.walk_rate):
                self.rect.x += 1
                interaction = False

                roof_hit_list = pygame.sprite.groupcollide(player, self.roofs, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
                wall_hit_list = pygame.sprite.groupcollide(player, self.walls, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
                portal_hit_list = pygame.sprite.groupcollide(self.portals, player, False, False, collided=pygame.sprite.collide_rect_ratio(1))

                for wall in wall_hit_list:
                    self.rect.right = wall.rect.left + 63
                    interaction = True

                for roof in roof_hit_list:
                    self.rect.right = roof.rect.left + 63
                    interaction = True

                for portal in portal_hit_list:
                    self.rect.y = portal.rect.y
                    self.rect.x = 0
                    self.current_x = portal.room_x
                    interaction = True

                if interaction == True:
                    break

        if self.specialPressed and self.can_attack:
            if self.sp >= self.specialCost:
                self.ui.sp_bar.updateSpecial(self.specialCost, self.sp, self.MAX_SP)
                self.sp -= self.specialCost
                
        elif self.oneKeyPressed and self.can_attack and self.inventory.slots[0][1] != 'empty':
            if self.inventory.slots[0][0].item_name == 'health':
                if self.hp + 25 > self.MAX_HP:
                    self.ui.hp_bar.updateHealth(-(self.MAX_HP - self.hp), self.hp, self.MAX_HP)
                    self.hp = self.MAX_HP
                else:
                    self.ui.hp_bar.updateHealth(-25, self.hp, self.MAX_HP)
                    self.hp += 25
            elif self.inventory.slots[0][0].item_name == 'special':
                if self.sp + 25 > self.MAX_SP:
                    self.ui.sp_bar.updateSpecial(-(self.MAX_SP - self.sp), self.sp, self.MAX_SP)
                    self.sp = self.MAX_SP
                else:
                    self.ui.sp_bar.updateSpecial(-25, self.sp, self.MAX_SP)
                    self.sp += 25
            self.inventory.slots[0][1] = "empty"
            self.inventory.slots[0][0].kill()
                        

        elif self.twoKeyPressed and self.can_attack and self.inventory.slots[1][1] != 'empty':
            if self.inventory.slots[1][0].item_name == 'health':
                if self.hp + 25 > self.MAX_HP:
                    self.ui.hp_bar.updateHealth(-(self.MAX_HP - self.hp), self.hp, self.MAX_HP)
                    self.hp = self.MAX_HP
                else:
                    self.ui.hp_bar.updateHealth(-25, self.hp, self.MAX_HP)
                    self.hp += 25
            elif self.inventory.slots[1][0].item_name == 'special':
                if self.sp + 25 > self.MAX_SP:
                    self.ui.sp_bar.updateSpecial(-(self.MAX_SP - self.sp), self.sp, self.MAX_SP)
                    self.sp = self.MAX_SP
                else:
                    self.ui.sp_bar.updateSpecial(-25, self.sp, self.MAX_SP)
                    self.sp += 25
            self.inventory.slots[1][1] = "empty"
            self.inventory.slots[1][0].kill()


        if not self.rightKeyPressed and not self.leftKeyPressed and not self.upKeyPressed and not self.downKeyPressed and self.can_move:
            if self.DIRECTION == self.UP:
                self.image = self.walk_up_animation[0]
            if self.DIRECTION == self.DOWN:
                self.image = self.walk_down_animation[0]
            if self.DIRECTION == self.RIGHT:
                self.image = self.walk_right_animation[0]
            if self.DIRECTION == self.LEFT:
                self.image = self.walk_left_animation[0]
                
        if self.invuln_frames != 0:
            self.invuln_frames -= 1
            print 'invulnerable'

        # advance the current frame
        self.ticker += 1

        # mage walk animation is quicker than the rest
        if isinstance(self, Mage):
            if self.ticker % 4 == 0:
                self.current_frame = (self.current_frame + 1) % 4
                self.ticker = 0
        else:
            if self.ticker % 8 == 0:
                self.current_frame = (self.current_frame + 1) % 4
                self.ticker = 0

    def initiate_attack(self):
        self.can_move = False
        self.can_attack = False
        self.attack_timer = self.attack_length

    def remove_mob_with_id(self, mob_id):
        i = 0
        for mob in self.current_room.mobs:
            if mob.id == mob_id:
                del self.current_room.mobs[i]
            i = i + 1

    def read_buffer(self):
        if self.buffer != None:
            if self.buffer_type == KEYDOWN:

                if self.buffer == K_UP:
                    self.upKeyPressed = True
                    self.downKeyPressed = False
                if self.buffer == K_DOWN:
                    self.downKeyPressed = True
                    self.upKeyPressed = False
                if self.buffer == K_LEFT:
                    self.leftKeyPressed = True
                    self.rightKeyPressed = False
                if self.buffer == K_RIGHT:
                    self.rightKeyPressed = True
                    self.leftKeyPressed = False

                if self.buffer == K_SPACE:
                    self.spacePressed = True
                elif self.buffer == K_u:
                    self.specialPressed = True
                elif self.buffer == K_1 and self.inventory.slots[0][1] != 'empty':
                    self.oneKeyPressed = True
                elif self.buffer == K_2 and self.inventory.slots[1][1] != 'empty':
                    self.twoKeyPressed = True

            elif self.buffer_type == KEYUP:
                if self.buffer == K_UP:
                    self.upKeyPressed = False
                elif self.buffer == K_DOWN:
                    self.downKeyPressed = False
                elif self.buffer == K_LEFT:
                    self.leftKeyPressed = False
                elif self.buffer == K_RIGHT:
                    self.rightKeyPressed = False
                if self.buffer == K_SPACE:
                    self.spacePressed = False
                if self.buffer == K_u:
                    self.specialPressed = False
                if self.buffer == K_1:
                    self.oneKeyPressed = False
                if self.buffer == K_2:
                    self.twoKeyPressed = False

            self.buffer = None
            self.buffer_type = None        

class Paladin(Hero):
    def __init__(self, x, y, DIRECTION, screen):
        self.walk_right_animation = [PaladinR1, PaladinR2, PaladinR1, PaladinR3]
        self.attack_right_animation = [PaladinAttackR1, PaladinAttackR2, PaladinAttackR3]

        self.walk_left_animation = [PaladinL1, PaladinL2, PaladinL1, PaladinL3]
        self.attack_left_animation = [PaladinAttackL1, PaladinAttackL2, PaladinAttackL3]

        self.walk_down_animation = [PaladinD1, PaladinD2, PaladinD1, PaladinD3]
        self.attack_down_animation = [PaladinAttackD1, PaladinAttackD2, PaladinAttackD3]

        self.walk_up_animation = [PaladinU1, PaladinU2, PaladinU1, PaladinU3]
        self.attack_up_animation = [PaladinAttackU1, PaladinAttackU2, PaladinAttackU3]

        #instance of a attack_hit_box hit box that will be used to attack
        self.attack_hit_box = None
        self.specialCost = 10
        self.walk_rate = 8
        self.attack_length = 15
        self.attack_left_ratio = 0.7
        self.attack_up_ratio = 0.7
        self.damage = 34
        self.knockback = 80

        # hp vars
        self.hp = 2000
        self.MAX_HP = 2000

        # sp vars
        self.sp = 100
        self.MAX_SP = 100

        if DIRECTION == "UP":
            Hero.__init__(self, self.walk_up_animation[0], x, y, DIRECTION, screen)
        elif DIRECTION == "DOWN":
            Hero.__init__(self, self.walk_down_animation[0], x, y, DIRECTION, screen)
        elif DIRECTION == "LEFT":
            Hero.__init__(self, self.walk_left_animation[0], x, y, DIRECTION, screen)
        elif DIRECTION == "RIGHT":
            Hero.__init__(self, self.walk_right_animation[0], x, y, DIRECTION, screen)

    def attack(self):
        # perform attack animation
        if self.attack_timer > 0:
            # every 5 frames change the animation
            if self.attack_timer % 5 == 0:
                if self.DIRECTION == self.RIGHT:
                    # change animation to next frame
                    self.image = self.attack_right_animation[
                        len(self.attack_right_animation) - ((self.attack_timer) / 5)]

                    # damage enemies that are in range, if on attack frame
                    if len(self.attack_right_animation) - ((self.attack_timer) / 5) == 2:
                        self.attack_hit_box = AttackHitBox(PaladinR1, self.rect.x + 30, self.rect.y, self.damage)

                        attack_hit_box = pygame.sprite.GroupSingle(self.attack_hit_box)
                        mob_hit_list = pygame.sprite.groupcollide(self.mobs, attack_hit_box, False, False)

                        for mob in mob_hit_list:
                            mob.take_damage(self.attack_hit_box.damage, self)

                if self.DIRECTION == self.LEFT:
                    # change animation to next frame
                    self.image = self.attack_left_animation[len(self.attack_left_animation) - ((self.attack_timer) / 5)]

                    # damage enemies that are in range, if on attack frame
                    if len(self.attack_left_animation) - ((self.attack_timer) / 5) == 2:
                        self.rect.x -= 19

                        self.attack_hit_box = AttackHitBox(PaladinR1, self.rect.x - 30, self.rect.y, self.damage)

                        attack_hit_box = pygame.sprite.GroupSingle(self.attack_hit_box)
                        mob_hit_list = pygame.sprite.groupcollide(self.mobs, attack_hit_box, False, False)

                        for mob in mob_hit_list:
                            mob.take_damage(self.attack_hit_box.damage, self)

                if self.DIRECTION == self.UP:

                    # change animation to next frame
                    self.image = self.attack_up_animation[len(self.attack_up_animation) - ((self.attack_timer) / 5)]

                    # damage enemies that are in range, if on attack frame
                    if len(self.attack_up_animation) - ((self.attack_timer) / 5) == 2:
                        self.rect.y -= 19

                        self.attack_hit_box = AttackHitBox(PaladinR1, self.rect.x, self.rect.y - 30, self.damage)

                        attack_hit_box = pygame.sprite.GroupSingle(self.attack_hit_box)
                        mob_hit_list = pygame.sprite.groupcollide(self.mobs, attack_hit_box, False, False)

                        for mob in mob_hit_list:
                            mob.take_damage(self.attack_hit_box.damage, self)

                if self.DIRECTION == self.DOWN:
                    # change animation to next frame
                    self.image = self.attack_down_animation[len(self.attack_down_animation) - ((self.attack_timer) / 5)]
                    # damage enemies that are in range, if on attack frame
                    if len(self.attack_down_animation) - ((self.attack_timer) / 5) == 2:
                        self.attack_hit_box = AttackHitBox(PaladinR1, self.rect.x, self.rect.y + 30, self.damage)

                        attack_hit_box = pygame.sprite.GroupSingle(self.attack_hit_box)
                        mob_hit_list = pygame.sprite.groupcollide(self.mobs, attack_hit_box, False, False)

                        for mob in mob_hit_list:
                            mob.take_damage(self.attack_hit_box.damage, self)

            self.attack_timer -= 1
        # attack finished; put back to standing position
        elif self.attack_timer == 0:
            if self.DIRECTION == self.RIGHT:
                self.image = self.walk_right_animation[0]
            if self.DIRECTION == self.LEFT:
                self.image = self.walk_left_animation[0]
                self.rect.x += 19
            if self.DIRECTION == self.UP:
                self.image = self.walk_up_animation[0]
                self.rect.y += 19
            if self.DIRECTION == self.DOWN:
                self.image = self.walk_down_animation[0]

            self.read_buffer()

            self.can_move = True
            self.can_attack = True
            self.attack_timer = -1
            self.attack_hit_box = None

class Mage(Hero):
    def __init__(self, x, y, DIRECTION, screen):
        self.walk_right_animation = [MageR1, MageR2, MageR1, MageR2]
        self.attack_right_animation = [MageAttackR1, MageAttackR2, MageAttackR3]

        self.walk_left_animation = [MageL1, MageL2, MageL1, MageL2]
        self.attack_left_animation = [MageAttackL1, MageAttackL2, MageAttackL3]

        self.walk_up_animation = [MageU1, MageU2, MageU1, MageU2]
        self.attack_up_animation = [MageAttackU1, MageAttackU2, MageAttackU3]
        
        self.walk_down_animation = [MageD1, MageD2, MageD1, MageD2]
        self.attack_down_animation = [MageAttackD1, MageAttackD2, MageAttackD3]

        self.specialCost = 10
        self.walk_rate = 5

        self.attack_length = 6
        self.attack_frame = -1
        #self.damage = 17
        self.knockback = 2
        self.attack_up_ratio = 1.0
        self.attack_left_ratio = 1.0

        # hp vars
        self.hp = 60
        self.MAX_HP = 60

        # sp vars
        self.sp = 200
        self.MAX_SP = 200
        
        if DIRECTION == "UP":
            Hero.__init__(self, self.walk_up_animation[0], x, y, DIRECTION, screen)
        elif DIRECTION == "DOWN":
            Hero.__init__(self, self.walk_down_animation[0], x, y, DIRECTION, screen)
        elif DIRECTION == "LEFT":
            Hero.__init__(self, self.walk_left_animation[0], x, y, DIRECTION, screen)
        elif DIRECTION == "RIGHT":
            Hero.__init__(self, self.walk_right_animation[0], x, y, DIRECTION, screen)

    def attack(self):
        # perform attack animation
        if self.attack_timer > 0:
            # every 5 frames change the animation
            if self.attack_timer % 2 == 0:
                self.attack_frame = len(self.attack_right_animation) - ((self.attack_timer) / 2)

                if self.DIRECTION == self.RIGHT:
                    # change animation to next frame
                    self.image = self.attack_right_animation[self.attack_frame]
                    
                if self.DIRECTION == self.LEFT:
                    # change animation to next frame
                    self.image = self.attack_left_animation[self.attack_frame]

                if self.DIRECTION == self.UP:
                    # change animation to next frame
                    self.image = self.attack_up_animation[self.attack_frame]
                    if self.attack_frame == 2:
                        self.rect.x -= 7

                if self.DIRECTION == self.DOWN:
                    # change animation to next frame
                    self.image = self.attack_down_animation[self.attack_frame]

                if self.attack_frame == 2:
                    self.projectiles.add(Bolt(self.rect.x, self.rect.y, self.DIRECTION, self.walls, self.roofs, self.mobs, self))

            self.attack_timer -= 1
        # attack finished; put back to standing position
        elif self.attack_timer == 0:
            if self.DIRECTION == self.RIGHT:
                self.image = self.walk_right_animation[0]
            if self.DIRECTION == self.LEFT:
                self.image = self.walk_left_animation[0]
            if self.DIRECTION == self.UP:
                self.rect.x += 7
                self.image = self.walk_up_animation[0]
            if self.DIRECTION == self.DOWN:
                self.image = self.walk_down_animation[0]

            self.read_buffer()

            self.can_move = True
            self.can_attack = True
            self.attack_timer = -1
            self.attack_frame = -1
        

class Alien(Hero):
    pass

class Assassin(Hero):
    def __init__(self, x, y, DIRECTION, screen):
        self.walk_right_animation = [AssassinR1, AssassinR2, AssassinR3, AssassinR4]
        self.attack_right_animation = [AssassinAttackR1, AssassinAttackR2, AssassinAttackR3]

        self.walk_left_animation = [AssassinL1, AssassinL2, AssassinL3, AssassinL4]
        self.attack_left_animation = [AssassinAttackL1, AssassinAttackL2, AssassinAttackL3]

        self.walk_down_animation = [AssassinD1, AssassinD2, AssassinD3, AssassinD4]
        self.attack_down_animation = [AssassinAttackD1, AssassinAttackD2, AssassinAttackD3]

        self.walk_up_animation = [AssassinU1, AssassinU2, AssassinU3, AssassinU4]
        self.attack_up_animation = [AssassinAttackU1, AssassinAttackU2, AssassinAttackU3]

        #instance of a attack_hit_box hit box that will be used to attack
        self.attack_hit_box = None
        self.specialCost = 10
        self.walk_rate = 10

        self.attack_length = 9
        self.attack_left_ratio = 0.02
        self.attack_up_ratio = 0.1
        self.attack_frame = -1
        self.damage = 9
        self.knockback = 6

        # hp vars
        self.hp = 100
        self.MAX_HP = 100

        # sp vars
        self.sp = 150
        self.MAX_SP = 150

        if DIRECTION == "UP":
            Hero.__init__(self, self.walk_up_animation[0], x, y, DIRECTION, screen)
        elif DIRECTION == "DOWN":
            Hero.__init__(self, self.walk_down_animation[0], x, y, DIRECTION, screen)
        elif DIRECTION == "LEFT":
            Hero.__init__(self, self.walk_left_animation[0], x, y, DIRECTION, screen)
        elif DIRECTION == "RIGHT":
            Hero.__init__(self, self.walk_right_animation[0], x, y, DIRECTION, screen)

    def attack(self):
        # perform attack animation
        if self.attack_timer > 0:
            # every 5 frames change the animation
            if self.attack_timer % 3 == 0:
                self.attack_frame = len(self.attack_right_animation) - ((self.attack_timer) / 3)

                if self.DIRECTION == self.RIGHT:
                    # change animation to next frame
                    self.image = self.attack_right_animation[self.attack_frame]

                    # damage enemies that are in range, if on attack frame
                    if self.attack_frame == 0:
                        self.attack_hit_box = AttackHitBox(AssassinHitBoxH, self.rect.x, self.rect.y, self.damage)
                    else:
                        self.attack_hit_box = AttackHitBox(AssassinHitBoxH, self.rect.x + 35, self.rect.y, self.damage)


                    attack_hit_box = pygame.sprite.GroupSingle(self.attack_hit_box)
                    mob_hit_list = pygame.sprite.groupcollide(self.mobs, attack_hit_box, False, False)

                    for mob in mob_hit_list:
                        mob.take_damage(self.attack_hit_box.damage, self)
                        print self.attack_frame

                    self.attack_hit_box = None

                if self.DIRECTION == self.LEFT:

                    # change animation to next frame
                    self.image = self.attack_left_animation[self.attack_frame]

                    # damage enemies that are in range, if on attack frame
                    if self.attack_frame == 0:
                        self.rect.x -= 30
                    elif self.attack_frame == 1:
                        self.rect.x -= 48

                    self.attack_hit_box = AttackHitBox(AssassinHitBoxH, self.rect.x + 10, self.rect.y, self.damage)

                    attack_hit_box = pygame.sprite.GroupSingle(self.attack_hit_box)
                    mob_hit_list = pygame.sprite.groupcollide(self.mobs, attack_hit_box, False, False)

                    for mob in mob_hit_list:
                        mob.take_damage(self.attack_hit_box.damage, self)

                    self.attack_hit_box = None

                if self.DIRECTION == self.UP:

                    # change animation to next frame
                    self.image = self.attack_up_animation[self.attack_frame]

                    # damage enemies that are in range, if on attack frame
                    if self.attack_frame == 0:
                        self.rect.y -= 33
                    if self.attack_frame == 1:
                        self.rect.y -= 48

                    self.attack_hit_box = AttackHitBox(AssassinHitBoxV, self.rect.x, self.rect.y, self.damage)

                    attack_hit_box = pygame.sprite.GroupSingle(self.attack_hit_box)
                    mob_hit_list = pygame.sprite.groupcollide(self.mobs, attack_hit_box, False, False)

                    for mob in mob_hit_list:
                        mob.take_damage(self.attack_hit_box.damage, self)

                    self.attack_hit_box = None


                if self.DIRECTION == self.DOWN:

                    # change animation to next frame
                    self.image = self.attack_down_animation[self.attack_frame]

                    # damage enemies that are in range, if on attack frame
                    if self.attack_frame == 0:
                        self.attack_hit_box = AttackHitBox(AssassinHitBoxV, self.rect.x, self.rect.y, self.damage)
                    else:
                         self.attack_hit_box = AttackHitBox(AssassinHitBoxV, self.rect.x, self.rect.y + 40, self.damage)                       

                    attack_hit_box = pygame.sprite.GroupSingle(self.attack_hit_box)
                    mob_hit_list = pygame.sprite.groupcollide(self.mobs, attack_hit_box, False, False)

                    for mob in mob_hit_list:
                        mob.take_damage(self.attack_hit_box.damage, self)
                        print self.attack_frame

                    self.attack_hit_box = None

            self.attack_timer -= 1
        # attack finished; put back to standing position
        elif self.attack_timer == 0:
            if self.DIRECTION == self.RIGHT:
                self.image = self.walk_right_animation[0]
            if self.DIRECTION == self.LEFT:
                self.image = self.walk_left_animation[0]
                self.rect.x += 78
            if self.DIRECTION == self.UP:
                self.image = self.walk_up_animation[0]
                self.rect.y += 81
            if self.DIRECTION == self.DOWN:
                self.image = self.walk_down_animation[0]

            self.read_buffer()

            self.can_move = True
            self.can_attack = True
            self.attack_timer = -1
            self.attack_frame = -1


class AttackHitBox(Sprite):
    def __init__(self, image, x, y, damage):
        Sprite.__init__(self, image, x, y)
        self.damage = damage
