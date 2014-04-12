import pygame
from math import pi

PI = pi
WHITE = [255,255,255]
BLACK = [0,0,0]
RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,255,0]

pygame.init()

#window width
ww = 700
#window height
wh = 500

screen = pygame.display.set_mode((ww,wh))
font = pygame.font.Font(None,20)

clock = pygame.time.Clock()

playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            
        # User pressed down on a key
        if event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_LEFT:
                x_speed = -3
            if event.key == pygame.K_RIGHT:
                x_speed = 3
            if event.key == pygame.K_UP:
                y_speed = -3
            if event.key == pygame.K_DOWN:
                y_speed = 3
     
        # User let up on a key
        if event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_LEFT:
                x_speed = 0
            if event.key == pygame.K_RIGHT:
                x_speed = 0
            if event.key == pygame.K_UP:
                y_speed = 0
            if event.key == pygame.K_DOWN:
                y_speed = 0        
    
    pos = pygame.mouse.get_pos()
    text = font.render(str(pos),True,WHITE)
    
    screen.fill(BLACK)
    # Draw on the screen a line from (0,0) to (100,100) 
    # 5 pixels wide.
    pygame.draw.line(screen,GREEN,[0,0],[100,100],5)
    # Draw on the screen several lines from (0,10) to (100,110) 
    # 5 pixels wide using a loop
    for y_offset in range(0, 100, 10):
        pygame.draw.line(screen, RED, [0, 10 + y_offset], [100, 110 + y_offset], 5)
 
 
    # Draw a rectangle
    pygame.draw.rect(screen, BLACK, [20, 20, 250, 100], 2)
     
    # Draw an ellipse, using a rectangle as the outside boundaries
    pygame.draw.ellipse(screen, BLACK, [20, 20, 250, 100], 2) 
 
    # Draw an arc as part of an ellipse. 
    # Use radians to determine what angle to draw.
    pygame.draw.arc(screen, BLACK, [20, 220, 250, 200], 0, PI / 2, 2)
    pygame.draw.arc(screen, GREEN, [20, 220, 250, 200], PI / 2, PI, 2)
    pygame.draw.arc(screen, BLUE, [20, 220, 250, 200], PI, 3 * PI / 2, 2)
    pygame.draw.arc(screen, RED, [20, 220, 250, 200], 3 * PI / 2, 2 * PI, 2)
     
    # This draws a triangle using the polygon command	
    pygame.draw.polygon(screen, BLACK, [[100, 100], [0, 200], [200, 200]], 5)    
    
    screen.blit(text,[10,10])
    pygame.display.flip()
    clock.tick(60)
            
pygame.quit()