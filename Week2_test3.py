import time
import random
#from tkinter import *
import tkinter as tk
import pygame

pygame.init()
pygame.display.set_caption('Python Nibbles')

options = []
bestFont = pygame.font.SysFont('Comic Sans MS', 30)
run = True
cellSize = 30
scoreHeight = 45
screenDim = [12, 10]
size = (screenDim[0]*cellSize, screenDim[1]*cellSize+scoreHeight)
carryOn = True
direction = 3 # left
clock = pygame.time.Clock()
points = 0

class Square:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour

class Snake:
    def __init__(self, length, colour):
        self.segments = []
        self.length = length
        self.colour = colour
        self.pause = 320
        self.turn = 0
        x = int(screenDim[0]/2)
        y = int(screenDim[1]/2)
        for seg in range(length):
            self.segments.append(Square(x, y, colour))
            x += 1 # add segments to the right of "head"
    
    def isValid(self, theX, theY):
        if theX >= 0 and theX < screenDim[0] and theY >= 0 and theY < screenDim[1]:
            for seggy in range(1, len(self.segments), 1):
                if theX == self.segments[seggy].x and theY == self.segments[seggy].y:
                    return False
            return True
        else:
            return False

    def movePlayer(self):
        global run

        if self.turn < now():
            # checkKeys()
            self.turn = now()+self.pause
            for segment in range(len(self.segments)-1, 0, -1): # look at the segments in reverse order
                self.segments[segment].x = self.segments[segment-1].x
                self.segments[segment].y = self.segments[segment-1].y

            if direction == 0 and self.isValid(self.segments[0].x, self.segments[0].y-1):
                self.segments[0].y -= 1
            elif direction == 2 and self.isValid(self.segments[0].x, self.segments[0].y+1):
                self.segments[0].y += 1
            elif direction == 1 and self.isValid(self.segments[0].x+1, self.segments[0].y):
                self.segments[0].x += 1
            elif direction == 3 and self.isValid(self.segments[0].x-1, self.segments[0].y):
                self.segments[0].x -= 1
            else:
            #print("Game OVER!!!")
            #gameOver()
                run = False

            if self.segments[0].x == apple.x and self.segments[0].y == apple.y:
                moveFruit(self)
                self.ateFruit()

    def ateFruit(self):
        global points
        lastSegment = len(self.segments)-1
        self.segments.append(Square(self.segments[lastSegment].x, self.segments[lastSegment].y, self.colour))
        points += 1

        # inc speed slightly
        if points <= 8:
            self.pause -= 5
        elif points <= 16:
            self.pause -= 4
        elif points <= 24:
            self.pause -= 3
        elif points <= 48:
            self.pause -= 2
        elif points <= 72:
            self.pause -= 1
        elif points%2 == 0:
            self.pause -= 1

        print("Your pause:", self.pause)

# - - - - - - - 

def moveFruit(self):
    pos = [apple.x, apple.y]
    done = False
    while not done:
        for segment in self.segments:
            while (pos[0] == segment.x and pos[1] == segment.y) or (pos[0] == -1 and pos[1] == -1):
                pos = [random.randint(0, screenDim[0]-1), random.randint(0, screenDim[1]-1)]
                hasRandomised = True
        if hasRandomised:
            hasRandomised = False # reset to go through all the segments again
        else:
            done = True

    apple.x = pos[0]
    apple.y = pos[1]

def now():
    millis = int(round(time.time() * 1000))
    return millis

def checkKeys():
    global direction
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and direction != 2:
        direction = 0
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and direction != 3:
        direction = 1
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and direction != 0:
        direction = 2
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and direction != 1:
        direction = 3

def mainLoop():
    global run
    global outer
    global inner
    global direction
    global player
    player = Snake(4, (90, 0, 90))
    global apple
    apple = Square(-1, -1, (0, 180, 0))
    moveFruit(player)
    direction = 3
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                outer = False
                inner = False
        checkKeys()
        player.movePlayer()
        renderScreen()
        clock.tick(60)

