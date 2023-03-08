import os

import pygame.sprite

from game.constants import *


class Player(pygame.sprite.Sprite):
    def __init__(self, left, bottom, dir_images):
        pygame.sprite.Sprite.__init__(self)

        self.images = (
            pygame.image.load(os.path.join(dir_images, 'bird.png')),
            pygame.image.load(os.path.join(dir_images, 'birdDownflap.png')),
            pygame.image.load(os.path.join(dir_images, 'birdUpflap.png'))
        )
        self.actualImage = 0
        self.image = self.images[self.actualImage]

        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.bottom = bottom

        self.posY = self.rect.bottom
        self.velY = 0
        self.timeForChangeImage = TIME_FOR_CHANGE_IMAGE

        self.playing = True

    def update_pos(self):
        self.velY += PLAYER_GRAV
        self.posY += self.velY + (0.5 * PLAYER_GRAV)

    def update(self):
        if self.playing:
            self.update_pos()
            self.rect.bottom = self.posY
            if self.timeForChangeImage == 0:
                if self.actualImage != 2:
                    self.image = self.images[self.actualImage+1]
                    self.actualImage += 1
                else:
                    self.actualImage = 0
                    self.image = self.images[self.actualImage]
                self.timeForChangeImage = TIME_FOR_CHANGE_IMAGE
            self.timeForChangeImage -= 1

    def validateGround(self, ground):
        result = pygame.sprite.collide_rect(self, ground)
        if result:
            self.velY = 0
            self.posY = ground.rect.top

    def validateRoof(self):
        if self.rect.top < 0:
            self.posY = 25
            self.velY = 0

    def collide_with(self, sprites):
        objects = pygame.sprite.spritecollide(self, sprites, False)
        if objects:
            return objects[0]

    def verifyPoints(self, sprites, dir_sounds):
        score = 0
        for sprite in sprites:
            if self.rect.x >= sprite.getPosX():
                if not sprite.isPassed():
                    score += 1
                    sprite.nowPass()
        if score >= 1:
            sound = pygame.mixer.Sound(os.path.join(dir_sounds, 'score.mp3'))
            sound.set_volume(VOLUME_SCORE)
            sound.play()
        return score // 2

    def stop(self):
        self.playing = False

    def jump(self):
        self.velY = -JUMP_FORCE
