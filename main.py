#!/usr/bin/env python3

import pygame
import sys
import os

""" Setup """


#Settle screen coordinates
screenSize = (960, 960)
world = pygame.display.set_mode(screenSize)

#settle framerate and start clock
fps = 60

gravity = 2

clock = pygame.time.Clock()
lastTick = 0

#start pygame and enable mainloop
pygame.init()
main = True

#load and scale background
backdrop = pygame.image.load(os.path.join('images', 'stage.png'))
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
    if (a.coordinates[0] + a.size[0] >= b.coordinates[0] and
        a.coordinates[0] <= b.coordinates[0] + b.size[0] and
        a.coordinates[1] + a.size[1] >= b.coordinates[1] and
        a.coordinates[1] <= b.coordinates[1] + b.size[1]):
        return(True)

#check on which site of an object collision occurs (if collision occurs),
def collisionSiteCheck(a, b):
    distanceOfCollision = {
        'left': abs(a.coordinates[0] - (b.coordinates[0] + b.size[0])),
        'right': abs((a.coordinates[0] + a.size[0]) - b.coordinates[0]),
        'down': abs((a.coordinates[1] + a.size[1]) - b.coordinates[1]),
        'up': abs(a.coordinates[1] - (b.coordinates[1] + b.size[1]))
    }
    return(min(distanceOfCollision, key=distanceOfCollision.get))

#create player
class spawnPlayer(pygame.sprite.Sprite):
    def __init__(self, screenSize):
        pygame.sprite.Sprite.__init__(self)

        #settle color (RGB[a])
        self.color = (255, 255, 255)

        self.size = (50, 50)

        #set coordinates of the player
        self.coordinates = [screenSize[0] / 2 - self.size[0] / 2,
                            screenSize[1] / 2 - self.size[1] / 2]

        #create image
        self.image = pygame.Surface(self.size)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft = tuple(self.coordinates))

        #settle player speed based on player width
        self.speed = 2.5
        self.speed = self.size[0] / 10 * self.speed

        self.isJumping = False
        self.isFalling = True
        self.standardForce = 7
        self.force = self.standardForce
        self.mass = 2

        #settle possible movements
        self.possibleMovements = ['left', 'right', 'down', 'up']

    def handleKeys(self, keybinds):
        #check for pressed keys
        keys = pygame.key.get_pressed()

        if 'left' in self.possibleMovements:
            for k in keybinds['left']:
                if keys[k]:
                    self.coordinates[0] -= self.speed

        if 'right' in self.possibleMovements:
            for k in keybinds['right']:
                if keys[k]:
                    self.coordinates[0] += self.speed

        if 'up' in self.possibleMovements:
            for k in keybinds['up']:
                if keys[k]:
                    self.isJumping = True

        if self.isJumping == True:
            if self.force > 0:
                F = (0.5 * self.mass * self.force ** 2)

            else:
                F = -(0.5 * self.mass * self.force ** 2)

            self.coordinates[1] -= F
            self.force -= 1

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
    for f in floors:
        world.blit(f.image, f.coordinates)

    for p in players:
        p.possibleMovements = ['left', 'right', 'down', 'up']
        onFloor = False

        #check if the player is on the floor
        for i, f in enumerate(floors):
            collision = checkCollision(p, f)
            collisionSite = collisionSiteCheck(p, f)

            if collision:
                #player cannot move towards the collision site anymore and stops jumping
                p.possibleMovements.remove(collisionSite)
                p.isJumping = False

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
            p.isJumping = False
            onFloor = True
            p.force = p.standardForce

        #player falls when not on floor and not jumping
        if onFloor == False and p.isJumping == False:
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

