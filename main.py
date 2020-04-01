#Carrot Crusaders
# Ariel Chouminov

from pygame import *
import sys
from os.path import abspath, dirname
from random import choice
from constants import *
from enemy import *
from boss import *
import random

class Player(sprite.Sprite):
    def __init__(self, x = 375, y = 0):
        sprite.Sprite.__init__(self)
        x = SCREEN_WIDTH / 3
        y = SCREEN_HEIGHT - PLAYER_SIZE - 25
        self.states = [IMAGES['small'], IMAGES['normal'], IMAGES['big']]
        self.currentState = self.states[PLAYER_STATE]
        self.image = self.currentState
        self.rect = self.image.get_rect(topleft=(x, y)) #placement
        self.speed = 5
        self.hidden = False
    def shrink(self):
        global PLAYER_STATE
        #shrinks the player
        if PLAYER_STATE > 0:
            PLAYER_STATE -= 1
            self.currentState = self.states[PLAYER_STATE]
        else:
            print("HES ALREASDY TOO SMALL")

    def grow(self):
        global PLAYER_STATE

        #grows the player
        if PLAYER_STATE < (len(self.states) - 1):
            PLAYER_STATE += 1
            self.currentState = self.states[PLAYER_STATE]

    def update(self, keys, *args):
        if self.hidden == False:
            if keys[K_LEFT] and self.rect.x > 0:
                self.rect.x -= self.speed
            if keys[K_RIGHT] and self.rect.x < SCREEN_WIDTH - (PLAYER_SIZE):
                self.rect.x += self.speed

            self.image = self.currentState
            game.screen.blit(self.image, self.rect)



class Bullet(sprite.Sprite):
    def __init__(self, xpos, ypos, direction, speed, filename, side):
        sprite.Sprite.__init__(self)
        self.image = IMAGES[filename]
        self.rect = self.image.get_rect(topleft=(xpos, ypos))
        self.speed = speed
        self.direction = direction
        self.side = side
        self.filename = filename

    def update(self, keys, *args):
        game.screen.blit(self.image, self.rect)
        self.rect.y += self.speed * self.direction
        # self.rect.x += self.speed * self.direction
        if self.rect.y < 15 or self.rect.y > SCREEN_HEIGHT:
            self.kill()


class PlayerExplosion(sprite.Sprite):
    def __init__(self, player, *groups):
        super(PlayerExplosion, self).__init__(*groups)
        self.image = player.image
        self.rect = self.image.get_rect(topleft=(player.rect.x, player.rect.y))
        self.timer = time.get_ticks()
        self.player = player


    def update(self, current_time, *args):
        global SCREEN
        passed = current_time - self.timer
        # x = self.player.rect.x
        # y = self.player.rect.y
        # rect = draw.rect(SCREEN,(0,0,0), (x,y,self.image.get_width(),self.image.get_height()))
        self.player.hidden = True
        if 300 < passed <= 600:
            game.screen.blit(self.image, self.rect)
        elif 900 < passed:
            self.player.hidden = False


class Powerup(sprite.Sprite):
    #Draws the amount of lives on the screen
    def __init__(self, xpos):
        sprite.Sprite.__init__(self)
        self.image = IMAGES['powerup']
        self.timer = time.get_ticks()
        self.image = transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(topleft=(xpos, SCREEN_HEIGHT - 50))

    def update(self, currentTime, *args):
        #add code to only blit at certain times
        passed = currentTime - self.timer

        if passed < 3000:
            game.screen.blit(self.image, self.rect)

        elif 3300 < passed <= 3700:
            game.screen.blit(self.image, self.rect)

        elif 4000 < passed <= 4500:
            game.screen.blit(self.image, self.rect)

        elif passed > 4000:
            self.kill()


class Text(object):
    def __init__(self, textFont, size, message, color, xpos, ypos):
        self.font = font.Font(textFont, size)
        self.surface = self.font.render(message, True, color)
        self.rect = self.surface.get_rect(topleft=(xpos, ypos))

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

