import pygame

from spritesheet_functions import *

# These constants define our platform types:
#   Name of file
#   X location of sprite
#   Y location of sprite
#   Width of sprite
#   Height of sprite

grass_left            = (576, 720, 70, 70)
grass_right           = (576, 576, 70, 70)
grass_middle          = (504, 576, 70, 70)
stone_platform_left   = (432, 720, 70, 40)
stone_platform_middle = (648, 648, 70, 40)
stone_platform_right  = (792, 648, 70, 40)  
            
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, sprite_sheet_data ):
        """ Platform constructor. Assumes constructed with user passing in 
            an array of 5 numbers like what's defined at the top of this code. """
        pygame.sprite.Sprite.__init__(self)
        
        sprite_sheet = SpriteSheet("tiles_spritesheet.png")
        # Grab the image for this platform
        self.image = sprite_sheet.getImage(sprite_sheet_data[0],
                                           sprite_sheet_data[1],
                                           sprite_sheet_data[2], 
                                           sprite_sheet_data[3])
        
        self.rect = self.image.get_rect()
 

class MovingPlatform(Platform):
    """ This is a fancier platform that can actually move. """
    change_x = 0
    change_y = 0
     
    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0
    
    level = None
    
    def update(self):
        """ Move the platform. """
        
        # Move left/right
        self.rect.x += self.change_x
        
        # See if we hit anything
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # If we are moving right, set our right side 
            # to the left side of the item we hit
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player.rect.left = self.rect.right

        # Move up/down
        self.rect.y += self.change_y
        
        # Check and see if we hit anything
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:

            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top 
            else:
                self.player.rect.top = self.rect.bottom

        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1
            
        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1         