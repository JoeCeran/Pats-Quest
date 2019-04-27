#importings
import pygame
import time
import scipy
from random import randrange
from skimage.transform import resize



pygame.mixer.pre_init(44100, -16, 2, 2048) 
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('assets/music/Main.mp3')
pygame.mixer.music.play(0)
screen = pygame.display.set_mode((900,700))

up = [pygame.image.load("assets/img/playerup.png"),pygame.image.load("assets/img/playerup2.png"),pygame.image.load("assets/img/playerup3.png"),pygame.image.load("assets/img/playerup4.png")]
down = [pygame.image.load("assets/img/playerdown.png"),pygame.image.load("assets/img/playerdown2.png"),pygame.image.load("assets/img/playerdown4.png"),pygame.image.load("assets/img/playerdown3.png")]
left = [pygame.image.load("assets/img/playerleft.png"),pygame.image.load("assets/img/playerleft2.png"),pygame.image.load("assets/img/playerleft4.png"),pygame.image.load("assets/img/playerleft3.png")]
right = [pygame.image.load("assets/img/playerright.png"),pygame.image.load("assets/img/playerright2.png"),pygame.image.load("assets/img/playerright3.png"),pygame.image.load("assets/img/playerright4.png")]

up = [pygame.image.load("assets/img/playerup.png"),pygame.image.load("assets/img/playerup2.png"),pygame.image.load("assets/img/playerup3.png"),pygame.image.load("assets/img/playerup4.png")]
stubbsdown = [pygame.image.load("assets/img/stubbsdown1.png"),pygame.image.load("assets/img/stubbsdown1.png"),pygame.image.load("assets/img/stubbsdown1.png"),pygame.image.load("assets/img/stubbsdown1.png")]
left = [pygame.image.load("assets/img/playerleft.png"),pygame.image.load("assets/img/playerleft2.png"),pygame.image.load("assets/img/playerleft4.png"),pygame.image.load("assets/img/playerleft3.png")]
right = [pygame.image.load("assets/img/playerright.png"),pygame.image.load("assets/img/playerright2.png"),pygame.image.load("assets/img/playerright3.png"),pygame.image.load("assets/img/playerright4.png")]

bg = pygame.image.load("assets/img/background.png")
bg = pygame.transform.scale(bg, (900,700))

bg2 = pygame.image.load("assets/img/background3.png")
bg2 = pygame.transform.scale(bg2, (900,700))

items = [pygame.image.load("assets/img/Pepper.png"),pygame.image.load("assets/img/Cheese.png"),pygame.image.load("assets/img/Bread.png"),pygame.image.load("assets/img/steak.png"),pygame.image.load("assets/img/Door.png"), pygame.image.load("assets/img/DoorOpen.png")]
#treasure = resize(treasure, (64, 64), anti_aliasing=True)



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

def fade(width, height):
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(3)

def enemyMovement(x, y, x2, y2, i):
    global enemies
    if x >= x2 + 10 :
        enemies[i].x += 3
        enemies[i].up = False
        enemies[i].down = False
        enemies[i].left = False
        enemies[i].right = True
        enemies[i].standing = False
    elif x <= x2 - 10:
        enemies[i].x -= 3
        enemies[i].up = False
        enemies[i].down = False
        enemies[i].left = True
        enemies[i].right = False
        enemies[i].standing = False
    elif y >= y2 - 10:
        enemies[i].y += 3
        enemies[i].up = False
        enemies[i].down = True
        enemies[i].left = False
        enemies[i].right = False
        enemies[i].standing = False
    elif y <= y2 - 10:
        enemies[i].y -= 3
        enemies[i].up = True
        enemies[i].down = False
        enemies[i].left = False
        enemies[i].right = False
        enemies[i].standing = False

def bossMovement(x, y, x2, y2, i):
    global enemies
    if x >= x2 + 10 :
        enemies[i].x += 5
        enemies[i].up = False
        enemies[i].down = False
        enemies[i].left = False
        enemies[i].right = True
        enemies[i].standing = False
    elif x <= x2 - 10:
        enemies[i].x -= 5
        enemies[i].up = False
        enemies[i].down = False
        enemies[i].left = True
        enemies[i].right = False
        enemies[i].standing = False
    elif y >= y2 - 10:
        enemies[i].y += 5
        enemies[i].up = False
        enemies[i].down = True
        enemies[i].left = False
        enemies[i].right = False
        enemies[i].standing = False
    elif y <= y2 - 10:
        enemies[i].y -= 5
        enemies[i].up = True
        enemies[i].down = False
        enemies[i].left = False
        enemies[i].right = False
        enemies[i].standing = False

#Object classes



