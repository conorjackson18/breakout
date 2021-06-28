import time
import pygame
from pygame.locals import *

pygame.init()

#Screen Variables
screenWidth = 600
screenHeight = 600

#Fonts
mainFont = pygame.font.SysFont('Calibri', 50)
bottomFont = pygame.font.SysFont('Calibri', 25)

#Colours
backgroundColour = (138, 138, 138)
brickColour = (98, 110, 189)
paddleColour = (106, 189, 98)
ballColour = (189, 98, 107)
textColour = (50,50,50)

#Game Variables
columns = 8
rows = 8
clock = pygame.time.Clock()
fps = 60
score = 0
ballIn = False
gameOver = 0
lives = 5

#Text display function
def drawText(text, font, textColour, x, y):
    image = font.render(text, True, textColour)
    screen.blit(image, (x,y))


class brickWall():
    def __init__(self):
        #Each brick variable
        self.width = 75
        self.height = 40

    def makeBricks(self):
        #Create a 2d list of the bricks
        self.bricks = []
        for row in range(rows):
            rowOfBricks = []
            for column in range(columns):
                xPos = column*self.width
                yPos = row*self.height
                brick = pygame.Rect(xPos, yPos, self.width, self.height)

                rowOfBricks.append(brick)
            
            self.bricks.append(rowOfBricks)

    def drawWall(self):
        #Iterate through bricks and draw them.
        for row in self.bricks:
            for brick in row:
                pygame.draw.rect(screen, brickColour, brick)
                pygame.draw.rect(screen, backgroundColour, brick, 2)


class paddle():
    def __init__(self):
        self.reset()
       
    def move(self):
        #Direction of the paddle.

        self.direction=0
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1

        if key[pygame.K_RIGHT] and self.rect.left < 500:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        #Draw the paddle.
        pygame.draw.rect(screen, paddleColour, self.rect)

    def reset(self):
        #Paddle variables.
        self.height = 10
        self.width = 100
        self.xPos = 250
        self.yPos = 500
        self.speed = 10
        self.rect = Rect(self.xPos, self.yPos, self.width, self.height)
        self.direction = 0



class ball():
    def __init__(self, x, y):
        self.score=0
        self.reset(x,y)

    
    def draw(self):
        #Draw the ball.
        pygame.draw.circle(screen, ballColour, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)

    def move(self):

        #To prevent double collision.
        thresholdCollide = 5

        #Assume wall is destroyed.
        wallDestroyed = 1
        rowCount=0

        #Iterate through bricks looking for collision.
        for row in wall.bricks:
            itemCount=0

            for block in row:
                #Determine what direction the collision occured.
                if self.rect.colliderect(block):
                    self.score+=1
                    if abs(self.rect.bottom - block.top) < thresholdCollide and self.ySpeed > 0:
                        self.ySpeed *= -1
                    if abs(self.rect.top - block.bottom) < thresholdCollide and self.ySpeed < 0:
                        self.ySpeed *= -1
                    if abs(self.rect.right - block.left) < thresholdCollide and self.xSpeed > 0:
                        self.xSpeed *= -1
                    if abs(self.rect.left - block.right) < thresholdCollide and self.xSpeed < 0:
                        self.xSpeed *= -1

                    #Remove brick from screen
                    wall.bricks[rowCount][itemCount] = (0,0,0,0)
                
                #If any bricks still exist, wall is not destroyed.
                if wall.bricks[rowCount][itemCount] != (0,0,0,0):
                    wallDestroyed = 0
                
                itemCount += 1
            rowCount += 1

        if wallDestroyed == 1:
            self.death = 1
            gameOver = 1
    
        #Collision with left and right of screen
        if self.rect.left < 0 or self.rect.right > screenWidth:
            self.xSpeed *= -1
        
        #Collision with top of screen
        if self.rect.top < 0:
            self.ySpeed *= -1
        
        #Collision with bottom of screen
        if self.rect.bottom > screenHeight:
            self.death = -1

        #Collision with paddle
        if self.rect.colliderect(myPaddle):
            if abs(self.rect.bottom - myPaddle.rect.top) < thresholdCollide and self.ySpeed > 0:
                 self.ySpeed *= -1
                 self.xSpeed += myPaddle.direction
            else:
                self.xSpeed *= -1
            
        #Ball movement.
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed

        return self.death

    def reset(self, x, y):
        #Ball variables.
        self.radius = 10
        self.xPos = x - self.radius
        self.yPos = y
        self.rect = Rect(self.xPos, self.yPos, self.radius*2, self.radius*2)
        self.xSpeed = 4
        self.ySpeed = -4
        self.death = 0



#Creating objects
wall = brickWall()
wall.makeBricks()
myPaddle = paddle()
myBall = ball(myPaddle.xPos+50,myPaddle.yPos -20)
screen = pygame.display.set_mode((screenWidth, screenHeight))


#Game loop
game = True
while game:

    clock.tick(fps)
    screen.fill(backgroundColour)

    #updating items every loop
    wall.drawWall()
    myPaddle.draw()
    myBall.draw()
    drawText(f'Score : {myBall.score}', bottomFont, textColour, 20, 550)
    drawText(f'Lives : {lives}', bottomFont, textColour, 400, 550)

    #If ball is in play
    if ballIn:
        myPaddle.move()
        gameOver=myBall.move()

        if gameOver != 0:
            ballIn=False

    #If ball is out of play
    if not ballIn:

        #Game is starting/ lives are left
        if gameOver == 0:
            drawText('Click button to start', mainFont, textColour, 100, 400)

        #Wall is empty
        elif gameOver == 1:
            game=False
            drawText('Congrats! You Won!', mainFont, textColour, 100, 400)

        #Subtract a life or game over is 0 lives left
        elif gameOver == -1:
            lives -= 1
            if lives < 0:
                drawText('Oh No! You Lost!', mainFont, textColour, 100, 400)
                game=False
        
        gameOver = 0

    for event in pygame.event.get():

        #If you press the X 
        if event.type == pygame.QUIT:
            game = False
            pygame.quit()

        #If you click to start game
        if event.type == pygame.MOUSEBUTTONDOWN and ballIn == False:
            ballIn=True
            myBall.reset(myPaddle.xPos+50,myPaddle.yPos -20)
            myPaddle.reset()

    pygame.display.update()

time.sleep(5)
pygame.quit()
