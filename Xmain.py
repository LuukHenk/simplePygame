#!/usr/bin/env python3

import pygame
import sys
import os

""" Objects """

# put Python classes and functions here
class Player(pygame.sprite.Sprite):
    def __init__(self):  #Spawn a player
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.scalingFactor = 4
        self.frame = 0
        self.images = []
        for i in range(1, 10):
            #Load player walking images
            img = pygame.image.load(os.path.join('images', 'Walk' + str(i) + '.png'))
            #rescale player image
            img = pygame.transform.scale(img, (int(img.get_size()[0] / self.scalingFactor),
                int(img.get_size()[1] / self.scalingFactor)))
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()

        self.size = self.images[0].get_size()

    def control(self, x, y):
        #TODO player should not walk further than the end of the screen
        self.movex += x
        self.movey += y

    def update(self):
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        #TODO how does this work!?
        # moving left
        if self.movex < 0:
            # print(self.images)
            if self.movex < 0:
                self.frame += 1
                if self.frame > 3*ani:
                    self.frame = 0
            # self.frame -= 1
            # if self.frame == -1:
            #     self.frame =
            self.image = self.images[self.frame//ani]

        # moving right
        if self.movex > 0:
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = self.images[(self.frame//ani)+4]

""" Setup """

#screen coordinates
screenSize = (1000, 800)

#set framerate, start clock and start pygame
fps = 60
ani = 10
clock = pygame.time.Clock()
pygame.init()

#set screen size
world = pygame.display.set_mode(screenSize)

#load and scale background
backdrop = pygame.image.load(os.path.join('images', 'stage.png'))
backdrop = pygame.transform.scale(backdrop, screenSize)
backdropbox = world.get_rect()

#Load player and set positions
player = Player()
player.rect.x = screenSize[0] / 2 - player.size[0] / 2
player.rect.y = screenSize[1] - player.size[1] + 10
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 10

main = True

""" Main loop """

while main:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
            main = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(-steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(steps, 0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                print('jump')

            if event.key == ord('q'):
                pygame.quit(); sys.exit()
                main = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(-steps, 0)

    world.blit(backdrop, backdropbox)
    player.update()
    player_list.draw(world)
    pygame.display.flip()
    clock.tick(fps)
