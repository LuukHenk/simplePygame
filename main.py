#!/usr/bin/env python3

import pygame
import sys
import os
from player import Player, HealthBar
from mob import Mob

""" Setup """

#screen coordinates
screenSize = (1000, 800)

#set framerate, start clock and start pygame
fps = 60
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

healthbar = HealthBar()
healthbar_list = pygame.sprite.Group()
healthbar_list.add(healthbar)

# Constructor expects colors as Tuple (RGB[a])
mob1 = Mob((255, 215, 0))
mob1_list = pygame.sprite.Group()
mob1_list.add(mob1)

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
    healthbar_list.draw(world)
    mob1.update()
    mob1_list.draw(world)
    pygame.display.flip()
    clock.tick(fps)
