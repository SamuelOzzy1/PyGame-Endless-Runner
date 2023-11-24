import pygame
import this
from random import randrange

pygame.init()

#display
width = 800
height = 600

pygame.display.set_caption("Runner")
screen = pygame.display.set_mode((width,height))
fclock = pygame.time.Clock()
timer = pygame.USEREVENT + 1
pygame.time.set_timer(timer,1000)

#Assets
spacebg = pygame.image.load("space.jfif")
font = pygame.font.Font("FB.TTF",20)
magicsong = pygame.mixer.Sound('Magic.mp3')
menusong = pygame.mixer.Sound('Menu.wav')
menuclick = pygame.mixer.Sound('MenuClick.mp3')
death_sound = pygame.mixer.Sound('sfx_hit.wav')
score_sound = pygame.mixer.Sound('sfx_point.wav')
gameoversound = pygame.mixer.Sound('gameover.mp3')

menusong.set_volume(0.2)
magicsong.set_volume(0.5)
gameoversound.set_volume(0.2)

#Main variables
gamemenu = True
gameover = False
gameactive = False
dead = False

#scores variables
highscore = 0
score1 = 0
fixedscore = 0
score = 0
score2 = 0

#Updatedscore/ highscore
def update_score(score, highscore):
    if score > highscore:
        highscore = score
    return highscore

#lose screen
def show_go_screen():
    lose = font.render("You Lose!", False, "yellow")
    lose2 = font.render("Press arrow key up to start again!", False, "yellow")
    display_score = font.render("Points= "f"{(int(score))}", False, "yellow")
    shownhighscore = font.render("Highest Score= "f"{(int(highscore))}", False, "yellow")

    loserect = lose.get_rect(center=(400, 250))
    lose2rect = lose2.get_rect(center=(400, 280))
    displayscorerect = display_score.get_rect(center=(400, 350))
    shownhighscorerect = shownhighscore.get_rect(center=(400, 380))

    screen.blit(spacebg, (0, 0))
    screen.blit(lose2,lose2rect)
    screen.blit(lose,loserect)
    screen.blit(shownhighscore,shownhighscorerect)
    screen.blit(display_score,displayscorerect)

#game main menu
def show_gamemenu():
    start = font.render("Press up arrow key to start", False, "yellow")
    startrect = start.get_rect(center=(400, 350))
    shownhighscore = font.render("Highest Score= "f"{(int(highscore))}", False, "yellow")

    shownhighscorerect = shownhighscore.get_rect(center=(400, 280))
    screen.blit(spacebg, (0, 0))
    screen.blit(start, startrect)
    screen.blit(shownhighscore, shownhighscorerect)

#class for the playable character
class Character:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.character1 = pygame.image.load("Enemy.png")
        self.character = pygame.transform.flip(self.character1, True, False)
        self.characterhitbox = self.character.get_rect(center = (x,y))
        self.character_movement_amount = 50

    def drawchar(self):
        screen.blit(self.character,self.characterhitbox)

#class for the enemy
class Enemy:
    def __init__(self):
        self.enemy = pygame.image.load("Ghost.png")
        self.enemyhitbox = self.enemy.get_rect(center=(800, randrange(height)))
        self.enemyspeed = 5

    def drawenemy(self):
        self.enemyhitbox.centerx -= self.enemyspeed
        if self.enemyhitbox.centerx <= 0:
            self.enemyhitbox.centerx = 800
            self.enemyhitbox.centery = randrange(height)
        screen.blit(self.enemy,self.enemyhitbox)

#class for the line
class Line:
    def __init__(self):
        self.line = pygame.image.load("Line.png")
        self.linehitbox = self.line.get_rect(midtop = (40,0))

    def drawline(self):
        screen.blit(self.line,self.linehitbox)

#to show the classes above
character = Character(60,300)
enemy = Enemy()
line = Line()

while not dead:

    #showing score and highscore ingame
    shownhighscore = font.render("Highest= "f"{(int(highscore))}", False, "yellow")
    shownhighscorerect = shownhighscore.get_rect(center=(50, 70))

    display_score = font.render("Points= "f"{(int(score))}", False, "yellow")
    displayscorerect = display_score.get_rect(center=(50, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dead = True
    #ingame
        keys = pygame.key.get_pressed()

        if gameactive == True:
            menusong.stop()
            gameoversound.stop()
            magicsong.play()

        if event.type == timer:
            enemy.enemyspeed = enemy.enemyspeed + 0.25
        if keys[pygame.K_UP] and character.characterhitbox.top >= 0:
            character.characterhitbox.centery -= character.character_movement_amount
        elif keys[pygame.K_DOWN] and character.characterhitbox.bottom <= 600:
            character.characterhitbox.centery += character.character_movement_amount

    #menu settings
        if gamemenu == True:
            menusong.play(-1)

            if keys[pygame.K_UP]:
                enemy.enemyspeed = 5
                score2 = int(pygame.time.get_ticks() / 1000)
                menuclick.play()
                gameactive = True
                gameover = False
                gamemenu = False

    #gameover settings
        if gameover == True:
            magicsong.stop()
            gameoversound.play()

            if keys[pygame.K_UP]:
                score1 = int(pygame.time.get_ticks()/1000)
                score2 = 0
                menuclick.play()
                enemy.enemyspeed = 5
                gameactive = True
                gameover = False

    #sound effect for every ghost passed the character
    if gameactive == True:
        if enemy.enemyhitbox.colliderect(line.linehitbox):
             score_sound.play()

        #score settings
        fixedscore = int(pygame.time.get_ticks() / 1000)
        score = fixedscore - score1 - score2
        highscore = update_score(score, highscore)

        line.drawline()
        screen.blit(spacebg,(0,0))
        character.drawchar()
        enemy.drawenemy()
        screen.blit(display_score, displayscorerect)
        screen.blit(shownhighscore, shownhighscorerect)

        #dead sound effect
        if enemy.enemyhitbox.colliderect(character.characterhitbox):
            death_sound.play()
            gameover = True
            gameactive = False

    #show gameover screen
    if gameover == True:
        show_go_screen()
        enemy.enemyhitbox.centerx = 0

    #show main menu (this will only be shown when opening the game)
    if gamemenu == True:
        show_gamemenu()
        enemy.enemyspeed = 5

    pygame.display.update()
    fclock.tick(60)