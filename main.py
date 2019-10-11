#!/usr/bin/env python3

import pygame
import sys
import os
import glob
import re

""" Setup """

mainFile = os.path.realpath(__file__)
mainDir = os.path.dirname(mainFile)
imagesDir = os.path.join(mainDir, 'images')


#Settle screen coordinates
screenSize = (960, 960)
world = pygame.display.set_mode(screenSize)

#settle framerate and start clock
fps = 60

directions = ('left', 'right', 'down', 'up')
gravity = 2

clock = pygame.time.Clock()
lastTick = 0

#start pygame and enable mainloop
pygame.init()
main = True

#load and scale background
backdrop = pygame.image.load(os.path.join(imagesDir, 'stage.png'))
backdrop = pygame.transform.scale(backdrop, screenSize)
backdropbox = world.get_rect()

#set the keybinds:
keybinds = {}
keybinds['left'] = [pygame.K_LEFT, ord('a')]
keybinds['right'] = [pygame.K_RIGHT, ord('d')]
keybinds['up'] = [pygame.K_SPACE, pygame.K_UP, ord('w')]
keybinds['down'] = [pygame.K_DOWN, ord('s')]
keybinds['close'] = [pygame.K_ESCAPE, ord('q')]

#check for collision between 2 objects
def checkCollision(a, b):
    if (a.coordinates[0] + a.size[0] >= b.coordinates[0] and \
        a.coordinates[0] <= b.coordinates[0] + b.size[0] and \
        a.coordinates[1] + a.size[1] >= b.coordinates[1] and \
        a.coordinates[1] <= b.coordinates[1] + b.size[1]):

        return(True)

#check on which site of an object collision occurs (if collision occurs),
def collisionSiteCheck(a, b):
    x = (abs(a.coordinates[0] - (b.coordinates[0] + b.size[0])),
         abs((a.coordinates[0] + a.size[0]) - b.coordinates[0]),
         abs((a.coordinates[1] + a.size[1]) - b.coordinates[1]),
         abs(a.coordinates[1] - (b.coordinates[1] + b.size[1])))

    return(directions[x.index(min(x))])

def getImages(relativePath, scalingFactor):
    images = glob.glob(os.path.join(imagesDir, relativePath))
    images = sorted(images, key=lambda f: int(re.findall("\((\d+)\)\.png", f)[0]))
    imageSet = []
    for image in images:
        img = pygame.image.load(image)
        img = pygame.transform.scale(img, (int(img.get_size()[0] * scalingFactor), \
                int(img.get_size()[1] * scalingFactor)))
        imageSet.append(img)
    return(imageSet)

#create player
#TODO rename spawnPlayer to player
class spawnPlayer(pygame.sprite.Sprite):
    def __init__(self, screenSize):
        pygame.sprite.Sprite.__init__(self)

        #settle color (RGB[a])
        self.color = (255, 255, 255)
        #load images
        self.imagesDir = os.path.join(imagesDir, 'player')
        self.images = {}
        self.scalingFactor = 0.13

        self.walkingImages = getImages('player/walking/*.png', self.scalingFactor)
        self.walkingFrames = len(self.walkingImages)
        self.currentWalkingFrame = 0

        self.idleImages = getImages('player/idle/*.png', self.scalingFactor)
        self.idleFrames = len(self.idleImages)
        self.currentIdleFrame = 0

        self.jumpingImages = getImages('player/jumping/*.png', self.scalingFactor)
        self.jumpingFrames = len(self.jumpingImages)
        self.currentJumpingFrame = 0

        self.image = self.idleImages[0]
        self.size = self.idleImages[0].get_size()

        #TODO move to dev class as object bounderies visualisation
        self.testImage = pygame.Surface(self.size)
        self.testImage.fill((0, 0, 0))
        self.rect = self.image.get_rect()

        #set coordinates of the player
        self.coordinates = [screenSize[0] / 2 - self.size[0] / 2,
                            screenSize[1] / 2 - self.size[1] / 2]

        self.rect = self.image.get_rect(topleft = tuple(self.coordinates))
        # self.rect = self.walkingImage.get_rect(topleft=tuple(self.coordinates))

        #settle player speed based on player width
        self.speed = 1
        self.speed = self.size[0] / 10 * self.speed

        #Set jumping and falling settings
        self.jumping = False
        self.isFalling = True
        self.standardForce = 7
        self.force = self.standardForce
        self.mass = 2

        #settle possible movements
        self.possibleMovements = ['left', 'right', 'down', 'up']

    def handleKeys(self, keybinds):
        #check for pressed keys
        keys = pygame.key.get_pressed()
        walking = False

        #TODO if left and right both are pressed, stop walking
        for k in keybinds['left']:
            if keys[k]:
                self.coordinates[0] -= self.speed
                walking = True

        for k in keybinds['right']:
            if keys[k]:
                self.coordinates[0] += self.speed
                walking = True

        for k in keybinds['up']:
            if keys[k]:
                self.jumping = True

        if self.jumping:
            if self.force >= 0:
                F = (0.5 * self.mass * self.force ** 2)
                self.coordinates[1] -= F
                self.force -= 1

            else:
                self.jumping = False

        else:
            self.currentJumpingFrame = 0

        if walking:
            if self.jumping:
                if self.currentJumpingFrame + 1 < self.jumpingFrames:
                    self.currentJumpingFrame += 1

                self.image = self.jumpingImages[self.currentJumpingFrame]

            else:
                if self.currentWalkingFrame + 1 >= self.walkingFrames:
                    self.currentWalkingFrame = 0

                else:
                    self.currentWalkingFrame += 1

                self.image = self.walkingImages[self.currentWalkingFrame]

        else:
            if self.currentIdleFrame + 1 >= self.idleFrames:
                self.currentIdleFrame = 0

            else:
                self.currentIdleFrame += 1

            self.image = self.idleImages[self.currentIdleFrame]

