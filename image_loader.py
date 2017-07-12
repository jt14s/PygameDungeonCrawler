import pygame

#######################################################################################################
#Pink character images ################################################################################
#######################################################################################################

#walk images
PinkR1 = pygame.image.load('images/pink/walk/right/right1.png')
PinkR2 = pygame.image.load('images/pink/walk/right/right2.png')
PinkR3 = pygame.image.load('images/pink/walk/right/right3.png')

PinkL1 = pygame.image.load('images/pink/walk/left/left1.png')
PinkL2 = pygame.image.load('images/pink/walk/left/left2.png')
PinkL3 = pygame.image.load('images/pink/walk/left/left3.png')

PinkU1 = pygame.image.load('images/pink/walk/up/up1.png')
PinkU2 = pygame.image.load('images/pink/walk/up/up2.png')
PinkU3 = pygame.image.load('images/pink/walk/up/up3.png')
        
PinkD1 = pygame.image.load('images/pink/walk/down/down1.png')
PinkD2 = pygame.image.load('images/pink/walk/down/down2.png')
PinkD3 = pygame.image.load('images/pink/walk/down/down3.png')

#attack images
PinkAttackR1 = pygame.image.load('images/pink/attack/right/attack1.png')
PinkAttackR2 = pygame.image.load('images/pink/attack/right/attack2.png')
PinkAttackR3 = pygame.image.load('images/pink/attack/right/attack3.png')

PinkAttackL1 = pygame.image.load('images/pink/attack/left/attack1.png')
PinkAttackL2 = pygame.image.load('images/pink/attack/left/attack2.png')
PinkAttackL3 = pygame.image.load('images/pink/attack/left/attack3.png')

PinkAttackU1 = pygame.image.load('images/pink/attack/up/attack1.png')
PinkAttackU2 = pygame.image.load('images/pink/attack/up/attack2.png')
PinkAttackU3 = pygame.image.load('images/pink/attack/up/attack3.png')

PinkAttackD1 = pygame.image.load('images/pink/attack/down/attack1.png')
PinkAttackD2 = pygame.image.load('images/pink/attack/down/attack2.png')
PinkAttackD3 = pygame.image.load('images/pink/attack/down/attack3.png')

#######################################################################################################
#Map Images ###########################################################################################
#######################################################################################################

#wall images
WallImg = pygame.image.load('images/level1/wallbrickpattern.png')

#floor images
FloorImgCenter = pygame.image.load('images/level1/floors/floortile/floortile1.png')
FloorImgTop = pygame.image.load('images/level1/floors/floortile/floortile2.png')
FloorImgRight = pygame.image.load('images/level1/floors/floortile/floortile3.png')
FloorImgLeft = pygame.image.load('images/level1/floors/floortile/floortile5.png')
FloorImgTopRight = pygame.image.load('images/level1/floors/floortile/floortile6.png')
FloorImgTopLeft = pygame.image.load('images/level1/floors/floortile/floortile9.png')
FloorImgVerticalTunnel = pygame.image.load('images/level1/floors/floortile/floortile11.png')
FloorImgTopDeadEnd = pygame.image.load('images/level1/floors/floortile/floortile12.png')

#roof images
RoofImgCenter = pygame.image.load('images/level1/rooftile/roof1.png')
RoofImgCenterCenter = pygame.image.load('images/level1/rooftile/roof12.png')

#torch images
TorchImg1 = pygame.image.load('images/level1/wall_torch/walltorch1.png')
TorchImg2 = pygame.image.load('images/level1/wall_torch/walltorch2.png')
TorchImg3 = pygame.image.load('images/level1/wall_torch/walltorch3.png')
TorchImg4 = pygame.image.load('images/level1/wall_torch/walltorch2.png')
TorchImg5 = pygame.image.load('images/level1/wall_torch/walltorch1.png')
TorchImg6 = pygame.image.load('images/level1/wall_torch/walltorch4.png')
TorchImg7 = pygame.image.load('images/level1/wall_torch/walltorch5.png')
TorchImg8 = pygame.image.load('images/level1/wall_torch/walltorch4.png')

#######################################################################################################
#Item Images ##########################################################################################
#######################################################################################################

#items
RopeImg = pygame.image.load('images/items/rope/rope.png')
ThrownRopeDown = pygame.image.load('images/items/rope/throwndown1.png')
BowImg = pygame.image.load('images/items/bow/bow.png')

#######################################################################################################
#HUD Images ###########################################################################################
#######################################################################################################
InvImg = pygame.image.load('images/inventory.png')
UiImg = pygame.image.load('images/hud.png')
HealthBar = pygame.image.load('images/healthbar.png')
SpecialBar = pygame.image.load('images/specialbar.png')

#######################################################################################################
#Enemy Images #########################################################################################
#######################################################################################################

#shrimp walk images
ShrimpWalkU1 = pygame.image.load('images/mobs/shrimp/walk/up/walk1.png')
ShrimpWalkU2 = pygame.image.load('images/mobs/shrimp/walk/up/walk2.png')

ShrimpWalkD1 = pygame.image.load('images/mobs/shrimp/walk/down/walk1.png')
ShrimpWalkD2 = pygame.image.load('images/mobs/shrimp/walk/down/walk2.png')

ShrimpWalkL1 = pygame.image.load('images/mobs/shrimp/walk/left/walk1.png')
ShrimpWalkL2 = pygame.image.load('images/mobs/shrimp/walk/left/walk2.png')

ShrimpWalkR1 = pygame.image.load('images/mobs/shrimp/walk/right/walk1.png')
ShrimpWalkR2 = pygame.image.load('images/mobs/shrimp/walk/right/walk2.png')

#shrimp attack images
ShrimpAttackU1 = pygame.image.load('images/mobs/shrimp/attack/up/attack1.png')
ShrimpAttackU2 = pygame.image.load('images/mobs/shrimp/attack/up/attack2.png')
ShrimpAttackU3 = pygame.image.load('images/mobs/shrimp/attack/up/attack3.png')

ShrimpAttackD1 = pygame.image.load('images/mobs/shrimp/attack/down/attack1.png')
ShrimpAttackD2 = pygame.image.load('images/mobs/shrimp/attack/down/attack2.png')
ShrimpAttackD3 = pygame.image.load('images/mobs/shrimp/attack/down/attack3.png')

ShrimpAttackL1 = pygame.image.load('images/mobs/shrimp/attack/left/attack1.png')
ShrimpAttackL2 = pygame.image.load('images/mobs/shrimp/attack/left/attack2.png')
ShrimpAttackL3 = pygame.image.load('images/mobs/shrimp/attack/left/attack3.png')

ShrimpAttackR1 = pygame.image.load('images/mobs/shrimp/attack/right/attack1.png')
ShrimpAttackR2 = pygame.image.load('images/mobs/shrimp/attack/right/attack2.png')
ShrimpAttackR3 = pygame.image.load('images/mobs/shrimp/attack/right/attack3.png')
