# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://programarcadegames.com/
# http://simpson.edu/computer-science/
 
# Explanation video: http://youtu.be/qbEEcQXw8aw
 
import pygame
import random
 
# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
red      = ( 255,   0,   0)
 
# This class represents the ball        
# It derives from the "Sprite" class in Pygame
class Block(pygame.sprite.Sprite):
     
    # Constructor. Pass in the color of the block, 
    # and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        
    # Reset position to the top of the screen, at a random x location.
	# Called by update() or the main program loop if there is a collision.
	def reset_pos(self):
        self.rect.y = random.randrange(-300, -20)
        self.rect.x = random.randrange(700-20)        

	# Called each frame
    def update(self):
		# Move block down one pixel
        self.rect.y += 1
        
		# If block is too far down, reset to top of screen.
        if self.rect.y > 410:
            self.reset_pos()

# The player class derives from Block, but overrides the 'update' functionality
# with new a movement function that will move the block with the mouse.
class Player(Block):
    def update(self):
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()
         
        # Fetch the x and y out of the list, 
        # just like we'd fetch letters out of a string.
        # Set the player object to the mouse location
        self.rect.x=pos[0]
        self.rect.y=pos[1]        
        
# Initialize Pygame
pygame.init()
 
# Set the height and width of the screen
screen_width=700
screen_height=400
screen=pygame.display.set_mode([screen_width,screen_height])
 
# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
block_list = pygame.sprite.Group()
 
# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()
 
for i in range(50):
    # This represents a block
    block = Block(black, 20, 15)
 
    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height)
     
    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)
     
     
 
# Create a red player block
player = Player(red, 20, 15)
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
 
    # Clear the screen
    screen.fill(white)
    
	# Calls update() method on every sprite in the list
    all_sprites_list.update()
     
    # See if the player block has collided with anything.
    blocks_hit_list = pygame.sprite.spritecollide(player, block_list, False)  
     
    # Check the list of collisions.
    for block in blocks_hit_list:
        score +=1
        print( score )
		# Reset block to the top of the screen to fall again.
        block.reset_pos() 
         
    # Draw all the spites
    all_sprites_list.draw(screen)
     
    # Limit to 20 frames per second
    clock.tick(20)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
pygame.quit()