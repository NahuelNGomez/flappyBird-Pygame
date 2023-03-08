import os

import pygame.sprite
from .constants import *


class Ground(pygame.sprite.Sprite):

    def __init__(self, dir_images, posX):
        pygame.sprite.Sprite.__init__(self)

        # Define ground size and color
        self.image = pygame.image.load(os.path.join(dir_images, 'base.png'))

        # Define ground position
        self.rect = self.image.get_rect()
        self.rect.x = posX
        self.rect.y = HEIGHT - 40
