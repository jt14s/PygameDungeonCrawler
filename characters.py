import pygame
from image_loader import *
from hud import *

class Hero(pygame.sprite.Sprite):

    #all characters will share these attrivutes
    walls = None
    floors = None
    roofs = None
    mobs = None
    items = None
    keys = None
        
    def __init__(self, x, y,DIRECTION, screen):
        #init self as a srpite object
        pygame.sprite.Sprite.__init__(self)

        #images and animation lists
        self.image = PinkD1

        self.walk_right_animation = [PinkR1,PinkR2, PinkR1, PinkR3]
        self.attack_right_animation = [PinkAttackR1, PinkAttackR2, PinkAttackR3]
        
        self.walk_left_animation = [PinkL1, PinkL2, PinkL1, PinkL3]
        self.walk_down_animation = [PinkD1, PinkD2, PinkD1, PinkD3]
        self.walk_up_animation = [PinkU1, PinkU2, PinkU1, PinkU3]

        #character hitbox
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #frame info
        self.ticker = 0
        self.current_frame = 0
        
        #inv and ui
        self.ui = UI((screen.get_width()/6)+10, 10, 100, 100, screen)
        self.inventory = Inventory(InvImg, (screen.get_width()/2)-70, (screen.get_height()/1.1))

        self.item_slot_group = pygame.sprite.Group()

        #key variables
        self.DIRECTION = DIRECTION
        self.upKeyPressed = False
        self.downKeyPressed = False
        self.leftKeyPressed = False
        self.rightKeyPressed = False
        self.spacePressed = False

        self.onePressed = False
        self.twoPressed = False

        #misc
        self.RIGHT, self.LEFT, self.UP, self.DOWN = "right left up down".split()
        self.action = 'walking'
        self.can_move = True
        self.walk_rate = 5
        self.invuln_frames = 0

        #hp vars
        self.hp = 100
        self.MAX_HP = 100
        self.MIN_HP = 0

        #sp vars
        self.sp = 100
        self.MAX_SP = 100
        self.MIN_SP = 0
    
    def update(self):
        #instance of the player in a group to check against collisions
        player = pygame.sprite.GroupSingle(self)

        mob_hit_list = pygame.sprite.groupcollide(self.mobs, player, False, False)
        item_hit_list = pygame.sprite.groupcollide(self.items, player, True, False)

        for item in item_hit_list:
            print('picked up item')

            for slot in self.inventory.slots:
                if slot[1] == 'empty':
                    #update slot info and then add to be drawn to screen
                    slot[0].addToInventory(item.name, item.image, self.inventory.rect.x + 21 + ( slot[0].index * 60), self.inventory.rect.y + 23)
                    slot[1] = 'used'
                    self.item_slot_group.add(slot[0])
                    break
                    
        for mob in mob_hit_list:
            if self.invuln_frames == 0:
                print('hit mob')
                self.ui.hp_bar.updateHealth(mob.damage, self.hp, self.MAX_HP)
                self.ui.sp_bar.updateSpecial(mob.damage, self.sp, self.MAX_SP)

                self.sp -= mob.damage
                self.hp -= mob.damage
                if self.hp <= self.MIN_HP:
                    print 'ded'

                self.invuln_frames = 20
                    
        if self.downKeyPressed and self.can_move:
            self.rect.y += self.walk_rate
            self.image = self.walk_down_animation[self.current_frame]

            #this is how you calculate collisions between two sprite groups, then all collided are stored in list
            roof_hit_list = pygame.sprite.groupcollide(player, self.roofs, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
 
            #check trhough all calculated collisions
            for roof in roof_hit_list:
                self.rect.bottom = roof.rect.top + 63
                    
                    
        elif self.upKeyPressed and self.can_move:
            self.rect.y -= self.walk_rate
            self.image = self.walk_up_animation[self.current_frame]

            wall_hit_list = pygame.sprite.groupcollide(player, self.walls, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))

            for wall in wall_hit_list:
                self.rect.top = wall.rect.bottom - 63

            
        elif self.leftKeyPressed and self.can_move:
            self.rect.x -= self.walk_rate
            self.image = self.walk_left_animation[self.current_frame]

            roof_hit_list = pygame.sprite.groupcollide(player, self.roofs, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
            wall_hit_list = pygame.sprite.groupcollide(player, self.walls, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))

            for wall in wall_hit_list:
                self.rect.left = wall.rect.right - 63

            for roof in roof_hit_list:
                self.rect.left = roof.rect.right - 63
                
        elif self.rightKeyPressed and self.can_move:
            self.rect.x += self.walk_rate
            self.image = self.walk_right_animation[self.current_frame]

            roof_hit_list = pygame.sprite.groupcollide(player, self.roofs, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))
            wall_hit_list = pygame.sprite.groupcollide(player, self.walls, False, False, collided=pygame.sprite.collide_rect_ratio(0.52))

            for wall in wall_hit_list:
                self.rect.right = wall.rect.left + 63

            for roof in roof_hit_list:
                self.rect.right = roof.rect.left + 63

        if self.invuln_frames != 0:
            self.invuln_frames -= 1
            print 'invulnerable'

        #advance the current frame based on FPS
        self.ticker += 1
        if self.ticker % 8 == 0:
            self.current_frame = (self.current_frame + 1) % 4
            self.ticker = 0