class spawnFloor(pygame.sprite.Sprite):
    def __init__(self, size, coordinates, screenSize):
        pygame.sprite.Sprite.__init__(self)

        self.size = size
        self.coordinates = coordinates

        self.color = (255, 0, 0)

        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft = self.coordinates)

#set basefloor
baseSize = 10
base = screenSize[1] - baseSize

#spawn floors
floors = pygame.sprite.Group()
floors.add(spawnFloor((screenSize[0], baseSize), (0, base), screenSize))
floors.add(spawnFloor((100, 10), (100, screenSize[1] - 100), screenSize))
floors.add(spawnFloor((200, 10), (500, screenSize[1] - 100), screenSize))

#spawn a player
player = spawnPlayer(screenSize)
players = pygame.sprite.Group()
players.add(player)

#development tools
class dev():
    def __init__(self):
        pass

    def collision(self, a, b, side):
        a.coordinates = [int(a.coordinates[0]), int(a.coordinates[1])]
        a.size = [int(a.size[0]), int(a.size[1])]
        b.coordinates = [int(b.coordinates[0]), int(b.coordinates[1])]
        b.size = [int(b.size[0]), int(b.size[1])]
        print('**************************')
        if side == 'left':
            print(side, ' | ', a.coordinates[0], ' | ',  b.coordinates[0] + b.size[0], ' | ', \
                    abs(a.coordinates[0] - (b.coordinates[0] + b.size[0])))

        elif side == 'right':
            print(side, ' | ', a.coordinates[0] + a.size[0], ' | ',  b.coordinates[0], ' | ', \
                    abs(a.coordinates[0] + a.size[0] - b.coordinates[0]))

        elif side == 'down':
            print(side, ' | ', a.coordinates[1] + a.size[1], ' | ',  b.coordinates[1], ' | ', \
                    abs(a.coordinates[1] + a.size[1] - b.coordinates[1]))

        elif side == 'up':
            print(side, ' | ', a.coordinates[1], ' | ',  b.coordinates[1] + b.size[1], ' | ', \
                    abs(a.coordinates[1] - (b.coordinates[1] + b.size[1])))
        else:
            print('none', ' | ', 000, ' | ', 000, '|', 000)

tests = dev()

""" Main loop """
while main:
    tick = pygame.time.get_ticks()
    dt = tick - lastTick

    #check events
    for event in pygame.event.get():

        #check if screen is closed
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            main = False

        #check if player quits the game using keys
        if event.type == pygame.KEYDOWN:
            for k in keybinds['close']:
                if event.key == k:
                    pygame.quit()
                    sys.exit()
                    main = False

    #draw background on screen
    world.blit(backdrop, backdropbox)

    #draw floors on screen
    #TODO change floors to objects and add floor into objects
    for f in floors:
        world.blit(f.image, f.coordinates)

    for p in players:
        onFloor = False

        #check if the player is on the floor
        for i, f in enumerate(floors):
            collision = checkCollision(p, f)
            collisionSite = collisionSiteCheck(p, f)

            if collision:
                #player cannot move towards the collision site anymore and stops jumping
                p.jumping = False

                #when collision occurs, make sure the player does not get in the object
                if collisionSite == 'down':
                    onFloor = True
                    p.coordinates[1] = f.coordinates[1] - p.size[1]

                elif collisionSite == 'up':
                    p.coordinates[1] = f.coordinates[1] + f.size[1] + 1

                elif collisionSite == 'left':
                    p.coordinates[0] = f.coordinates[0] + f.size[0] + 1

                elif collisionSite == 'right':
                    p.coordinates[0] = f.coordinates[0] - p.size[0] - 1

                #force is resetted whem player is on the floor
                if onFloor == True:
                    p.force = p.standardForce

        #make sure player does not get below the base floor
        if p.coordinates[1] > base:
            p.coordinates[1] = base - p.size[1]
            p.jumping = False
            onFloor = True
            p.force = p.standardForce

        #player falls when not on floor and not jumping
        if onFloor == False and p.jumping == False:
            if p.force > 0:
                p.force = -1
            else:
                F = -(0.5 * p.mass * p.force ** 2)
                p.coordinates[1] -= F
                p.force -= 1

        #draw player on the screen
        world.blit(p.image, p.coordinates)


        #handle playermovement
        p.handleKeys(keybinds)


    pygame.display.flip()
    lastTick = tick
    clock.tick(fps)