class CarrotCrusaders(object):
    def __init__(self):
        init()
        self.clock = time.Clock()
        self.caption = display.set_caption('Carrot Crusaders')
        self.background = IMAGES['background']
        self.screen = SCREEN
        self.startGame = False
        self.introScreen = True #first screen on
        self.gameOver = False
        self.startTime = False
        # Counter for enemy starting position (increased each new round)
        self.enemyPosition = ENEMY_DEFAULT_POSITION
        self.gameOverText = Text(FONT, 50, 'Game Over', WHITE, 250, 270)
        self.nextRoundText = Text(FONT, 50, 'Next Round', WHITE, 210, 270)
        self.scoreText = Text(FONT, 20, 'Score', WHITE, 5, 5)
        self.time_since_enter = 0
        self.w = SCREEN_WIDTH
        self.h = SCREEN_HEIGHT
        self.x = 0
        self.y = 0
        self.x2 = 0
        self.y2 = -self.h
        self.i = 0
        self.doubleShooting = False
        self.enemiesLeftToKill = 50
        self.highscore = self.read_highscore()
        self.doubleShootingBulletsLeft = 0


    def read_highscore(self):
        global BASE_PATH
        f = open(BASE_PATH + "/" + "highscore.txt", "r")
        if f.mode == "r":
            contents = f.read()
            try:
                contents = int(contents)
            except:
                self.write_highscore(0)
            return contents

    def write_highscore(self, score):
        global BASE_PATH
        f = open(BASE_PATH + "/" + "highscore.txt", "w+")
        f.write(str(score))

    def intro_screen_animation(self, currentTime2):
        currentTime = int(time.get_ticks() / 400) - 3

        if currentTime < len(INTRO_IMAGES):
            self.screen.fill(0)
            self.screen.blit(INTRO_IMAGES[currentTime], (0, 0))
            display.update()
        else:
            #MAKES THE INSERT COIN BLINK
            self.screen.blit(INTRO_IMAGES[len(INTRO_IMAGES) - 1], (0,0))
            i = self.i
            i += 1
            if i < 30:
                self.screen.blit(IMAGES['insertcoin'], (int(SCREEN_WIDTH/3.3), int(SCREEN_HEIGHT - (SCREEN_HEIGHT/2.3))))

            elif i < 60:
                self.screen.blit(IMAGES['insertcoin2'], (int(SCREEN_WIDTH / 3.3), int(SCREEN_HEIGHT - (SCREEN_HEIGHT / 2.3))))
            else:
                i = 0
            self.i = i

    def reset(self, score):
        self.player = Player() #makes a small player
        self.explosionsGroup = sprite.Group()
        self.powerupGroup = sprite.Group()
        self.bullets = sprite.Group()
        self.mysteryShip = Mystery(game)
        self.mysteryGroup = sprite.Group(self.mysteryShip)
        self.enemyBullets = sprite.Group()
        self.make_enemies()
        self.allSprites = sprite.Group(self.player, self.enemies, self.mysteryShip)
        self.keys = key.get_pressed()
        self.enemiesLeftToKill = 50
        self.timer = time.get_ticks()
        self.noteTimer = time.get_ticks()
        self.playerTimer = time.get_ticks()
        self.score = score
        self.i = 0
        self.highscore = self.read_highscore()
        self.doubleShooting = False

    def create_new_powerup(self):
        while True:
            xposition = random.randint(0, SCREEN_WIDTH)
            if xposition < (self.player.rect.x - PLAYER_SIZE) or xposition > (self.player.rect.x + PLAYER_SIZE):
                break

        powerupToAdd = Powerup(xposition) #change so it doesn't hit player make so the number it not in the facinity of the player
        self.powerupGroup.add(powerupToAdd)

    @staticmethod
    def should_exit(evt):
        # type: (pygame.event.EventType) -> bool
        return evt.type == QUIT or (evt.type == KEYUP and evt.key == K_ESCAPE)

    def check_input(self):
        self.keys = key.get_pressed()
        for e in event.get():
            if self.should_exit(e):
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if len(self.bullets) == 0:
                        if not self.doubleShooting:
                            if PLAYER_STATE == 0:
                                #small dude
                                bulletImg = 'bulletsmall'
                            elif PLAYER_STATE == 1:
                                #normal dude
                                bulletImg = 'bulletnormal'
                            elif PLAYER_STATE == 2:
                                bulletImg = 'bulletbig'

                            bullet = Bullet(self.player.rect.x + 23,
                                            self.player.rect.y + 5, -1,
                                            15, bulletImg, 'center')
                            self.bullets.add(bullet)
                            self.allSprites.add(self.bullets)
                        elif self.doubleShooting:
                            print(self.doubleShootingBulletsLeft)
                            if self.doubleShootingBulletsLeft <= 0:
                                self.doubleShooting = False
                            else:
                                self.doubleShootingBulletsLeft -= 1
                            if PLAYER_STATE == 0:
                                #small dude
                                bulletImg = 'bulletsmall'
                            elif PLAYER_STATE == 1:
                                #normal dude
                                bulletImg = 'bulletnormal'
                            elif PLAYER_STATE == 2:
                                bulletImg = 'bulletbig'

                            leftbullet = Bullet(self.player.rect.x + 8,
                                                self.player.rect.y + 5, -1,
                                                15, bulletImg, 'left')
                            rightbullet = Bullet(self.player.rect.x + 38,
                                                 self.player.rect.y + 5, -1,
                                                 15, bulletImg, 'right')
                            self.bullets.add(leftbullet)
                            self.bullets.add(rightbullet)
                            self.allSprites.add(self.bullets)

    def make_enemies(self):

        enemies = EnemiesGroup(10, 5, game)
        for row in range(5):
            for column in range(10):
                enemy = Enemy(row, column, game)
                enemy.rect.x = 157 + (column * 60)
                enemy.rect.y = self.enemyPosition + (row * 65)
                enemies.add(enemy)

        self.enemies = enemies

    def make_enemies_shoot(self):
        if (time.get_ticks() - self.timer) > 700 and self.enemies:
            enemy = self.enemies.random_bottom()
            self.enemyBullets.add(
                Bullet(enemy.rect.x + 14, enemy.rect.y + 20, 1, 5,
                       'enemylaser', 'center'))
            self.allSprites.add(self.enemyBullets)
            self.timer = time.get_ticks()

    def calculate_score(self, row):
        scores = {0: 30,
                  1: 20,
                  2: 20,
                  3: 10,
                  4: 10,
                  5: choice([50, 100, 150, 300])
                  }

        score = scores[row]
        self.score += score
        return score

    def check_collisions(self):
        global PLAYER_STATE
        sprite.groupcollide(self.bullets, self.enemyBullets, True, True)
        for enemy in sprite.groupcollide(self.enemies, self.bullets,
                                         True, True).keys():
            self.enemiesLeftToKill -= 1
            self.calculate_score(enemy.row)
            EnemyExplosion(enemy,game, self.explosionsGroup)
            self.gameTimer = time.get_ticks()
            if random.random() > 0.92:
                self.create_new_powerup()

        for mystery in sprite.groupcollide(self.mysteryGroup, self.bullets,
                                           True, True).keys():
            score = self.calculate_score(mystery.row)
            MysteryExplosion(mystery, score, game, self.explosionsGroup)
            newShip = Mystery(game)
            self.allSprites.add(newShip)
            self.mysteryGroup.add(newShip)
            if random.random() > 0.40:
                self.create_new_powerup()

        if sprite.spritecollide(self.player, self.enemyBullets, True):
            if PLAYER_STATE == 0: #small
                self.gameOver = True
                self.startGame = False

            else:
                self.player.shrink()

            PlayerExplosion(self.player, self.explosionsGroup)
            self.playerTimer = time.get_ticks()


        if sprite.spritecollide(self.player, self.powerupGroup, True):
            if PLAYER_STATE == 2:
                #he is big
                self.doubleShooting = True
                self.doubleShootingBulletsLeft = 5
                self.score += 300
            elif PLAYER_STATE == 1:
                self.player.grow()
                self.doubleShooting = True
                self.doubleShootingBulletsLeft = 5
            elif PLAYER_STATE == 0:
                self.player.grow()

        if sprite.spritecollide(self.player, self.enemies, True):
            if self.enemies.bottom >= 540:
                self.gameOver = True
                self.startGame = False

        if self.enemies.bottom >= SCREEN_HEIGHT - 20:
            sprite.groupcollide(self.enemies, self.player, True, True)
            if not self.player.alive() or self.enemies.bottom >= 600:
                self.gameOver = True
                self.startGame = False

    def create_game_over(self):
        #background screen
        global BG_IMAGES
        i = self.i
        i += 1

        if i < 40:
            self.screen.fill(0)
            background = BG_IMAGES[0]
            self.screen.blit(background, ((SCREEN_WIDTH / 2) - (background.get_width() / 2), 220))

        elif i < 60:
            background = BG_IMAGES[1]
            self.screen.blit(background, ((SCREEN_WIDTH / 2) - (background.get_width() / 2), 220))
        elif i < 90:
            background = BG_IMAGES[2]
            self.screen.blit(background, ((SCREEN_WIDTH / 2) - (background.get_width() / 2), 220))
        elif i < 120:
            background = BG_IMAGES[3]
            self.screen.blit(background, ((SCREEN_WIDTH / 2) - (background.get_width() / 2), 220))
        else:
            i = 0
        self.i = i

        if self.score > int(self.highscore):
            self.write_highscore(self.score)
            # All the texts
            highscoreText = Text(FONT, 20, 'NEW HIGHSCORE:', WHITE, SCREEN_WIDTH / 5 +85, 20)
            highscoreActual = Text(FONT, 20, str(self.score), WHITE, SCREEN_WIDTH / 2 + 80, 20)

            congratsText = Text(FONT, 40, 'CONGRATULATIONS!', WHITE, SCREEN_WIDTH / 7 + 30, 70)

            highscoreText.draw(self.screen)
            highscoreActual.draw(self.screen)

            congratsText.draw(self.screen)

        else:
            #All the texts
            highscoreText = Text(FONT, 20, 'Highscore:', WHITE, 80, 20)
            highscoreActual = Text(FONT, 20, str(self.highscore), WHITE, 225, 20)

            scoreText = Text(FONT, 20, 'Your Score:', WHITE, SCREEN_WIDTH - 260, 20)
            scoreActual = Text(FONT, 20, str(self.score), WHITE, SCREEN_WIDTH - 105, 20)

            highscoreText.draw(self.screen)
            highscoreActual.draw(self.screen)

            scoreText.draw(self.screen)
            scoreActual.draw(self.screen)

        for e in event.get():
            if self.should_exit(e):
                sys.exit()

    def scrolling_background(self):
        #Scrolls the background
        self.y2 += 0.7
        self.y += 0.7

        self.screen.blit(self.background, (self.x, self.y))
        self.screen.blit(self.background, (self.x2,self.y2))

        if self.y > self.h:
            self.y = -self.h
        if self.y2 > self.h:
            self.y2 = -self.h

    def main(self):
        #MAIN LOOP
        while True:
            if self.introScreen:
                #Intro SCREEN
                self.time_since_enter = (time.get_ticks()) / 1000
                currentTime = time.get_ticks()
                self.intro_screen_animation(currentTime) #runs the lure screen
                for e in event.get():
                    if self.should_exit(e):
                        sys.exit()
                    if e.type == KEYUP:
                        self.reset(0) #also creates a new player
                        self.startGame = True
                        self.startTime = True
                        self.introScreen = False

            elif self.startGame:

                # game started
                if not self.enemies and not self.explosionsGroup or self.enemiesLeftToKill == 0: #IF THE SCREEN IS CLEARED (NO ENEMIES LEFT)
                    currentTime = time.get_ticks()
                    if currentTime - self.gameTimer < 3000:
                        self.scrolling_background()
                        self.scoreText2 = Text(FONT, 20, str(self.score),
                                               GREEN, 85, 5)
                        highscoreText = Text(FONT, 20, 'HIGHSCORE:', WHITE, SCREEN_WIDTH - 250, 20)
                        highscoreActual = Text(FONT, 20, str(self.highscore), WHITE, SCREEN_WIDTH - 90, 20)
                        self.scoreText.draw(self.screen)
                        self.scoreText2.draw(self.screen)
                        highscoreText.draw(self.screen)
                        highscoreActual.draw(self.screen)
                        self.nextRoundText.draw(self.screen)
                        self.check_input()

                    if currentTime - self.gameTimer > 3000:
                        # Move enemies down
                        self.enemyPosition += ENEMY_MOVE_DOWN
                        self.reset(self.score)
                        self.gameTimer += 3000
                else:
                    currentTime = time.get_ticks()
                    self.scrolling_background()
                    self.scoreText2 = Text(FONT, 20, str(self.score), GREEN,
                                           85, 5)
                    highscoreText = Text(FONT, 20, 'HIGHSCORE:', WHITE, SCREEN_WIDTH - 235, 5)
                    highscoreActual = Text(FONT, 20, str(self.highscore), GREEN, SCREEN_WIDTH - 90, 5)
                    self.scoreText.draw(self.screen)
                    self.scoreText2.draw(self.screen)
                    highscoreText.draw(self.screen)
                    highscoreActual.draw(self.screen)
                    self.check_input()
                    self.enemies.update(currentTime)
                    self.allSprites.update(self.keys, currentTime)
                    self.explosionsGroup.update(currentTime)
                    self.check_collisions()
                    self.make_enemies_shoot()
                    self.powerupGroup.update(currentTime)

            elif self.gameOver:
                currentTime = time.get_ticks()
                # Reset enemy starting position
                self.enemyPosition = ENEMY_DEFAULT_POSITION
                self.create_game_over()
                keys = key.get_pressed()

                if keys[K_UP]:
                    self.reset(0) #also creates a new player
                    self.startGame = True
                    self.gameOver = False

            display.update()
            self.clock.tick(40)

if __name__ == '__main__':
    game = CarrotCrusaders()
    game.main()
