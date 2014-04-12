# Sample Python/Pygame Programs 
# Simpson College Computer Science 
# http://programarcadegames.com/
# http://simpson.edu/computer-science/

# Explanation video:

import pygame
import random
  
# Define some colors 
black    = (   0,   0,   0) 
white    = ( 255, 255, 255) 
red      = ( 255,   0,   0)
blue     = (   0,   0, 255)

# This class represents the platform we jump on
class Platform (pygame.sprite.Sprite):
    
    player = None

    change_x = 0
    change_y = 0
    
    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0
    
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        
    def update(self):
        # Move left/right
        self.rect.x += self.change_x
        
        # See if we hit anything
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # If we are moving right, set our right side to the left side of the item we hit
            if self.change_x < 0:
                player.rect.right = self.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                player.rect.left = self.rect.right

        # Move up/down
        self.rect.y += self.change_y
        
        # Check and see if we hit anything
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:

            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0:
                player.rect.bottom = self.rect.top 
            else:
                player.rect.top = self.rect.bottom

        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1
            
        if self.rect.x < self.boundary_left or self.rect.x > self.boundary_right:
            self.change_x *= -1
            

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
    
    block_list = None
    
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
    def update(self): 
        self.calc_grav()
        
        # Move left/right
        self.rect.x += self.change_x
        
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.block_list, False)
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
        block_hit_list = pygame.sprite.spritecollide(self, block_list, False) 
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
            
            self.rect.x += block.change_x

        # If we haven't hit anything in a while, allow us jump
        if self.frame_since_collision > 6:
            self.jump_ok = False

        # Increment frame counter
        self.frame_since_collision += 1

    # Calculate effect of gravity.
    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
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
def create_level1(block_list,all_sprites_list,player):

    block = Platform(white, 100, 20)
    block.rect.x = 50
    block.rect.y = 350
    block.change_y = 1
    block.boundary_bottom = 485
    block.boundary_top = 300    
    block.player = player
    block_list.add(block)
    all_sprites_list.add(block)

    block = Platform(blue, 100, 20)
    block.rect.x = 250
    block.rect.y = 480
    block.change_x = 1
    block.boundary_left = 225
    block.boundary_right = 400    
    block.player = player
    block_list.add(block)
    all_sprites_list.add(block)
    
    block = Platform(white, 100, 20)
    block.rect.x = 550
    block.rect.y = 150
    block.change_y = -1
    block.boundary_bottom = 300
    block.boundary_top = 100    
    block.player = player
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

# Create player  
player = Player(20, 15)

player.block_list = block_list

player.rect.x = 340
player.rect.y = 485
    
all_sprites_list.add(player)

# Create level
create_level1(block_list,all_sprites_list,player)

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

    all_sprites_list.update()
    
    # --- Draw Frame
    # Set the screen background 
    screen.fill(black)
  
    all_sprites_list.draw(screen)
      
    # Go ahead and update the screen with what we've drawn. 
    pygame.display.flip() 
      
    # Limit to 20 frames per second 
    clock.tick(60) 
  
# Be IDLE friendly. If you forget this line, the program will 'hang' 
# on exit. 
pygame.quit ()

