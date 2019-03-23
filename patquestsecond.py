#importings
import pygame
import scipy
from random import randrange
from skimage.transform import resize



pygame.init()

screen = pygame.display.set_mode((900,700))

up = [pygame.image.load("playerup.png"),pygame.image.load("playerup2.png"),pygame.image.load("playerup3.png"),pygame.image.load("playerup4.png")]
down = [pygame.image.load("playerdown.png"),pygame.image.load("playerdown2.png"),pygame.image.load("playerdown4.png"),pygame.image.load("playerdown3.png")]
left = [pygame.image.load("playerleft.png"),pygame.image.load("playerleft2.png"),pygame.image.load("playerleft4.png"),pygame.image.load("playerleft3.png")]
right = [pygame.image.load("playerright.png"),pygame.image.load("playerright2.png"),pygame.image.load("playerright3.png"),pygame.image.load("playerright4.png")]

bg = pygame.image.load("background.png")
bg = pygame.transform.scale(bg, (900,700))

items = [pygame.image.load("Pepper.png"),pygame.image.load("Cheese.png"),pygame.image.load("Bread.png")]
#treasure = resize(treasure, (64, 64), anti_aliasing=True)

enemyImg = pygame.image.load("enemy.png")
enemyImg = pygame.transform.scale(enemyImg, (35,40))

font = pygame.font.SysFont("comicsans",85)

def checkCollision(x,y,x2,y2):
    global screen,textWin
    collisionState = False
    if y >= y2 and y <= y2 + 40:
        if x >= x2 and x <= x2+35:
            collisionState = True
            
        elif x + 35 >= x2 and x + 35 <= x2 + 35:
            collisionState = True
            
    elif y + 40 >= y2 and y + 40<= y2 + 40:
        if x >= x2 and x<= x2+35:
            collisionState = True
            
        elif x+35 >= x2 and x+35 <= x2 + 35:
            collisionState = True
    return collisionState, x, y, x2, y2

#Object classes

