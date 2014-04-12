# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://programarcadegames.com/
# http://simpson.edu/computer-science/

import pygame

black = (0,0,0)
white = (255,255,255)
       
# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self,x,y):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
 
        # Set height, width
        self.image = pygame.Surface([15, 15])
        self.image.fill(black)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    # Find a new position for the player
    def update(self):
        self.rect.x += self.change_y
        self.rect.y += self.change_x


# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])

# Set the title of the window
pygame.display.set_caption('Test')

# Create the player paddle object
player = Player( 50,50 )
all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(player)

clock = pygame.time.Clock()
done = False

while done == False:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.rect.x -= player.rect.width
            elif event.key == pygame.K_RIGHT:
                player.rect.x += player.rect.width
            elif event.key == pygame.K_UP:
                player.rect.y -= player.rect.height
            elif event.key == pygame.K_DOWN:
                player.rect.y += player.rect.height
                
    # -- Draw everything
    # Clear screen
    screen.fill(white)
    
    # Draw sprites  
    all_sprites_list.draw(screen)
    
    # Flip screen   
    pygame.display.flip()
    
    # Pause
    clock.tick(40)  
                
pygame.quit()
