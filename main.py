#!/usr/bin/env python3

import pygame
import sys
import os

'''
Objects
'''
# put Python classes and functions here
class Player(pygame.sprite.Sprite):
    '''
    Spawn a player
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.moveX = 0
        self.moveY = 0
        self.frame = 0
        self.images = []
        for i in range(1, 9):
            img = pygame.image.load(os.path.join('images', 'Walk' + str(i) + '.png'))
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()

    # def control(self, x, y):
    #     self.x +
'''
Setup
'''
# put run-once code here

#screen coordinates
worldx = 1000
worldy = 800

#set framerate, start clock and start pygame
fps = 60
ani = 6
clock = pygame.time.Clock()
pygame.init()

#setting the background
world = pygame.display.set_mode([worldx, worldy])
backdrop = pygame.image.load(os.path.join('images', 'stage.png'))
backdropbox = world.get_rect()

player = Player()
player.rect.x = 0
player.rect.y = 0
player_list = pygame.sprite.Group()
player_list.add(player)

main = True
'''
Main Loop
'''
# put game loop here
while main:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
            main = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                print('left')
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                print('right')
            if event.key == pygame.K_UP or event.key == ord('w'):
                print('jump')

            if event.key == ord('q'):
                pygame.quit(); sys.exit()
                main = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                print('left stop')
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                print('right stop')

    world.blit(backdrop, backdropbox)
    player_list.draw(world)
    pygame.display.flip()
    clock.tick(fps)
