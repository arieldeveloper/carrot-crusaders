from pygame import *
import sys
from os.path import abspath, dirname
from random import choice
from constants import *
from enemy import *
from main import *

class Mystery(sprite.Sprite):
    def __init__(self, game):
        sprite.Sprite.__init__(self)
        self.game = game
        self.image = IMAGES['mysteryship']
        self.image = transform.scale(self.image, (95, 70))
        self.rect = self.image.get_rect(topleft=(-80, 45))
        self.row = 5
        self.moveTime = 25000
        self.direction = 1
        self.timer = time.get_ticks()


    def update(self, keys, currentTime, *args):
        resetTimer = False
        passed = currentTime - self.timer
        if passed > self.moveTime:
            if self.rect.x < 840 and self.direction == 1:
                self.rect.x += 2
                self.game.screen.blit(self.image, self.rect)
            if self.rect.x > -100 and self.direction == -1:
                self.rect.x -= 2
                self.game.screen.blit(self.image, self.rect)

        if self.rect.x > 830:
            self.direction = -1
            resetTimer = True
        if self.rect.x < -90:
            self.direction = 1
            resetTimer = True
        if passed > self.moveTime and resetTimer:
            self.timer = currentTime


class MysteryExplosion(sprite.Sprite):
    def __init__(self, mystery, score, game, *groups):
        super(MysteryExplosion, self).__init__(*groups)
        self.game = game
        self.text = Text(FONT, 20, str(score), WHITE,
                         mystery.rect.x + 20, mystery.rect.y + 6)
        self.timer = time.get_ticks()

    def update(self, current_time, *args):
        passed = current_time - self.timer
        if passed <= 200 or 400 < passed <= 600:
            self.text.draw(self.game.screen)
        elif 600 < passed:
            self.kill()