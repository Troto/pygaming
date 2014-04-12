# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://programarcadegames.com/
# http://simpson.edu/computer-science/

import pygame

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)

# This class represents the bar at the bottom that the player controls
class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self,x,y,width,height):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(blue)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        
        
# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):

    # Set speed vector
    change_x=0
    change_y=0

    # Constructor function
    def __init__(self,x,y):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
 
        # Set height, width
        self.image = pygame.Surface([15, 15])
        self.image.fill(white)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
    
    # Change the speed of the player
    def changespeed(self,x,y):
        self.change_x += x
        self.change_y += y
        
    # Find a new position for the player
    def update(self,walls):
        
        # Move left/right
        self.rect.x += self.change_x
        
        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
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
        block_hit_list = pygame.sprite.spritecollide(self, walls, False) 
        for block in block_hit_list:
                
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top 
            else:
                self.rect.top = block.rect.bottom            
  
score = 0
# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])

# Set the title of the window
pygame.display.set_caption('Test')

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Used for converting color maps and such
background = background.convert()

# Fill the screen with a black background
background.fill(black)

# Create the player paddle object
player = Player(50, 50)
all_sprite_list = pygame.sprite.Group()
all_sprite_list.add(player)

# Make the walls. (x_pos, y_pos, width, height)
wall_list = pygame.sprite.Group()

wall = Wall(0,0,10,600)
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(10,0,790,10)
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(10,200,100,10)
wall_list.add(wall)
all_sprite_list.add(wall)

clock = pygame.time.Clock()

done = False

while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-3,0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(3,0)
            elif event.key == pygame.K_UP:
                player.changespeed(0,-3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0,3)
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(3,0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-3,0)
            elif event.key == pygame.K_UP:
                player.changespeed(0,3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0,-3)
 
    player.update(wall_list)
    
    screen.fill(black)
    
    all_sprite_list.draw(screen)

    pygame.display.flip()

    clock.tick(40)
            
pygame.quit()
