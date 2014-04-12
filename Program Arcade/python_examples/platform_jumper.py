# Sample Python/Pygame Programs 
# Simpson College Computer Science 
# http://programarcadegames.com/
# http://simpson.edu/computer-science/

# Explanation video: http://youtu.be/G61EhqqtzlA

import pygame
import random
  
# Define some colors 
black    = (   0,   0,   0) 
white    = ( 255, 255, 255) 
red      = ( 255,   0,   0)

# This class represents the platform we jump on
class Platform (pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

# This class represents the bar at the bottom that the player controls 
class Player(pygame.sprite.Sprite): 
  
    # -- Attributes 
    # Set speed vector of player
    change_x = 0
    change_y = 0

    # Set to true if it is ok to jump
    jump_ok = True

    # Count of frames since the player 
    # collided against something. Used to prevent jumping
    # when we haven't hit anything.
    frame_since_collision = 0
    
    # -- Methods 
    # Constructor function 
    def __init__(self, x, y): 
        # Call the parent's constructor 
        pygame.sprite.Sprite.__init__(self) 
          
        # Set height, width 
        self.image = pygame.Surface([15, 15]) 
        self.image.fill(red)
  
        # Make our top-left corner the passed-in location. 
        self.rect = self.image.get_rect() 
        self.rect.x = x
        self.rect.y = y
      
    # Find a new position for the player 
    def update(self,blocks): 

        # Move left/right
        self.rect.x += self.change_x
        
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, blocks, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y
        
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, blocks, False) 
        for block in block_hit_list:

            # We hit something below us. Set the boolean to flag that we can jump
            if self.change_y > 0:
                self.jump_ok = True

            # Keep track of the last time we hit something
            self.frame_since_collision = 0

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top 
            else:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

        # If we haven't hit anything in a while, allow us jump
        if self.frame_since_collision > 3:
            self.jump_ok = False

        # Increment frame counter
        self.frame_since_collision += 1

    # Calculate effect of gravity.
    def calc_grav(self):
        self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= 485 and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = 485
            self.frame_since_collision = 0
            self.jump_ok = True

    # Called when user hits 'jump' button
    def jump(self,blocks):
        
        # If it is ok to jump, set our speed upwards
        if self.jump_ok:
            self.change_y = -8
        
# Create platforms
def create_level1(block_list,all_sprites_list):

    # 7 blocks
    for i in range(7):
        block = Platform(white, 100, 20)
        # Set x and y based on block number
        block.rect.x = 75 * i
        block.rect.y = 75 * i

        block_list.add(block)
        all_sprites_list.add(block)

# Initialize the window
pygame.init() 
   
# Set the height and width of the screen 
size=[700,500] 
screen=pygame.display.set_mode(size) 
  
pygame.display.set_caption("JUMP!") 

# Main program, create the blocks 
block_list = pygame.sprite.Group()

all_sprites_list = pygame.sprite.Group()

create_level1(block_list,all_sprites_list)
  
player = Player(20, 15)

player.rect.x = 340
player.rect.y = 485
    
all_sprites_list.add(player)

#Loop until the user clicks the close button. 
done = False
  
# Used to manage how fast the screen updates 
clock = pygame.time.Clock() 
  
# -------- Main Program Loop ----------- 
while not done: 
    
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.change_x = -6
            if event.key == pygame.K_RIGHT:
                player.change_x = 6
            if event.key == pygame.K_UP:
                player.jump(block_list)
                
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_LEFT: 
                player.change_x = 0
            if event.key == pygame.K_RIGHT: 
                player.change_x = 0

    # --- Game Logic    
    # Wrap player around the screen if they go too far left/right
    if player.rect.x >= 700:
        player.rect.x = -15

    if player.rect.x <= -20:
        player.rect.x = 699

    player.calc_grav()
    player.update(block_list)
    block_list.update()
    
    # --- Draw Frame
    # Set the screen background 
    screen.fill(black)
  
    all_sprites_list.draw(screen)
      
    # Go ahead and update the screen with what we've drawn. 
    pygame.display.flip() 
      
    # Limit to 20 frames per second 
    clock.tick(40) 
  
# Be IDLE friendly. If you forget this line, the program will 'hang' 
# on exit. 
pygame.quit ()

