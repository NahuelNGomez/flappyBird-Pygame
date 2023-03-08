import os

import pygame.sprite

from .constants import *


class Pipe(pygame.sprite.Sprite):

    def __init__(self, left, bottom, dir_images, rotate):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(dir_images, 'pipeGreen.png'))
        DEFAULT_IMAGE_SIZE = (40, 250)
        self.image = pygame.transform.scale(self.image, DEFAULT_IMAGE_SIZE)
        self. image = pygame.transform.rotate(self.image, rotate * 180)
        self.passed = False

        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.bottom = bottom

        self.velX = PIPE_SPEED

    def update(self):
        self.rect.left -= self.velX

    def stop(self):
        self.velX = 0

    def getPosX(self):
        return self.rect.x

    def isPassed(self):
        return self.passed

    def nowPass(self):
        self.passed = True
