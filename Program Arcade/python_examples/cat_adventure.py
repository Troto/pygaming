# Sample Python/Pygame Programs
# Simpson College Computer Science
# http://programarcadegames.com/
# http://simpson.edu/computer-science/
  
# Cat images may be downloaded from 
# http://ProgramArcadeGames.com/python_examples/cat_pngs.zip

import pygame
  
black = (0,0,0)
white = (255,255,255)

class GraphicWall(pygame.sprite.Sprite):
    
    def setGraphic(self,tilex,tiley,tilewidth,tileheight,x,y,width,height):
        myimage = pygame.image.load("terrain_atlas.png").convert()

        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        
        for row in range(height//tileheight+1):
            for column in range(width//tilewidth+1):
                self.image.blit(myimage,(column*tilewidth,row*tileheight),(tilex,tiley,tilewidth,tileheight))
        
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x  
        self.image.set_colorkey(black)
        
    def setGraphic2(self,tilex,tiley,x,y,width,height):
        myimage = pygame.image.load("terrain_atlas.png").convert()

        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        
        self.image.blit(myimage,(0,0),(tilex,tiley,32,32))
        for column in range(width//32-2):
            self.image.blit(myimage,((column+1)*32,0),(tilex+32,tiley,32,32))
        self.image.blit(myimage,( (width//32-1)*32,0),(tilex+64,tiley,32,32))        
        
        for row in range(height//32+1):
            self.image.blit(myimage,(0,(row+1)*32),(tilex,tiley+32,32,32))
            for column in range(width//32+1):
                self.image.blit(myimage,((column+1)*32,(row+1)*32),(tilex+32,tiley+32,32,32))
            self.image.blit(myimage,((width//32-1)*32,(row+1)*32),(tilex+64,tiley+32,32,32))

        self.image.blit(myimage,(0,(height//32-1)*32),(tilex,tiley+64,32,32))
        for column in range(width//32-2):
            self.image.blit(myimage,((column+1)*32,(height//32-1)*32),(tilex+32,tiley+64,32,32))
        self.image.blit(myimage,( (width//32-1)*32,(height//32-1)*32),(tilex+64,tiley+64,32,32))        
            
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x  
        self.image.set_colorkey(black)        
        
# This class represents the bar at the bottom that the player controls
class StoneWall(GraphicWall):
    # Constructor function
    def __init__(self,x,y,width,height):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        tilex=32*16
        tiley=32*29
        self.setGraphic2(tilex,tiley,x,y,width,height)

class StoneWall2(GraphicWall):
    # Constructor function
    def __init__(self,x,y,width,height):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        tilex=32*16
        tiley=32*23
        self.setGraphic2(tilex,tiley,x,y,width,height)


# This class represents the bar at the bottom that the player controls
class Tree1(GraphicWall):
    # Constructor function
    def __init__(self,x,y):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        width=64
        height=160
        tilewidth=64
        tileheight=160
        tilex=32*30
        tiley=32*0
        self.setGraphic(tilex,tiley,tilewidth,tileheight,x,y,width,height)


# This class represents the bar at the bottom that the player controls
class Tree2(GraphicWall):
    # Constructor function
    def __init__(self,x,y):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        width=96
        height=128
        tilewidth=96
        tileheight=128
        tilex=32*29
        tiley=32*28
        self.setGraphic(tilex,tiley,tilewidth,tileheight,x,y,width,height)
        
class WaterWall(GraphicWall):
    # Constructor function
    def __init__(self,x,y,width,height):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)


        tilex=32*9
        tiley=32*11
        self.setGraphic2(tilex,tiley,x,y,width,height)

class GardenWall(GraphicWall):
    # Constructor function
    def __init__(self,x,y,width,height):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        tilex=32*5
        tiley=32*17
        self.setGraphic2(tilex,tiley,x,y,width,height)

class TallGrass(GraphicWall):
    # Constructor function
    def __init__(self,x,y,width,height):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        tilex=32*0
        tiley=32*22
        self.setGraphic2(tilex,tiley,x,y,width,height)

class FallGrass(GraphicWall):
    # Constructor function
    def __init__(self,x,y,width,height):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        tilex=32*0
        tiley=32*28
        self.setGraphic2(tilex,tiley,x,y,width,height)       
        
class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self,x,y,width,height, color):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
  
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
  
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
          
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
    def update(self, walls):
        
        # Get the old position, in case we need to go back to it
        old_x=self.rect.x
        new_x=old_x+self.change_x
        self.rect.x = new_x
          
        # Did this update cause us to hit a wall?
        collide = pygame.sprite.spritecollide(self, walls, False)
        if collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.x=old_x
  
        old_y=self.rect.y
        new_y=old_y+self.change_y
        self.rect.y = new_y
          
        # Did this update cause us to hit a wall?
        collide = pygame.sprite.spritecollide(self, walls, False)
        if collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.y=old_y        
        

         
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
          

# This creates all the walls in room 1
def setupRoomOne():
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list=pygame.sprite.Group()
     
    wall=StoneWall(390,80, 96, 448)
    wall_list.add(wall)
    wall=StoneWall2(600,0, 96, 320)
    wall_list.add(wall)
    
    # return our new list
    return wall_list
 
# This creates all the walls in room 2
def setupRoomTwo():
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list=pygame.sprite.Group()
     
    wall=Tree1(100,100)
    wall_list.add(wall)
    wall=Tree2(300,250)
    wall_list.add(wall)
    wall=TallGrass(100,400,64,160)
    wall_list.add(wall)
    wall=Tree1(500,160)
    wall_list.add(wall)
    wall=FallGrass(600,128,192,160)
    wall_list.add(wall)
    wall=Tree1(700,350)
    wall_list.add(wall)
         
    return wall_list
 
# This creates all the walls in room 3
def setupRoomThree():
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list=pygame.sprite.Group()
     
    wall=WaterWall(64,64,192,192)
    wall_list.add(wall)
    wall=GardenWall(128,325,256,192)
    wall_list.add(wall)
    wall=Tree1(520,256)
    wall_list.add(wall)
 
    return wall_list
 
score = 0
# Call this function so the Pygame library can initialize itself
pygame.init()
  
# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])
  
# Set the title of the window
pygame.display.set_caption("Cat Adventure")
  
# Create a surface we can draw on
background = pygame.Surface(screen.get_size())
  
# Used for converting color maps and such
background = background.convert()
  
# Fill the screen with a black background
background.fill(black)
  
# Create the player paddle object
player = Player( )
player.rect.x=50
player.rect.y=50
movingsprites = pygame.sprite.Group()
movingsprites.add(player)
  
current_room = 1
wall_list = setupRoomOne()
 
clock = pygame.time.Clock()
  
done = False
  
while done == False:
    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
  
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-5,0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(5,0)
            elif event.key == pygame.K_UP:
                player.changespeed(0,-5)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0,5)
                  
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(5,0)
            if event.key == pygame.K_RIGHT:
                player.changespeed(-5,0)
            if event.key == pygame.K_UP:
                player.changespeed(0,5)
            if event.key == pygame.K_DOWN:
                player.changespeed(0,-5)
    # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
 
 
    # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
    player.update(wall_list)
    if player.rect.x < -15:
        if current_room == 1:
            wall_list = setupRoomThree()
            current_room = 3
            player.rect.x = 790
        elif current_room == 3:
            wall_list = setupRoomTwo()
            player.rect.x = 790
            current_room = 2
        else:
            wall_list = setupRoomOne()
            player.rect.x = 790
            current_room = 1
             
    if player.rect.x > 801:
        if current_room == 1:
            wall_list = setupRoomTwo()
            current_room = 2
            player.rect.x = 0
        elif current_room == 2:
            wall_list = setupRoomThree()
            current_room = 3
            player.rect.x = 0
        else:
            wall_list = setupRoomOne()
            current_room = 1
            player.rect.x = 0
 
 
    # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
 
                  
    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
    screen.fill( (47,129,54) )
      
    movingsprites.draw(screen)
    wall_list.draw(screen)
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
     
    pygame.display.flip()
  
    clock.tick(40)
              
pygame.quit()