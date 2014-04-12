# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://programarcadegames.com/
# http://simpson.edu/computer-science/

# Cat images may be downloaded from 
# http://ProgramArcadeGames.com/python_examples/cat_pngs.zip

import pygame

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
red      = ( 255,   0,   0)
        
class Player(pygame.sprite.Sprite):
    
    # -- Attributes
    # Set speed vector
    change_x=0
    change_y=0    
    
    # This is a frame counter used to determing which image to draw
    frame = 0
    
    # Constructor.
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 

        # List that the cat images will be saved in.
        self.images=[]
        # Load all the cat images, from cat1.png to cat8.png.
        for i in range(1,9):
            img = pygame.image.load("cat"+str(i)+".png").convert()
            img.set_colorkey(white)
            self.images.append(img)
        
        # By default, use image 0
        self.image = self.images[0]

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        
    # Change the speed of the player
    def changespeed(self,x,y):
        self.change_x+=x
        self.change_y+=y
         
    # Find a new position for the player
    def update(self):
        # Update position based on speed
        self.rect.y += self.change_y
        self.rect.x += self.change_x
        
        # If we are moving right to left
        if self.change_x < 0:
            # Update our frame counter
            self.frame += 1
            
            # We go from 0...3. If we are above image 3, reset to 0
            # Multiply by 4 because we flip the image every 4 frames
            if self.frame > 3*4:
                self.frame = 0
                
            # Grab the image, do floor division by 4 because we flip
            # every 4 frames. 
            # Frames 0...3 -> image[0]
            # Frames 4...7 -> image[1]
            # etc.
            self.image = self.images[self.frame//4]

        # Move left to right. About the same as before, but use
        # images 4...7 instead of 0...3. Note that we add 4 in the last
        # line to do this.
        if self.change_x > 0:
            self.frame += 1
            if self.frame > 3*4:
                self.frame = 0
            self.image = self.images[self.frame//4+4]
        
# Initialize Pygame
pygame.init()

# Set the height and width of the screen
screen_width=700
screen_height=400
screen=pygame.display.set_mode([screen_width,screen_height])

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# Create a red player block
player = Player()
all_sprites_list.add(player)

#Loop until the user clicks the close button.
done=False

# Used to manage how fast the screen updates
clock=pygame.time.Clock()

score = 0

# -------- Main Program Loop -----------
while done==False:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
            # Set the speed based on the key pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-3,0)
            if event.key == pygame.K_RIGHT:
                player.changespeed(3,0)
            if event.key == pygame.K_UP:
                player.changespeed(0,-3)
            if event.key == pygame.K_DOWN:
                player.changespeed(0,3)
                 
        # Reset speed when key goes up      
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(3,0)
            if event.key == pygame.K_RIGHT:
                player.changespeed(-3,0)
            if event.key == pygame.K_UP:
                player.changespeed(0,3)
            if event.key == pygame.K_DOWN:
                player.changespeed(0,-3)
    # Clear the screen
    screen.fill(white)

    player.update()

    # Draw all the spites
    all_sprites_list.draw(screen)
    
    # Limit to 20 frames per second
    clock.tick(20)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()
