#Imports
import pygame, sys
from pygame.locals import *
import random, time

#Initialzing 
pygame.init()



#Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255,0)

#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
#Variables for coins
COINS = 0   #number of collected coins
SPEED_C = 3    #speed for coins

N = 5 
last_speed_increase = 0

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("images/AnimatedStreet.png")

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

#coin sprite class
class Coins(pygame.sprite.Sprite):
    #initialize coins sprite
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/coin.png").convert_alpha()    #load coin image

        # вес монеты (1,2 или 3)
        self.value = random.choice([1, 2, 3])
        # можно визуально отличать
        size = 30 + self.value * 10
        

        self.image = pygame.transform.scale(self.image, (size, size))    #resize the coin image
        self.rect = self.image.get_rect()   #create rectangle for collision and position
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)   #spawn coin at random x position at the top
        

    # Move coin downward    
    def move(self):
        self.rect.move_ip(0,SPEED_C)

        # If coin goes below screen, move it back to top
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

            
            self.value = random.choice([1, 2, 3])
            size = 30 + self.value * 10
            self.image = pygame.transform.scale(self.image, (size, size))
            

    #draw coin on screen    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
 

class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("images/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)

      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("images/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
                  

#Setting up Sprites        
P1 = Player()
E1 = Enemy()
C1 = Coins()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)


#Game Loop
while True:
      
    #Cycles through all events occuring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5
              SPEED_C += 0.5


        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    DISPLAYSURF.blit(background, (0,0))
    # Create text surfaces for score and coins
    scores = font_small.render(str(SCORE), True, BLACK)
    coins = font_small.render(str(COINS), True, YELLOW)
    # Draw score and coins on screen
    DISPLAYSURF.blit(coins, (10,35))
    DISPLAYSURF.blit(scores, (10,10))

    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Coin collection logic
    if pygame.sprite.collide_rect(P1, C1):
        pygame.mixer.Sound('sounds/coin.mp3').play()  #play coin sound
        COINS += C1.value  #coin counter +1

        if COINS >= last_speed_increase + N:
            SPEED += 1
            last_speed_increase += N
        
    
        # move coin to top
        C1.rect.top = 0
        C1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        

        C1.value = random.choice([1, 2, 3])
        size = 30 + C1.value * 10
        C1.image = pygame.transform.scale(C1.image, (size, size))
        

    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound('sounds/crash.wav').play()
          time.sleep(1)
                   
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
          
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()


    

    pygame.display.update()
    FramePerSec.tick(FPS)
