import pygame
import sys
import os

class Player(pygame.sprite.Sprite):
    def __init__(self):  #Spawn a player
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.scalingFactor = 4
        self.frame = 0

        #Load images
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
        ani = 10

        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

        #TODO how does this work!?
        # moving left
        if self.movex < 0:
            if self.movex < 0:
                self.frame += 1
                if self.frame > 3*ani:
                    self.frame = 0
                self.image = self.images[(self.frame//ani)+4]

        # moving right
        if self.movex > 0:
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = self.images[(self.frame//ani)+4]

class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        emptyHeart = pygame.transform.scale(pygame.image.load('images/healthbar/emptyheart.png'), [50, 50])
        fullHeart = pygame.transform.scale(pygame.image.load('images/healthbar/fullheart.png'), [50, 50])
        # Todo : Draw multiple hearts, preferably in container
        self.healthcontainer = [fullHeart, fullHeart, fullHeart]
        self.health = 3
        self.image = fullHeart
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