class character(object):
    def __init__(self,x,y,width,height,items):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.walkCount = 0
        self.lives = 3
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
        self.open = False

        

    def draw(self, screen):
        if self.collected == True:
            pass
        else:
            if self.item == "Cheese":
                screen.blit(items[1], (self.x,self.y))
            if self.item == "Bread":
                screen.blit(items[2], (self.x,self.y))
            if self.item == "Steak":
                screen.blit(items[3], (self.x,self.y))
            if self.item == "Door":
                if self.open == False:
                    screen.blit(items[4], (self.x,self.y))
                else:
                    screen.blit(items[5], (self.x,self.y))

class poisons(object):
    def __init__(self,x,y,width,height,items):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.item = items
        self.collected = False
        self.type = type
        self.open = False

        

    def draw(self, screen):
        if self.collected == True:
            pass
        else:
            if self.item == "Pepper":
                screen.blit(items[0], (self.x,self.y))
            

class enemy(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.standing = True
        self.walkCount = 0
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
                screen.blit(stubbsdown[self.walkCount//3], (self.x,self.y))
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

class boss(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.standing = True
        self.walkCount = 0
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
                screen.blit(stubbsdown[self.walkCount//3], (self.x,self.y))
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
    

    
frame = pygame.time.Clock()
level = 1
finished = False
start = False



def redrawGameWindow():
    if level > 1 :
        screen.blit(bg2, (0,0))
    else: 
        screen.blit(bg, (0,0))
    pat.draw(screen)
    cheese.draw(screen)
    pepper.draw(screen)
    bread.draw(screen)
    Door.draw(screen)
    enemies[0].draw(screen)
    if level >= 2:
        enemies[1].draw(screen)
    if level >= 3:
        enemies[2].draw(screen)
    steak.draw(screen)
    pygame.display.update()



if level > 1 :
    screen.blit(bg2, (0,0))
else: 
    screen.blit(bg, (0,0))
pat = character(600, 450, 0, 0, " ")
pepper = poisons(65, 300, 0, 0, "Pepper")
cheese = item(800,525,15,15, "Cheese")
bread = item(50, 450,15,15, "Bread")
steak = item(80, 500,15,15, "Steak")
Door = item(450, 40, 0, 0, "Door")
enemies = [enemy(300, 300, 20, 20), enemy(0, 0, 20, 20), enemy(0, 0, 20, 20) ]
bosses = [boss(0, 0, 20, 20)]
pat.draw(screen)
pepper.draw(screen)
cheese.draw(screen)
steak.draw(screen)
bread.draw(screen)
Door.draw(screen)
enemies[0].draw(screen)
if level >= 2:
    enemies[1].draw(screen)
if level >= 3:
    enemies[2].draw(screen)
if level >= 4:
    bosses[0].draw(screen)



while finished == False: #While game is not finished
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
    
    #if pat.x > enemies.x + 15 or pat.y > enemies.y + 15 or pat.x < enemies.x + 15 or pat.y < enemies.y + 15 :
        #enemies.standing = True
        #enemies.walkCount = 0

    enemyMovement(pat.x, pat.y, enemies[0].x, enemies[0].y, 0)
    if level >= 2:
        enemyMovement(pat.x, pat.y, enemies[1].x, enemies[1].y, 1)
    if level >= 3:
        enemyMovement(pat.x, pat.y, enemies[2].x, enemies[2].y, 2)
    if level >= 4:
        bossMovement(pat.x, pat.y, bosses[0].x, enemies[0].y, 0)

    if len(pat.items) == 4:
        if level == 4:
            Door.open = True
            collisionDoor,x,y,x2,y2 = checkCollision(pat.x,pat.y,Door.x,Door.y)
            if collisionDoor == True:
                import patwin
        else:
            Door.open = True
            collisionDoor,x,y,x2,y2 = checkCollision(pat.x,pat.y,Door.x,Door.y)
            if collisionDoor == True:
                effect = pygame.mixer.Sound('assets/sounds/Select.wav')
                effect.play()
                level += 1
                fade(900,700)
                pygame.display.flip()
                pat.y = 600
                pat.x = 450 - 35/2
                pepper.y = randrange(100, 595)
                pepper.x = randrange(100, 595)
                cheese.y = randrange(100, 595)
                cheese.x = randrange(200, 595)
                bread.y = randrange(100, 595)
                bread.x = randrange(100, 595)
                steak.y = randrange(100, 595)
                steak.x = randrange(100, 595)
                enemies[0].y = randrange(100, 595)
                enemies[0].x = randrange(100, 595)
                if level >= 2:
                    enemies[1].y = randrange(100, 595)
                    enemies[1].x = randrange(100, 595)
                if level >= 3:
                    enemies[2].y = randrange(100, 595)
                    enemies[2].x = randrange(100, 595)
                if level >= 4:
                    effect = pygame.mixer.Sound('assets/sounds/Shields.wav')
                    effect.play()
                    pygame.mixer.music.load('assets/music/Boss.mp3')
                    pygame.mixer.music.play(0)
                frame.tick(1)
                pat.items = []  
                pepper.collected = False
                cheese.collected = False
                bread.collected = False
                steak.collected = False
                Door.open = False
                screen.blit(bg2, (0,0))
                start = False
    

    pressedKeys = pygame.key.get_pressed()

    if pressedKeys[pygame.K_UP] and pat.y > 15 :
        pat.y -= 5
        pat.up = True
        pat.down = False
        pat.left = False
        pat.right = False
        pat.standing = False

    elif pressedKeys[pygame.K_DOWN] and pat.y < 595:
        pat.y += 5
        pat.up = False
        pat.down = True
        pat.left = False
        pat.right = False
        pat.standing = False

    elif pressedKeys[pygame.K_LEFT] and pat.x > 45 :
        pat.x -= 5
        pat.up = False
        pat.down = False
        pat.left = True
        pat.right = False
        pat.standing = False

    elif pressedKeys[pygame.K_RIGHT] and pat.x < 815:
        pat.x += 5
        pat.up = False
        pat.down = False
        pat.left = False
        pat.right = True
        pat.standing = False
    
    else:
        pat.standing = True
        pat.walkCount = 0

    collisionWell,x,y,x2,y2 = checkCollision(pat.x,pat.y,pepper.x,pepper.y)
    if collisionWell == True and pepper.collected == False:
        effect = pygame.mixer.Sound('assets/sounds/Select.wav')
        effect.play()
        pygame.display.flip()
        pat.items.append("pepper")
        pepper.collected = True
    else:
        pass

    collisionPot,x,y,x2,y2 = checkCollision(pat.x,pat.y,cheese.x,cheese.y)
    if collisionPot == True and cheese.collected == False:
        effect = pygame.mixer.Sound('assets/sounds/Select.wav')
        effect.play()
        pygame.display.flip()
        pat.items.append("cheese")
        cheese.collected = True
    else:
        pass

    collisionTreasure,x,y,x2,y2 = checkCollision(pat.x,pat.y,bread.x,bread.y)
    if collisionTreasure == True and bread.collected == False:
        effect = pygame.mixer.Sound('assets/sounds/Select.wav')
        effect.play()
        pygame.display.flip()
        pat.items.append("bread")  
        bread.collected = True
    else:
        pass

    collisionSteak,x,y,x2,y2 = checkCollision(pat.x,pat.y,steak.x,steak.y)
    if collisionSteak == True and steak.collected == False:
        effect = pygame.mixer.Sound('assets/sounds/Select.wav')
        effect.play()
        pygame.display.flip()
        pat.items.append("steak")  
        steak.collected = True
    else:
        pass

    collisionenemies,x,y,x2,y2 = checkCollision(pat.x,pat.y,enemies[0].x,enemies[0].y)
    if collisionenemies == True:
        effect = pygame.mixer.Sound('assets/sounds/Damage.wav')
        effect.play()
        pygame.display.flip()
        enemies[0].y = randrange(100, 595)
        enemies[0].x = randrange(100, 595)
        pat.y = 595
        pat.x = 450 - 35/2
        pat.lives -= 1
        print(pat.lives)
        frame.tick(1)  

    collisionenemies2,x,y,x2,y2 = checkCollision(pat.x,pat.y,enemies[1].x,enemies[1].y)
    if collisionenemies2 == True:
        effect = pygame.mixer.Sound('assets/sounds/Damage.wav')
        effect.play()
        pygame.display.flip()
        enemies[1].y = randrange(100, 595)
        enemies[1].x = randrange(100, 595)
        pat.y = 595
        pat.x = 450 - 35/2
        pat.lives -= 1
        print(pat.lives)
        frame.tick(1)  

    collisionenemies3,x,y,x2,y2 = checkCollision(pat.x,pat.y,enemies[2].x,enemies[2].y)
    if collisionenemies3 == True:
        effect = pygame.mixer.Sound('assets/sounds/Damage.wav')
        effect.play()
        pygame.display.flip()
        enemies[2].y = randrange(100, 595)
        enemies[2].x = randrange(100, 595)
        pat.y = 595
        pat.x = 450 - 35/2
        pat.lives -= 1
        print(pat.lives)
        frame.tick(1)  

    if start == False :
        textWin = font.render("Level "+str(level),True,(0,0,0))
        screen.blit(textWin,(450 - textWin.get_width()/2,350 - textWin.get_height()/2))
        pygame.display.flip()
        frame.tick(1) 
        start = True

    if pat.lives <= 0:
        textWin = font.render("Game Over!",True,(0,0,0))
        screen.blit(textWin,(450 - textWin.get_width()/2,350 - textWin.get_height()/2))
        pygame.display.flip()
        pygame.mixer.music.load('assets/music/Game Over.mp3')
        pygame.mixer.music.play(0)
        frame.tick(1) 
        finished = True
        time.sleep(5)
        pygame.display.quit()
    else:
        pygame.display.flip()
        redrawGameWindow()
        frame.tick(30)
    

    