def renderScreen():
    global screen
    global bestFont
    global size
    size = (screenDim[0]*cellSize, screenDim[1]*cellSize+scoreHeight)
    screen = pygame.display.set_mode(size)
    #scoreText = ""
    screen.fill((0, 0, 0)) # base background colour of black

    pygame.draw.rect(screen, apple.colour, (apple.x*cellSize, apple.y*cellSize+scoreHeight, cellSize, cellSize)) # draw the "apple"

    for segment in player.segments: # draw each part of the snake
        pygame.draw.rect(screen, (200, 0, 200), (segment.x*cellSize, segment.y*cellSize+scoreHeight, cellSize, cellSize))

    pygame.draw.rect(screen, (40, 40, 40), (0, 0, screenDim[0]*cellSize, scoreHeight)) # Texts background colour
    scoreText = "Your Points: " + str(points) # Text itself
    scoring = bestFont.render(scoreText, True, (255, 255, 255)) # Visual transformation of text
    screen.blit(scoring, (10, 0)) # display the text

    pygame.display.update()

def colourOps(selected):
    global options
    global screen

    opNums = 3 # was 4 to include Custom
    options = []

    for num in range(opNums):
        if num == selected:
            colour = (0, 255, 0)
        else:
            colour = (255, 0, 0)
    s = Square(num*(4*cellSize)+70, 500-50, colour)
    options.append(pygame.draw.rect(screen, s.colour, (s.x, s.y, cellSize, cellSize)))
    pygame.display.update()

def welcome():
    global run
    global options
    global screen
    global screenDim
    global outer
    global inner

    go = True
    size = (510, 500)
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))

    introText = ["Welcome to Nibble reboot!!", "Made in Python", "", "", 'Press "Enter" to begin...', "", "", "", "Choose Game Size:"]
    for i, t in enumerate(introText):
        intro = bestFont.render(t, True, (255, 255, 255)) # Visual transformation of text
        screen.blit(intro, (50, 35+i*40)) # display the text
    
    for i in range(3): # was range 4 to include Custom
        if i == 0:
            sizeText = "Small"
        elif i == 1:
            sizeText = "Med."
        elif i == 2:
            sizeText = "Large"
        elif i == 3:
            sizeText = "Cust."
        sizes = bestFont.render(sizeText, True, (255, 255, 255)) # Visual transformation of text
        screen.blit(sizes, (i*(4*cellSize)+50, 500-95)) # display the text
        colourOps(0)
        screenDim = [12, 10]
    
    colourOps(0)
    screenDim = [12, 10]

    while go:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked = -1
                for i, op in enumerate(options):
                    if op.collidepoint(pos):
                        clicked = i
                if clicked == 0:
                    print("#load preset 1")
                    colourOps(0)
                    screenDim = [12, 10]
                if clicked == 1:
                    print("#load preset 2")
                    colourOps(1)
                    screenDim = [26, 18]
                if clicked == 2:
                    print("#load preset 3")
                    colourOps(2)
                    screenDim = [38, 28]
                if clicked == 3:
                    print("#load custom dialog")
                    colourOps(3)
                    #screenDim = customOptions()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                go = False
                inner = True

        if event.type == pygame.QUIT:
            run = False
            go = False
            outer = False
            inner = False

def gameOver():
    global size
    global run
    global outer
    global inner

    exitText = ["Game Over", "Press:", '"Enter" to exit', '"T" to try again', '"S" to go to start']
    for i, t in enumerate(exitText):
        intro = bestFont.render(t, True, (0, 0, 255)) # Visual transformation of text
        screen.blit(intro, ((size[0]-260)/2, ((size[1]-260)/2)+10+i*60)) # display the text

    pygame.display.update()

    over = False
    while not over:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    over = True
                    inner = False
                    outer = False
                elif event.key == pygame.K_t:
                    over = True
                    # run = True
                elif event.key == pygame.K_s:
                    over = True
                    inner = False
                if event.type == pygame.QUIT:
                    over = True
                    inner = False
                    outer = False

outer = True
while outer:
    welcome()
    while inner:
        mainLoop()
        gameOver()

pygame.quit()
#cannot exit game