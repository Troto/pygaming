"""
Sprite tutorial exercise

7/4/2014
Author: Toby Sutherland
"""

import pygame
import random

WHITE = [255,255,255]
BLACK = [0,0,0]
RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,255,0]

WW = 1000 #window width
WH = 500 #window height

SW = 10 #Square width
SH = 10 #Square height

class Square(pygame.sprite.Sprite):
    # Width:int Height:int Position:tuple of x and y
    def __init__(self,width,height,position,colour):
        self.velocityx = 0
        self.velocityy = 0
        self.colour = colour
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        
    def move(self):
        self.rect.x += self.velocityx
        self.rect.y += self.velocityy
        if self.rect.y > WH-SH:
            self.rect.y = 0
            
    def update(self):
        self.image.fill(self.colour)        
        self.move()
        
class Player_square(Square):
    
    count = 0
    
    def move(self):
        self.rect.x += self.velocityx
        self.rect.y += self.velocityy
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WW-SW:
            self.rect.x = WW-SW
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > WH-SH:
            self.rect.y = WH-SH

    def add_one(self):
        self.count +=1
    
    def reset(self):
        self.count = 0
    
def main():
    #setup
    pygame.init()
    screen = pygame.display.set_mode((WW,WH))
    font = pygame.font.Font(None,25)
    pacer = pygame.time.Clock()
    pacer.tick(60)
    score = 0
    
    #setup sprites
    block_list = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    
    #player square
    redditor = Player_square(SW,SH,(WW/2-SW/2,WH/2-SH/2),RED)
    all_sprites.add(redditor)
    
    #setup hit squares
    for i in range(20):
        block = Square(SW,SH,[random.randrange(WW-SW),random.randrange(WH-SH)],BLACK)
        block.velocityy = 1
        block_list.add(block)
        all_sprites.add(block)
    
    #main loop
    playing = True
    while playing and score<20:
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    redditor.velocityx += -3
                if event.key == pygame.K_RIGHT:
                    redditor.velocityx += 3
                if event.key == pygame.K_UP:
                    redditor.velocityy += -3
                if event.key == pygame.K_DOWN:
                    redditor.velocityy += 3
         
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    redditor.velocityx += 3
                if event.key == pygame.K_RIGHT:
                    redditor.velocityx += -3
                if event.key == pygame.K_UP:
                    redditor.velocityy += 3
                if event.key == pygame.K_DOWN:
                    redditor.velocityy += -3
                    
        #game logic
        all_sprites.update()

        blocks_hit = pygame.sprite.spritecollide(redditor,block_list,False)
        for block in blocks_hit:
            if block.colour == BLACK:
                score +=1
                block.colour = GREEN
                block.rect.y = 0
                print(score)
        
        #drawing
        screen.fill(WHITE)
        all_sprites.draw(screen)
        
        pygame.display.flip()
        
    pygame.quit()

if __name__ == "__main__":  
    main()
    