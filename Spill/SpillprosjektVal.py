import pygame, sys
from pygame import image as img
from pygame.locals import *
import itertools
pygame.init()
pygame.font.init()
pygame.mixer.init()

window_height = 600
window_width = 640
#Spiller musikk fra Undertale på loop, NB må legge til musikken i mu_code sin music folder for at det skal fungere
pygame.mixer.music.load("music/OST.mp3")
pygame.mixer.music.play(-1)

win = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Underfail")
# alle bildene som brukes, NB må legge til bildene i mu_code sin images folder
char = img.load("images/standing.png")
walkRight = [img.load("images/standRight.png"), img.load("images/walkRight.png")]
walkLeft = [img.load("images/standLeft.png"), img.load("images/walkLeft.png")]
walkUp = [img.load("images/walkBackL.png"), img.load("images/walkBackR.png")]
walkDown = [img.load("images/walkDownR.png"), img.load("images/walkDownL.png")]
bg = [img.load("images/sans_house.png"), img.load("images/house_inside.png")]
rect = img.load("images/black.png")
#karakterens posisjon når spillet starter
x = 50
y = 300
width = 50
height = 64
vel = 4
b = 0
x_limit = [0,640]    # grenser for hvor karakteren kan bevege seg
y_limit = [230,370]
v = 7
m = 1
# Farger og tekst
black = (0, 0, 0)
white = (255, 255, 255)
font = pygame.font.SysFont("Britannic Bold", 20)
font2 = pygame.font.SysFont("Britannic Bold", 40)

clock = pygame.time.Clock()
# Definerer alle bevegelser
jump = False
left = False
right = False
up = False
down = False
# variabel som teller hvor mange steg vi tar
walkCount = 0

#Formelen for kinetisk energi som brukes til å hoppe
def force(m, v):
        return (1/2)*m*(v**2)
# Hvordan karakteren ser ut basert på retningen de bever seg i
def redrawGameWindow():
    global walkCount, b, x, y
    win.blit(bg[b], (0, 0))
    if walkCount >=4:
        walkCount = 0
    if left:
        win.blit(walkLeft[walkCount//2], (x, y))   # Heltallsdeling på 2 for at bildet bytter
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
        win.blit(char, (x,y))    # tilbake til å stå hvis ingen input
        walkCount = 0
    pygame.display.update()
#Definerer text funksjon
def text(s, size, x, y, colour):
    fontObj = pygame.font.Font(None, size) #Lager fontobjekt
    textSurfaceObj = fontObj.render(s, True, colour)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.left = x
    textRectObj.top = y
    win.blit(textSurfaceObj, textRectObj)
# Et slags starting screen
run = False
while run ==False:
    win.fill(black)
    label = font.render("click to start", 1, (255, 255, 255))
    label2 = font.render("press escape to exit", 1, (255, 255, 255))
    label3 = font2.render("Welcome to my Crib", 1, (255, 255, 255))
    label4 = font.render("Made by Valerie", 1, (255, 255, 255))
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            run = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
    win.blit(label, (300, 270))
    win.blit(label2, (275, 300))
    win.blit(label3, (210, 200))
    win.blit(label4, (290, 450))
    pygame.display.update()

run = True

while run:
    clock.tick(30)  #30 FPS

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

    keys = pygame.key.get_pressed()
    # Kan bruke piler eller WASD til å bevege seg og space til å hoppe
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and x > x_limit[0]:
        x -= vel
        left = True     # Aktiverer left for at riktig bilde skal vises
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

    if jump:  #Hvis jump er True
        y -= force(m, v)
        v = v-1
        if v < 0:
            m = -1
        if v == -6:
            jump = False
            v = 5
            m = 1

    if b == 0 and 280<x<360 and 220<y<250: # Hvis man er ute og kommer nærme døra, får man opp tekst
        text("Press E to enter", 50, 50, 530, white)
        pygame.display.update()
        if keys[pygame.K_e]: # Hvis man trykker på e byttes bildet
            b = 1
            x = 465    #gir karakteren koordinater som passer
            y = 420
            x_limit = [40, 520]    # setter nye grenser
            y_limit = [230, 440]
    elif b == 1 and 430<x<520 and 350<y<377:     # Hvis man er i huset kan man gå ut
        text("Press E to exit", 50, 50, 530, white)
        pygame.display.update()
        if keys[pygame.K_e]:
            b = 0
            x = 300
            y = 270
            x_limit = [0, 640]
            y_limit = [230, 370]
    elif b ==1 and 340>y>220:  # Hvis man kommer lengere inn i huset får man opp tekst
        text("Welcome to my crib, this is it", 50, 50, 530, white)
        pygame.display.update()
    else:
        win.blit(rect, (0,481)) # Ellers dekker jeg over teksten med svart for at teksten ikke overlapper

    redrawGameWindow()

pygame.quit()
exit()