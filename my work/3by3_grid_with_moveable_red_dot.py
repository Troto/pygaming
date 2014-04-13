"""
Implementation of a generic observer pattern for future use with games.

Structure is as follows:

Classes:
Program - The overarching class
Event_manager - Handler class for all events
Event - Generic superclass for all events
[Events] - Various event classes
Event_manageable - Super class for classes that will use the event manager
Pacer - The tick timer class
Controller - Class for handling player input (keyboard/mouse/joystick etc)
View - The display class
Map - The structure class for all non-player objects
Map_component - A generic class that represents individual parts of a map
Game - The game class for each run through of the game
Player - The class for the player attributes
Avatar - The player's object class

Simple stucture outline -

Program uses:
    Event_manager
    Pacer
    Controller
    View
    Game

Event_manager uses:
    Event

Game uses:
    Map
    Player

Player uses:
    Avatar

Created: 12/4/2014
Last edited:
Author: Toby Sutherland
"""
import pygame

RESOLUTION = (700,700)

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

sector_size = (200,200)
avatar_radius = 50

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class Program():
    '''
    This is used as the overarching run class.
    '''
    def __init__(self):
        pygame.init()
        self.em = Event_manager()
        self.pacer = Pacer(self.em)
        self.controller = Controller(self.em)
        self.view = View(self.em)

    def run(self):
        self.game = Game(self.view,self.em)
        self.game.run()
        self.pacer.run()

class Event_manager():
    '''
    This is the observer that notifies the appropriate objects of events.
    It uses a weak key dictionary so that if an listener no longer exists the
    reference will be caught by garbage collection.
    '''
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()

    def add_listener(self,listener):
        self.listeners[listener] = 1

    def remove_listener(self,listener):
        if listener in self.listeners:
            del self.listeners[listener]

    def broadcast(self,event):
        for listener in self.listeners:
            listener.notify(event)

class Event_manageable():
    def __init__(self,event_manager):
        self.em = event_manager
        self.em.add_listener(self)

    def notify(self,event):
        pass

class Pacer(Event_manageable):
    '''
    This class is where you will implement a timer to for limiting your tick
    rate. Left as is, it will run as fast as it can. You should implement a pacer
    so your game doesn't become a CPU guzzling abomination.
    '''
    def __init__(self,event_manager):
        Event_manageable.__init__(self,event_manager)
        self.clock = pygame.time.Clock()

        #initialize a timer here
        self.keep_going = True

    def run(self):
        #this is the while loop to limit
        while self.keep_going:
            self.clock.tick(60)
            event = Tick_event()
            self.em.broadcast(event)

    def notify(self,event):
        #checks if received event is a quit event, if so halts main loop.
        if isinstance(event,Quit_event):
            self.keep_going = False

class Controller(Event_manageable):
    def __init__(self,em):
        Event_manageable.__init__(self,em)
        self.em = em

    def notify(self,event):
        if isinstance(event,Tick_event):
            #put input conditions such as keyboard event logic here
            ev = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ev = Quit_event()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        ev = Move_avatar_event(UP)
                    if event.key == pygame.K_DOWN:
                        ev = Move_avatar_event(DOWN)
                    if event.key == pygame.K_LEFT:
                        ev = Move_avatar_event(LEFT)
                    if event.key == pygame.K_RIGHT:
                        ev = Move_avatar_event(RIGHT)
            if ev:
                self.em.broadcast(ev)

class View(Event_manageable):
    def __init__(self,event_manager):
        Event_manageable.__init__(self,event_manager)
        #initialize display here
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BLACK)
        self.screen.blit(self.background, (0,0))
        pygame.display.flip()

        self.back_sprites = pygame.sprite.RenderUpdates()
        self.front_sprites = pygame.sprite.RenderUpdates()

    def show_map(self,game_map):
        for component in game_map.components:
            if isinstance(component,Sector):
                Sector_sprite(component,self.back_sprites)

    def move_avatar(self,avatar):
        avatar_sprite = self.get_avatar_sprite(avatar)
        sector_sprite = self.get_sector_sprite(avatar.sector)
        avatar_sprite.rect.center = sector_sprite.rect.center

    def get_avatar_sprite(self,avatar):
        for s in self.front_sprites:
            return s
        else:
            return Avatar_sprite(avatar,self.front_sprites)

    def get_sector_sprite(self,sector):
        for s in self.back_sprites:
            if s.sector == sector:
                return s

    def notify(self,event):
        if isinstance(event,Tick_event):
            #draw everything here
            self.back_sprites.clear(self.screen,self.background)
            self.front_sprites.clear(self.screen,self.background)

            self.back_sprites.update()
            self.front_sprites.update()

            back_dirty_recs = self.back_sprites.draw(self.screen)
            front_dirty_recs = self.front_sprites.draw(self.screen)

            dirty_rects = back_dirty_recs + front_dirty_recs
            pygame.display.update(dirty_rects)

        elif isinstance(event,Move_avatar_sprite_event):
            avatar = event.avatar
            self.move_avatar(avatar)

