import os.path
import random
import sys
import time

import pygame
from .constants import *
from .ground import Ground
from .player import Player
from .pipe import Pipe


class Game:

    def __init__(self):
        self.pipes = None
        self.pipe = None
        self.player = None
        self.ground = None
        self.sprites = None
        self.bestScore = 0

        self.clock = pygame.time.Clock()
        pygame.init()
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.running = True

        self.dir = os.path.dirname(__file__)
        self.dir_sounds = os.path.join(self.dir, '../music')

        self.dir_images = os.path.join(self.dir, '../sprites')

    def start(self):
        self.menu()
        self.new()

    def new(self):
        self.generate_elements()
        self.score = 0
        self.playing = True
        self.background = pygame.image.load(os.path.join(self.dir_images, 'background.png'))
        self.scoreBackground = pygame.image.load(os.path.join(self.dir_images, 'scoreBackground.png'))
        self.restartButton = pygame.image.load(os.path.join(self.dir_images, 'restartButton.png'))

        pygame.mixer.music.load(os.path.join(self.dir_sounds, 'background.mp3'))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0)
        self.run()

    def generate_elements(self):
        # Generate ground

        self.ground = Ground(self.dir_images, 0)
        self.ground1 = Ground(self.dir_images, 336)
        self.ground2 = Ground(self.dir_images, 672)

        self.player = Player(100, self.ground.rect.top - 300, self.dir_images)

        self.pipes = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        self.generatePipes()
        self.sprites.add(self.ground, self.ground1, self.ground2)

        self.sprites.add(self.player)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.player.jump()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                if event.key == pygame.K_SPACE and not self.playing:
                    self.new()
            if event.type == pygame.MOUSEBUTTONDOWN and not self.playing:
                if INITIAL_POS_X_RETRY <= event.pos[POS_X] <= FINAL_POS_X_RETRY:
                    if INITIAL_POS_Y_RETRY <= event.pos[POS_Y] <= FINAL_POS_Y_RETRY:
                        self.new()

    def generatePipes(self):
        lastPosition = WIDTH + 100
        if not len(self.pipes) > 0:
            for w in range(0, MAX_PIPES):
                left = random.randrange(lastPosition + 300, lastPosition + 500)
                top = random.randrange(-100, 100)
                pipeBottom = Pipe(left, HEIGHT + 50 - top, self.dir_images, False)
                pipeTop = Pipe(left, 115 - top, self.dir_images, True)
                lastPosition = pipeBottom.rect.right
                self.sprites.add(pipeBottom, pipeTop)
                self.pipes.add(pipeBottom, pipeTop)

    def draw(self):
        #Draw Background
        rectBackground = self.background.get_rect()
        self.surface.blit(self.background, (0,0))
        self.surface.blit(self.background, (rectBackground.right, 0))
        self.surface.blit(self.background, (rectBackground.right*2, 0))
        self.surface.blit(self.background, (rectBackground.right*3, 0))


        self.drawText()
        self.sprites.draw(self.surface)
        pygame.display.flip()

    def update(self):
        if self.playing:
            pipe = self.player.collide_with(self.pipes)
            self.score += self.player.verifyPoints(self.pipes, self.dir_sounds)

            if pipe:
                self.stop()
            self.sprites.update()
            self.player.validateGround(self.ground)
            self.player.validateRoof()

            self.updateElements(self.pipes)
            self.generatePipes()

    def updateElements(self, elements):
        for element in elements:
            if not element.rect.right > 0:
                element.kill()

    def stop(self):
        self.playing = False
        pygame.mixer.music.stop()
        if self.score >= self.bestScore:
            self.bestScore = self.score
        sound = pygame.mixer.Sound(os.path.join(self.dir_sounds, 'colision.mp3'))
        sound.set_volume(VOLUME_SCORE)
        sound.play()
        self.player.stop()
        self.stopElements(self.pipes)

    def stopElements(self, elements):
        for element in elements:
            element.stop()

    def drawScoreBackground(self):
        DEFAULT_IMAGE_SIZE = (SCORE_BACKGROUND_SIZE_X, SCORE_BACKGROUND_SIZE_Y)
        self.scoreBackground = pygame.transform.scale(self.scoreBackground, DEFAULT_IMAGE_SIZE)
        self.surface.blit(self.scoreBackground, ((WIDTH - SCORE_BACKGROUND_SIZE_X) // 2, (HEIGHT - SCORE_BACKGROUND_SIZE_Y) // 2))

    def drawScore(self):
        self.displayText("SCORE", SCORE_TEXT_SIZE, LIGHT_RED, WIDTH // 2 + SCROLLING_X, HEIGHT // 2 - 60)
        self.displayText(str(self.score), SCORE_TEXT_SIZE, LIGHT_RED, WIDTH // 2 + SCROLLING_X, HEIGHT // 2-30)
        self.displayText("BEST", SCORE_TEXT_SIZE, LIGHT_RED, WIDTH // 2 + SCROLLING_X, HEIGHT // 2 + 10)
        self.displayText(str(self.bestScore), SCORE_TEXT_SIZE, LIGHT_RED, WIDTH // 2 + SCROLLING_X, HEIGHT // 2 + 40)

    def drawButton(self):
        DEFAULT_IMAGE_SIZE = (BUTTON_SIZE_X, BUTTON_SIZE_Y)
        self.restartButton = pygame.transform.scale(self.restartButton, DEFAULT_IMAGE_SIZE)
        self.surface.blit(self.restartButton, ((WIDTH - SCORE_BACKGROUND_SIZE_X) // 2 + 11, (HEIGHT - SCORE_BACKGROUND_SIZE_Y) // 2 - 60))

    def drawText(self):
        if self.playing:
            self.displayText(str(self.score), 36, LIGHT_RED, WIDTH // 2, 40)

        if not self.playing:
            self.drawScoreBackground()
            self.drawScore()
            self.drawButton()
            # self.displayText('GAME OVER', 20, RED, WIDTH // 2, HEIGHT // 2)
            # self.displayText('press R to restart', 20, RED, WIDTH // 2, 130)
            # self.displayText(self.bestScoreFormat(), 20, RED, WIDTH // 2, 200)

    def bestScoreFormat(self):
        return 'Best Score: {}'.format(self.bestScore)


    def displayText(self, text, size, color, posX, posY):
        font = pygame.font.Font("font/Minecrafter.Reg.ttf", size)
        text = font.render(text, True, color)
        rect = text.get_rect()
        rect.midtop = (posX, posY)
        self.surface.blit(text, rect)

    def menu(self):
        self.surface.fill(GREEN_MENU)
        self.displayText("Presiona una tecla para comenzar", 20, BLACK, WIDTH //2, HEIGHT//2)

        pygame.display.flip()
        self.wait()

    def wait(self):
        wait = True
        while wait:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                    wait = False