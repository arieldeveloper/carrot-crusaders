from pygame import *
import sys
from os.path import abspath, dirname
from random import choice


BASE_PATH = abspath(dirname(__file__))
FONT_PATH = BASE_PATH + '/fonts/'
IMAGE_PATH = BASE_PATH + '/images/'

# Colors (R, G, B)
WHITE = (255, 255, 255)
GREEN = (78, 255, 87)
YELLOW = (241, 255, 0)
BLUE = (80, 255, 239)
PURPLE = (203, 0, 255)
RED = (237, 28, 36)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
SCREEN = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


FONT = FONT_PATH + 'space_invaders.ttf'

IMG_NAMES = ['ship', 'mystery',
             'enemy1_1', 'enemy1_2',
             'enemy2_1', 'enemy2_2',
             'enemy3_1', 'enemy3_2', 'alien1_1', 'alien1_2', 'alien2_1', 'alien2_2', 'alien3_1', 'alien3_2',
             'explosionblue', 'explosiongreen', 'explosionpurple',
             'laser', 'enemylaser', 'small', 'big', 'normal', 'game-over', 'powerup','mysteryship', 'insertcoin', 'insertcoin2', 'explosion', 'bulletnormal', 'bulletbig', 'bulletsmall', 'background']


IMAGES = {name: image.load(IMAGE_PATH + '{}.png'.format(name)).convert_alpha()
          for name in IMG_NAMES}

IMAGES['bulletsmall'] = transform.scale(IMAGES['bulletsmall'], (10, 30))
IMAGES['bulletnormal'] = transform.scale(IMAGES['bulletnormal'], (15, 35))
IMAGES['bulletbig'] = transform.scale(IMAGES['bulletbig'], (20, 40))

PLAYER_SIZE = 70

IMAGES['small'] = transform.scale(IMAGES['small'], (PLAYER_SIZE, PLAYER_SIZE + 20))
IMAGES['normal'] = transform.scale(IMAGES['normal'], (PLAYER_SIZE, PLAYER_SIZE + 20))
IMAGES['big'] = transform.scale(IMAGES['big'], (PLAYER_SIZE, PLAYER_SIZE + 20))

IMAGES['game-over'] = transform.scale(IMAGES['game-over'], (SCREEN_WIDTH, SCREEN_HEIGHT))
IMAGES['background'] = transform.scale(IMAGES['background'], (SCREEN_WIDTH, SCREEN_HEIGHT))
#appending intro images into an array
INTRO_IMAGES = []
for i in range(19, 31):
    img = image.load(IMAGE_PATH + 'intro' + str(i) + '.png').convert()
    img = transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    INTRO_IMAGES.append(img)

BG_IMAGES = []
for i in range(1, 5):
    img = image.load(IMAGE_PATH + 'bg' + str(i) + '.png').convert()
    img = transform.scale(img, (int(SCREEN_WIDTH / 1.5), int(SCREEN_HEIGHT /1.5)))
    BG_IMAGES.append(img)

BLOCKERS_POSITION = 450
ENEMY_DEFAULT_POSITION = 65  # Initial value for a new game
ENEMY_MOVE_DOWN = 35

PLAYER_STATE = 0