class Map():
    def build(self):
        #build map here
        self.components = []

        num_across = RESOLUTION[0]//sector_size[0]
        num_down = RESOLUTION[1]//sector_size[1]
        total_sectors = num_across*num_down

        horizontal_margin = (RESOLUTION[0]-sector_size[0]*num_across)//(num_across+1)
        vertical_margin = (RESOLUTION[1]-sector_size[1]*num_down)//(num_down+1)

        posx = horizontal_margin
        posy = vertical_margin

        while posy < RESOLUTION[1]:
            while posx < RESOLUTION[0]:
                sector = Sector((posx,posy),sector_size,GREEN)
                self.components.append(sector)
                posx += (sector_size[0] + horizontal_margin)
            posx = horizontal_margin
            posy += (sector_size[1] + vertical_margin)

        #configure neighbour sectors
        #find up neighbours
        for i in range(num_across,total_sectors):
            self.components[i].neighbours[UP] = self.components[i-num_across]
        #find right neighbours
        for i in range(total_sectors):
            if i%num_across != num_across-1:
                self.components[i].neighbours[RIGHT] = self.components[i+1]
        #find down neighbours
        for i in range(total_sectors-num_across):
            self.components[i].neighbours[DOWN] = self.components[i+num_across]
        #find left neighbours
        for i in range(total_sectors):
            if i%num_across != 0:
                self.components[i].neighbours[LEFT] = self.components[i-1]

        #return the map
        return self.components

class Map_component():
    pass

class Static_map_component(Map_component):
    pass

class Sector(Static_map_component):
    def __init__(self,pos,size,colour):
        self.pos = pos
        self.size = size
        self.colour = colour

        self.neighbours = [None for x in range(4)]

    def has_neighbour(self,direction):
        return self.neighbours.direction

class Sector_sprite(pygame.sprite.Sprite):
    def __init__(self,sector,group=None):
        pygame.sprite.Sprite.__init__(self,group)
        self.image = pygame.Surface(sector.size)
        self.image.fill(sector.colour)
        self.rect = self.image.get_rect()
        self.rect.x = sector.pos[0]
        self.rect.y = sector.pos[1]
        self.sector = sector

class Dynamic_map_component(Map_component,Event_manageable):
    def __init__(self):
        Event_manageable.__init__(self)

class Game(Event_manageable):
    def __init__(self,view,event_manager):
        Event_manageable.__init__(self,event_manager)
        self.view = view
        self.game_map = Map()
        self.player = Player(event_manager)

    def run(self):
        self.game_map.build()
        self.view.show_map(self.game_map)
        for avatar in self.player.avatars:
            avatar.place(self.game_map.components[0])

class Player(Event_manageable):
    def __init__(self,em):
        Event_manageable.__init__(self,em)
        #define player attributes such as score etc here
        self.avatars = [Avatar(em)]

class Avatar(Event_manageable):
    def __init__(self,em):
        Event_manageable.__init__(self,em)
        #define avatar atrributes such as speed and position here
        self.sector = None
        self.em = em

    def place(self,sector):
        self.sector = sector
        self.em.broadcast(Move_avatar_sprite_event(self))

    def move(self,direction):
        if self.sector.neighbours[direction]:
            self.sector = self.sector.neighbours[direction]
            self.em.broadcast(Move_avatar_sprite_event(self))

    def notify(self,event):
        if isinstance(event,Move_avatar_event):
            self.move(event.direction)

class Avatar_sprite(pygame.sprite.Sprite):
    def __init__(self,avatar,group=None):
        pygame.sprite.Sprite.__init__(self,group)
        self.image = pygame.Surface((avatar_radius*2,avatar_radius*2))
        self.image = self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        pygame.draw.circle(self.image,RED,(avatar_radius,avatar_radius),avatar_radius)
        self.rect = self.image.get_rect()
        self.avatar = avatar

class Event():
    def __init__(self):
        self.name = "Generic Event"

class Tick_event(Event):
    def __init__(self):
        self.name = "Tick Event"

class Quit_event(Event):
    def __init__(self):
        self.name = "Quit Event"

class Move_avatar_event(Event):
    def __init__(self,direction):
        self.name = "Move Avatar Event"
        self.direction = direction

class Move_avatar_sprite_event(Event):
    def __init__(self,avatar):
        self.name = "Move Avatar Sprite Event"
        self.avatar = avatar

# Here define any other events that you will use
def main():
    program = Program()
    program.run()

if __name__ == "__main__":
    main()