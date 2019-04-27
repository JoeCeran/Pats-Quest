import pygame 


def checkCollision(x,y,treasureX,treasureY):
    global screen,textWin
    collisionState = False
    if y >= treasureY and y <= treasureY + 40:
        if x >= treasureX and x <= treasureX+35:
            collisionState = True
            
        elif x + 35 >= treasureX and x + 35 <= treasureX + 35:
            collisionState = True
            
    elif y + 40 >= treasureY and y + 40<= treasureY + 40:
        if x >= treasureX and x<= treasureX+35:
            collisionState = True
            
        elif x+35 >= treasureX and x+35 <= treasureX + 35:
            collisionState = True
    return collisionState, x, y


pygame.mixer.pre_init(44100, -16, 2, 2048) 
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('Main.mp3')
pygame.mixer.music.play(-1)


screen = pygame.display.set_mode((900,700))

class character(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.walkCount = 0

finished = False # 0 < 10 -> True/ 10<10 -> False
x = 450-35/2
y = 650
index = [0,1,2,3,4]
array = [0,1,2,4,5,"Hello"]

playerImage = pygame.image.load("playerup.png")
playerImage = pygame.transform.scale(playerImage, (43,47))
playerImage = playerImage.convert_alpha()

backgroundImage = pygame.image.load("background.png")
backgroundImage = pygame.transform.scale(backgroundImage, (900,700))
screen.blit(backgroundImage, (0,0))

treasureImage = pygame.image.load("Treasure.png")
treasureImage = pygame.transform.scale(treasureImage, (35,40))
treasureImage = treasureImage.convert_alpha()

enemyImage = pygame.image.load("enemy.png")
enemyImage = pygame.transform.scale(enemyImage, (35,40))
enemyImage = enemyImage.convert_alpha()

bulletImage = pygame.image.load("bullet.png")
bulletImage = pygame.transform.scale(bulletImage, (35,40))
bulletImage = bulletImage.convert_alpha()

enemyX = 100
enemyY = 580-40/2

treasureX = 450 - 35/2
treasureY = 50

potX = 800
potY = 525

wellX = 70
wellY = 300

screen.blit(treasureImage,(treasureX,treasureY))

font = pygame.font.SysFont("comicsans",85)
level = 1
gold = 0

items = ["Steak", "Cheese", "Onions"]
poisons = ["Peppers", "Mushrooms", "HipsterShit"]
enemyNames = {0: "Max", 1: "Jill", 2: "Greg", 3: "Diane"}

frame = pygame.time.Clock()
collisionTreasure = False
collisionEnemy = False
collisionPot = False
collisionWell = False
movingRight = True

enemies = [(enemyX,enemyY,movingRight)]

while finished == False: #While game is not finished
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

    
    pressedKeys = pygame.key.get_pressed()

    enemyIndex = 0
    for enemyX,enemyY,movingRight in enemies:
        if enemyX >= 850-35:
            movingRight = False
        elif enemyX <= 100:
            movingRight = True
        if movingRight == True:
            enemyX += 5*level
        else:
            enemyX -= 5*level
        enemies[enemyIndex] = (enemyX,enemyY, movingRight)
        enemyIndex += 1

    if pressedKeys[pygame.K_UP] == 1 and y > 0:
        playerImage = pygame.image.load("playerup.png")
        playerImage = pygame.transform.scale(playerImage, (43,47))
        playerImage = playerImage.convert_alpha()
        y -= 5
    if pressedKeys[pygame.K_DOWN] == 1 and y < 665:
        playerImage = pygame.image.load("playerdown.png")
        playerImage = pygame.transform.scale(playerImage, (43,47))
        playerImage = playerImage.convert_alpha()
        y += 5
    if pressedKeys[pygame.K_LEFT] == 1 and x > 0:
        playerImage = pygame.image.load("playerleft.png")
        playerImage = pygame.transform.scale(playerImage, (43,47))
        playerImage = playerImage.convert_alpha()
        x -= 5
    if pressedKeys[pygame.K_RIGHT] == 1 and x < 860:
        playerImage = pygame.image.load("playerright.png")
        playerImage = pygame.transform.scale(playerImage, (43,47))
        playerImage = playerImage.convert_alpha()
        x += 5
    #if pressedKeys[pygame.K_SPACE] == 1

    
    #playerImage.clamp_ip(screen_rect)

    rectOne = pygame.Rect(x,y,30,30)#x,y,width,height

    color = (0,0,255)#R,G,B
    white = (255,255,255)
    screen.fill(white)
    screen.blit(backgroundImage,(0,0))
    screen.blit(treasureImage,(treasureX,treasureY))
    screen.blit(playerImage,(x,y))

    #Enemy Spawning and collision 
    enemyIndex = 0
    for enemyX,enemyY,movingRight in enemies:
        screen.blit(enemyImage,(enemyX,enemyY))
        collisionEnemy,x,y = checkCollision(x,y,enemyX,enemyY)
        if collisionEnemy == True:
            name = enemyNames[enemyIndex]
            textLose = font.render("You were killed by "+name,True,(255,0,0))
            screen.blit(textLose,(450 - textLose.get_width()/2, 350 - textLose.get_height()/2))
            pygame.display.flip()
            y = 650
            x = 450 - 35/2
            frame.tick(1)  
        enemyIndex += 1

    #Treasure collision
    collisionTreasure,x,y = checkCollision(x,y,treasureX,treasureY)
    if collisionTreasure == True:
        level += 1
        enemies.append((enemyX-50*level,enemyY-50*level,False))
        textWin = font.render("You've reached level "+str(level),True,(0,0,0))
        screen.blit(textWin,(450 - textWin.get_width()/2,350 - textWin.get_height()/2))
        pygame.display.flip()
        y = 650
        x = 450 - 35/2
        frame.tick(1)  

    #Pot collision
    collisionPot,x,y = checkCollision(x,y,potX,potY)
    if collisionPot == True:
        textWin = font.render("You found the cheese!",True,(0,0,0))
        screen.blit(textWin,(450 - textWin.get_width()/2,350 - textWin.get_height()/2))
        effect = pygame.mixer.Sound('Select.wav')
        effect.play()
        y = 650
        x = 450 - 35/2
        pygame.display.flip()
        frame.tick(1)  

    #Pot collision
    collisionWell,x,y = checkCollision(x,y,wellX,wellY)
    if collisionWell == True:
        textWin = font.render("You found the steak!",True,(0,0,0))
        screen.blit(textWin,(450 - textWin.get_width()/2,350 - textWin.get_height()/2))
        pygame.display.flip()

        frame.tick(1)  

    pygame.display.flip()
    frame.tick(30)