class character(object):
    def __init__(self,x,y,width,height,items):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.walkCount = 0
        self.lives = 1
        self.standing = True
        self.items = []
        self.up = True
        self.down = False
        self.left= False
        self.right = False

    def draw(self, screen):
        if self.walkCount + 1 >= 12:
            self.walkCount = 0

        if not(self.standing):
            if self.up:
                screen.blit(up[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.down:
                screen.blit(down[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.left:
                screen.blit(left[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                screen.blit(right[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.up:
                screen.blit(up[0], (self.x, self.y))
            elif self.down:
                screen.blit(down[0], (self.x, self.y))
            elif self.left:
                screen.blit(left[0], (self.x, self.y))
            elif self.right:
                screen.blit(right[0], (self.x, self.y))

class item(object):
    def __init__(self,x,y,width,height,items):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.item = items
        self.collected = False
        self.type = type

    def draw(self, screen):
        if self.collected == True:
            pass
        else:
            if self.item == "Pepper":
                screen.blit(items[0], (self.x,self.y))
            if self.item == "Cheese":
                screen.blit(items[1], (self.x,self.y))
            if self.item == "Bread":
                screen.blit(items[2], (self.x,self.y))

class enemy(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        screen.blit(enemyImg, (self.x,self.y))

    
frame = pygame.time.Clock()
level = 1
finished = False

def redrawGameWindow():
    screen.blit(bg, (0,0))
    pat.draw(screen)
    pot.draw(screen)
    well.draw(screen)
    treasured.draw(screen)
    enemy.draw(screen)
    pygame.display.update()

screen.blit(bg,(0,0))
pat = character(200, 410, 0, 0, " ")
well = item(65, 300, 0, 0, "Pepper")
pot = item(800,525,15,15, "Cheese")
treasured = item(50, 450,15,15, "Bread")
enemy = enemy(300, 300, 20, 20)
pat.draw(screen)
pot.draw(screen)
well.draw(screen)
treasured.draw(screen)

while finished == False: #While game is not finished
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    if pat.x > enemy.x:
        enemy.x += 1
    if pat.x < enemy.x:
        enemy.x -= 1
    if pat.y > enemy.y:
        enemy.y += 1
    if pat.y < enemy.y:
        enemy.y -= 1

    if pat.lives <= 0:
        textWin = font.render("You're Dead!",True,(0,0,0))
        screen.blit(textWin,(450 - textWin.get_width()/2,350 - textWin.get_height()/2))
        effect = pygame.mixer.Sound('Select.wav')
        effect.play()
        pygame.display.flip()
        frame.tick(1) 

    if len(pat.items) == 3 :
        level += 1
        textWin = font.render("You've reached level "+str(level),True,(0,0,0))
        screen.blit(textWin,(450 - textWin.get_width()/2,350 - textWin.get_height()/2))
        pygame.display.flip()
        pat.y = 650
        pat.x = 450 - 35/2
        well.y = randrange(100, 700)
        well.x = randrange(100, 700)
        pot.y = randrange(100, 700)
        pot.x = randrange(100, 700)
        treasured.y = randrange(100, 700)
        treasured.x = randrange(100, 700)
        frame.tick(1)
        pat.items = []  
        well.collected = False
        pot.collected = False
        treasured.collected = False

    pressedKeys = pygame.key.get_pressed()

    if pressedKeys[pygame.K_UP] and pat.y > 0 :
        pat.y -= 5
        pat.up = True
        pat.down = False
        pat.left = False
        pat.right = False
        pat.standing = False

    elif pressedKeys[pygame.K_DOWN] and pat.y < 665:
        pat.y += 5
        pat.up = False
        pat.down = True
        pat.left = False
        pat.right = False
        pat.standing = False

    elif pressedKeys[pygame.K_LEFT] and pat.x > 0 :
        pat.x -= 5
        pat.up = False
        pat.down = False
        pat.left = True
        pat.right = False
        pat.standing = False

    elif pressedKeys[pygame.K_RIGHT] and pat.x < 860:
        pat.x += 5
        pat.up = False
        pat.down = False
        pat.left = False
        pat.right = True
        pat.standing = False
    
    else:
        pat.standing = True
        pat.walkCount = 0

    collisionWell,x,y,x2,y2 = checkCollision(pat.x,pat.y,well.x,well.y)
    if collisionWell == True and well.collected == False:
        effect = pygame.mixer.Sound('Select.wav')
        effect.play()
        pygame.display.flip()
        pat.items.append("cheese")
        well.collected = True
    else:
        pass

    collisionPot,x,y,x2,y2 = checkCollision(pat.x,pat.y,pot.x,pot.y)
    if collisionPot == True and pot.collected == False:
        effect = pygame.mixer.Sound('Select.wav')
        effect.play()
        pygame.display.flip()
        pat.items.append("steak")
        pot.collected = True
    else:
        pass

    collisionTreasure,x,y,x2,y2 = checkCollision(pat.x,pat.y,treasured.x,treasured.y)
    if collisionTreasure == True and treasured.collected == False:
        effect = pygame.mixer.Sound('Select.wav')
        effect.play()
        pygame.display.flip()
        pat.items.append("bread")  
        treasured.collected = True
    else:
        pass

    collisionEnemy,x,y,x2,y2 = checkCollision(pat.x,pat.y,enemy.x,enemy.y)
    if collisionEnemy == True:
        name = "John"
        textLose = font.render("You were killed by "+name,True,(255,0,0))
        screen.blit(textLose,(450 - textLose.get_width()/2, 350 - textLose.get_height()/2))
        pygame.display.flip()
        pat.y = 650
        pat.x = 450 - 35/2
        pat.lives -= 1
        print(pat.lives)
        frame.tick(1)  

    
    pygame.display.flip()
    redrawGameWindow()
    frame.tick(30)
    
