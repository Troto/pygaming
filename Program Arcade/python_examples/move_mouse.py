# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://programarcadegames.com/
# http://simpson.edu/computer-science/
 
import pygame
 
# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)

def draw_stick_figure(screen,x,y):
    # Head
    pygame.draw.ellipse(screen,black,[1+x,y,10,10],0)
 
    # Legs
    pygame.draw.line(screen,black,[5+x,17+y],[10+x,27+y],2)
    pygame.draw.line(screen,black,[5+x,17+y],[x,27+y],2)
 
    # Body
    pygame.draw.line(screen,red,[5+x,17+y],[5+x,7+y],2)
 
    # Arms
    pygame.draw.line(screen,red,[5+x,7+y],[9+x,17+y],2)
    pygame.draw.line(screen,red,[5+x,7+y],[1+x,17+y],2)
    
pygame.init()
  
# Set the width and height of the screen [width,height]
size = [700,500]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
#Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Hide the mouse cursor
pygame.mouse.set_visible(0)

# -------- Main Program Loop -----------
while done == False:
    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
    # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

    # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT

    # Call draw stick figure function
    pos = pygame.mouse.get_pos()
    x = pos[0]
    y = pos[1]

    # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT    

    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
     
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(white)
    draw_stick_figure(screen,x,y)  
    
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
     
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit to 20 frames per second
    clock.tick(20)
     
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()