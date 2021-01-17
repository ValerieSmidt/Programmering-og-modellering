import pygame, sys
from pygame import image as img
from pygame.locals import *
import itertools
pygame.init()
pygame.font.init()
pygame.mixer.init()

window_height = 600
window_width = 640
'''Spiller musikk fra Undertale på loop'''
pygame.mixer.music.load("music/OST.mp3")
pygame.mixer.music.play(-1)

win = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Underfail")
# alle bildene som brukes
char = img.load("images/standing.png")
walkRight = [img.load("images/standRight.png"), img.load("images/walkRight.png")]
walkLeft = [img.load("images/standLeft.png"), img.load("images/walkLeft.png")]
walkUp = [img.load("images/walkBackL.png"), img.load("images/walkBackR.png")]
walkDown = [img.load("images/walkDownR.png"), img.load("images/walkDownL.png")]
bg = [img.load("images/sans_house.png"), img.load("images/house_inside.png")]
rect = img.load("images/black.png")
x = 50
y = 300
width = 50
height = 64
vel = 4
b = 0
x_limit = [0,640]
y_limit = [230,370]

black = (0, 0, 0)
white = (255, 255, 255)
font = pygame.font.SysFont("Britannic Bold", 20)
font2 = pygame.font.SysFont("Britannic Bold", 40)


clock = pygame.time.Clock()

jump = False
left = False
right = False
up = False
down = False

walkCount = 0

v = 7
m = 1

def force(m, v):
        return (1/2)*m*(v**2)

def redrawGameWindow():
    global walkCount
    global b
    global x
    global y
    win.blit(bg[b], (0, 0))
    if walkCount >= 4:
        walkCount = 0
    if left:
        win.blit(walkLeft[walkCount//2], (x, y))
        walkCount += 1
    elif right:
        win.blit(walkRight[walkCount//2], (x, y))
        walkCount += 1
    elif up:
        win.blit(walkUp[walkCount//2], (x, y))
        walkCount += 1
    elif down:
        win.blit(walkDown[walkCount//2], (x, y))
        walkCount += 1
    else:
        win.blit(char, (x,y))
        walkCount = 0
    pygame.display.update()

def text(s, size, x, y, colour):
    fontObj = pygame.font.Font(None, size)
    textSurfaceObj = fontObj.render(s, True, colour)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.left = x
    textRectObj.top = y
    win.blit(textSurfaceObj, textRectObj)

run = False
while run ==False:
    win.fill(black)
    label = font.render("click to start", 1, (255, 255, 255))
    label2 = font.render("press escape to exit", 1, (255, 255, 255))
    label3 = font2.render("Welcome to my Crib", 1, (255, 255, 255))
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            run = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    win.blit(label, (300, 270))
    win.blit(label2, (275, 300))
    win.blit(label3, (210, 200))
    pygame.display.update()

run = True

while run:
    clock.tick(30)

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

    keys = pygame.key.get_pressed()

    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and x > x_limit[0]:
        x -= vel
        left = True
        right = False
        up = False
        down = False
    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and x < x_limit[1] - width:
        x += vel
        right = True
        left = False
        up = False
        down = False

    elif (keys[pygame.K_UP] or keys[pygame.K_w]) and y > y_limit[0]:
        y -= vel
        right = False
        left = False
        up = True
        down = False

    elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and y < y_limit[1] - height - vel:
        y += vel
        right = False
        left = False
        up = False
        down = True
    else:
        right = False
        left = False
        up = False
        down = False
        walkCount = 0

    if jump == False:

        if keys[pygame.K_SPACE]:

            jump = True
            right = False
            left = False
            up = False
            down = False
            walkCount = 0

    if jump:
        y -= force(m, v)
        v = v-1
        if v < 0:
            m = -1
        if v == -6:
            jump = False
            v = 5
            m = 1

    if b == 0 and 280<x<360 and 220<y<250:
        text("Press E to enter", 50, 50, 530, white)
        pygame.display.update()
        if keys[pygame.K_e]:
            b = 1
            x = 465
            y = 420
            x_limit = [40, 520]
            y_limit = [230, 440]
    elif b == 1 and 430<x<520 and 350<y<377:
        text("Press E to exit", 50, 50, 530, white)
        pygame.display.update()
        if keys[pygame.K_e]:
            b = 0
            x = 300
            y = 270
            x_limit = [0, 640]
            y_limit = [230, 370]
    elif b ==1 and 340>y>220:
        text("Welcome to my crib, this is it", 50, 50, 530, white)
        pygame.display.update()
    else:
        win.blit(rect, (0,481))

    redrawGameWindow()

pygame.quit()
exit()