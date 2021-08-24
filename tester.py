# Import and initialize the pygame library
import pygame
pygame.init()
# Set up the drawing window
screen_width=500
screen_height=480
win = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("My First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')
#frames
clock = pygame.time.Clock()
bulletSound = pygame.mixer.Sound('Game_bullet.mp3')
hitSound = pygame.mixer.Sound('Game_hit.mp3')

music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)
score = 0
#Setting positions and dimensions of character
class player(object):
    def __init__(self, x, y, width, height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=5
        self.isJump=False
        self.jumpCount=10
        self.left=False
        self.right=False
        self.walkCount=0
        self.standing = True
        self.hitbox = (self.x + 20, self.y + 20, 28, 60)
    def draw(self, win):
        if self.walkCount +1 >= 27:
            self.walkCount=0
        if not (self.standing):    
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount+=1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount+=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x,self.y))
            else:
                win.blit(walkLeft[0], (self.x,self.y))
        self.hitbox = (self.x + 20, self.y + 10, 28, 60)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
    
    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text= font1.render("-5", 1, (255,0,0))
        win.blit(text, (250 - (text.get_width()/2),200))
        pygame.display.update()
        i = 0
        while i<200:
            pygame.time.delay(10)
            i+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i=301
                    pygame.quit()


class projectile(object):
    def __init__(self, x,y,radius, color, facing):
        self.x=x
        self.y=y
        self.radius=radius
        self.facing=facing
        self.color=color
        self.vel=8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)



def redrawGameWindow():
    win.blit(bg,(0,0))
    text= font.render('Score: ' + str(score), 1, (0,0,0))
    win.blit(text, (350,10))
    BigBoy.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y=y
        self.width = width
        self.height = height
        self.end = end
        self.path = (self.x, self.end)
        self.walkCount = 0
        self.vel=3
        self.hitbox = (self.x + 20, self.y, 28, 60)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount +1 >= 33:
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //3], (self.x,self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount //3], (self.x,self.y))
                self.walkCount += 1      
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 125, 0), (self.hitbox[0], self.hitbox[1] - 20, (50 - (5 * (10 - self.health))), 10))
            self.hitbox = (self.x + 20, self.y, 28, 60)
            #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)   

    def move(self):
        if self.vel >0:
            if self.x + self.vel < self.path[1]:
                self.x +=self.vel
            else:
                self.vel *= -1
                self.walkCount=0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel*=-1
                self.walkCount=0

    def hit(self):
        if self.health >0:
            self.health -=1
            print("HIT")
        
        else:
            font2 = pygame.font.SysFont('comicsans', 100)
            text= font2.render("You Won!", 1, (255,0,0))
            win.blit(text, (250 - (text.get_width()/2),200))
            pygame.display.update()
            i = 0
            while i<200:
                pygame.time.delay(10)
                i+=1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i=301
                        pygame.quit()
            self.visible = False
            


# Run until the user asks to quit
font = pygame.font.SysFont('comicsans', 30, True, True)
BigBoy = player(300,410,64,64)
goblin = enemy (100, 410, 64, 64, 450)
bullets=[]
shootloop = 0
running = True
while running:
    clock.tick(27)
    if goblin.visible==True:
        if BigBoy.y < goblin.hitbox[1] + goblin.hitbox[3] and BigBoy.hitbox[1] + BigBoy.hitbox[3] > goblin.hitbox[1]:
            if BigBoy.hitbox[0] + BigBoy.hitbox[2] > goblin.hitbox[0] and BigBoy.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                BigBoy.hit()
                score-=5

    if shootloop > 0:
        shootloop = shootloop + 1
    if shootloop > 3:
        shootloop =0
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                hitSound.play()
                score += 10
                bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x>0: #then bullet shows
            bullet.x+=bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootloop ==0:
        bulletSound.play()
        if BigBoy.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 6:
            bullets.append(projectile(round(BigBoy.x+BigBoy.width//2), round(BigBoy.y + BigBoy.height//2), 6, (0,0,0), facing)) 
        shootloop = 1

    if keys[pygame.K_LEFT] and BigBoy.x>BigBoy.vel:
        BigBoy.x-=BigBoy.vel
        BigBoy.left = True
        BigBoy.right = False
        BigBoy.standing=False
    elif keys[pygame.K_RIGHT] and BigBoy.x< screen_width-BigBoy.width-BigBoy.vel:
        BigBoy.x+=BigBoy.vel
        BigBoy.right=True
        BigBoy.left = False
        BigBoy.standing=False
    else:
        BigBoy.standing=True
        BigBoy.walkCount=0

    if not(BigBoy.isJump): #if we are jumping
        #if keys[pygame.K_DOWN] and y < screen_height-height-vel:
            #y+=vel
        #if keys[pygame.K_UP] and y>vel:
            #y-=vel

        if keys[pygame.K_UP]:
            BigBoy.isJump=True
            BigBoy.right=False
            BigBoy.left=False
            BigBoy.walkCount=0
    else:
        if BigBoy.jumpCount>=-10:
            neg=1
            if BigBoy.jumpCount<0:
                neg=-1
            BigBoy.y-= BigBoy.jumpCount ** 2 * 0.5 * neg
            BigBoy.jumpCount -=1
        else:
            BigBoy.isJump=False
            BigBoy.jumpCount=10

    redrawGameWindow()


# Done! Time to quit.
pygame.quit()