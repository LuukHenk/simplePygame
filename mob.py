import pygame
import os
import random

class Mob(pygame.sprite.Sprite):
    # Constructor expects colors as Tuple (RGB[a])
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (50, 50)

    def update(self):
        self.rect.x += random.randint(1, 2) + random.randint(1, 2)
        self.rect.y += random.randint(1, 2) + random.randint(1, 2)
