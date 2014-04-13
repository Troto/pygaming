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
import math

RESOLUTION = (600,600)

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

sector_size = (180,180)

minimum_horizontal_margin = 10
minimum_vertical_margin = 10



win_limit = 3

NW = 0
NE = 1
SE = 2
SW = 3

DIRECTIONS = [NW,NE,SE,SW]

class Program():
    '''
    This is used as the overarching run class.
    '''
    def __init__(self):
        pygame.init()
        self.event_manager = Event_manager()
        self.pacer = Pacer(self.event_manager)
        self.controller = Controller(self.event_manager)
        self.view = View(self.event_manager)

    def run(self):
        self.game = Game(self.view,self.event_manager)
        self.game.run()
        self.pacer.run()
        pygame.quit()

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
        self.event_manager = event_manager
        self.event_manager.add_listener(self)

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
            self.event_manager.broadcast(event)

    def notify(self,event):
        #checks if received event is a quit event, if so halts main loop.
        if isinstance(event,Quit_event):
            self.keep_going = False

class Controller(Event_manageable):
    def __init__(self,event_manager):
        Event_manageable.__init__(self,event_manager)
        self.event_manager = event_manager

    def notify(self,event):
        if isinstance(event,Tick_event):
            #put input conditions such as keyboard event logic here
            ev = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ev = Quit_event()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    ev = Click_event(pygame.mouse.get_pos())

                self.event_manager.broadcast(ev)

class View(Event_manageable):
    def __init__(self,event_manager):
        Event_manageable.__init__(self,event_manager)
        #initialize display here
        self.font = pygame.font.Font(None,80)
        self.is_message = False
        self.message = None
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BLACK)
        self.screen.blit(self.background, (0,0))
        pygame.display.flip()

        self.back_sprites = pygame.sprite.RenderUpdates()
        self.front_sprites = pygame.sprite.RenderUpdates()
        self.message_sprites = pygame.sprite.RenderUpdates()

    def show_map(self,game_map):
        for component in game_map.components:
            if isinstance(component,Sector):
                Sector_sprite(component,self.back_sprites)
        return self.back_sprites

    def notify(self,event):
        if isinstance(event,Tick_event):
            #draw everything here
            self.back_sprites.clear(self.screen,self.background)
            self.front_sprites.clear(self.screen,self.background)
            self.message_sprites.clear(self.screen,self.background)

            self.back_sprites.update()
            self.front_sprites.update()
            self.message_sprites.update()

            back_dirty_recs = self.back_sprites.draw(self.screen)
            front_dirty_recs = self.front_sprites.draw(self.screen)
            message_dirty_recs = self.message_sprites.draw(self.screen)

            dirty_rects = back_dirty_recs + front_dirty_recs
            pygame.display.update(dirty_rects)
            pygame.display.update(message_dirty_recs)

        elif isinstance(event,Place_event):
            if isinstance(event.piece,Naught):
                piece_sprite = Naught_sprite(event.piece,self.front_sprites)
            elif isinstance(event.piece,Cross):
                piece_sprite = Cross_sprite(event.piece,self.front_sprites)

            piece_sprite.rect.center = event.square.rect.center

        elif isinstance(event,Game_won_event):
            message = "Player " + str(event.winner) + " has won!"
            self.message = Message_sprite(self.font,message,self.message_sprites)
            self.message.rect.center = [RESOLUTION[0]/2,RESOLUTION[1]/2]

class Map():
    def build(self):
        #build map here
        self.components = []

        num_across = RESOLUTION[0]//sector_size[0]
        horizontal_margin = (RESOLUTION[0]-sector_size[0]*num_across)//(num_across+1)
        while horizontal_margin < minimum_horizontal_margin:
            num_across-=1
            horizontal_margin = (RESOLUTION[0]-sector_size[0]*num_across)//(num_across+1)

        if (RESOLUTION[0]-sector_size[0]*num_across - (num_across+1) * horizontal_margin) != 0:
            ew_edge_margin = (RESOLUTION[0]-sector_size[0]*num_across - (num_across-1) * horizontal_margin)/2
        else:
            ew_edge_margin = horizontal_margin

        num_down = RESOLUTION[1]//sector_size[1]
        vertical_margin = (RESOLUTION[1]-sector_size[1]*num_down)//(num_down+1)
        while vertical_margin < minimum_vertical_margin:
            num_down -=1
            vertical_margin = (RESOLUTION[1]-sector_size[1]*num_down)//(num_down+1)

        if (RESOLUTION[1]-sector_size[1]*num_down - (num_down+1) * vertical_margin) != 0:
            ns_edge_margin = (RESOLUTION[1]-sector_size[1]*num_down - (num_down-1) * vertical_margin)/2
        else:
            ns_edge_margin = vertical_margin

        total_sectors = num_across*num_down

        posx = ew_edge_margin
        posy = ns_edge_margin

        while posy < RESOLUTION[1]-ns_edge_margin:
            while posx < RESOLUTION[0]-ew_edge_margin:
                sector = Sector((posx,posy),sector_size,GREEN)
                self.components.append(sector)
                posx += (sector_size[0] + horizontal_margin)
            posx = ew_edge_margin
            posy += (sector_size[1] + vertical_margin)

        #configure neighbour sectors
        #find NW neighbours
        for i in range(num_across,total_sectors):
            if i%num_across != 0:
                self.components[i].neighbours[NW] = self.components[i-num_across-1]

        #find NE neighbours
        for i in range(num_across,total_sectors):
            if i%num_across != num_across-1:
                self.components[i].neighbours[NE] = self.components[i-num_across+1]

        #find SE neighbours
        for i in range(total_sectors-num_across):
            if i%num_across != num_across-1:
                self.components[i].neighbours[SE] = self.components[i+num_across+1]

        #find SW neighbours
        for i in range(total_sectors-num_across):
            if i%num_across != 0:
                self.components[i].neighbours[SW] = self.components[i+num_across-1]

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
        self.piece = None

        self.neighbours = [None for x in range(4)]

    def count_adjacent_pieces(self,direction,piece):
        if type(self.piece) is type(piece):
            if self.neighbours[direction]:
                return self.neighbours[direction].count_adjacent_pieces(direction,piece) + 1
            else:
                return 1
        else:
            return 0

class Sector_sprite(pygame.sprite.Sprite):
    def __init__(self,sector,group=None):
        pygame.sprite.Sprite.__init__(self,group)
        self.image = pygame.Surface(sector.size)
        self.image.fill(sector.colour)
        self.rect = self.image.get_rect()
        self.rect.x = sector.pos[0]
        self.rect.y = sector.pos[1]
        self.sector = sector

class Naught(Static_map_component):
    def __init__(self,size,colour):
        self.size = size
        self.colour = colour

class Naught_sprite(pygame.sprite.Sprite):
    def __init__(self,naught,group=None):
        pygame.sprite.Sprite.__init__(self,group)
        self.image = pygame.Surface((naught.size,naught.size))
        self.image.fill(GREEN)
        half_naught = naught.size//2
        center_x = half_naught
        center_y = half_naught
        radius = half_naught - 5
        iterations = 150
        for i in range(iterations):
                ang = i * 3.14159 * 2 / iterations
                dx = int(math.cos(ang) * radius)
                dy = int(math.sin(ang) * radius)
                x = center_x + dx
                y = center_y + dy
                pygame.draw.circle(self.image, naught.colour, (x, y), 5)

        self.rect = self.image.get_rect()

class Cross(Static_map_component):
    def __init__(self,size,colour):
        self.size = size
        self.colour = colour

class Cross_sprite(pygame.sprite.Sprite):
    def __init__(self,cross,group=None):
        pygame.sprite.Sprite.__init__(self,group)
        self.image = pygame.Surface((cross.size,cross.size))
        self.image.fill(GREEN)
        pygame.draw.line(self.image,cross.colour,(0,0),(cross.size,cross.size),5)
        pygame.draw.line(self.image,cross.colour,(0,cross.size),(cross.size,0),5)
        self.rect = self.image.get_rect()

class Message_sprite(pygame.sprite.Sprite):
    def __init__(self,font,message,group=None):
        pygame.sprite.Sprite.__init__(self,group)
        self.image = pygame.Surface((600,200))
        self.image = self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        self.text = font.render(message,True,WHITE)
        self.image.blit(self.text,(60,60))
        self.rect = self.image.get_rect()


class Dynamic_map_component(Map_component,Event_manageable):
    pass

class Game(Event_manageable):
    def __init__(self,view,event_manager):
        Event_manageable.__init__(self,event_manager)
        self.view = view
        self.game_map = Map()
        self.active_player = 1
        self.event_manager
        self.playable_squares = []

    def run(self):
        self.game_map.build()
        self.playable_squares = self.view.show_map(self.game_map)

    def notify(self,event):
        if isinstance(event,Click_event):
            clicked_square = None
            for square in self.playable_squares:
                if square.rect.collidepoint(event.pos):
                    clicked_square = square
                    self.playable_squares.remove(clicked_square)
                    break
            if clicked_square:
                if self.active_player == 1:
                    piece = Naught(sector_size[0],RED)
                    self.active_player = 2
                else:
                    piece = Cross(sector_size[0],BLUE)
                    self.active_player = 1
                clicked_square.sector.piece = piece
                self.event_manager.broadcast(Place_event(piece,clicked_square))
                self.check_for_winner(clicked_square,piece)

    def check_for_winner(self,clicked_square,piece):
        results = [0 for x in range(6)]
        for direction in DIRECTIONS:
            if clicked_square.sector.neighbours[direction]:
                results[direction] = clicked_square.sector.neighbours[direction].count_adjacent_pieces(direction,piece)
            else:
                results[direction] = 0

        results[4] = results[NW] + results[SE]
        results[5] = results[NE] + results[SW]
        for i in results:
            if i == win_limit-1:
                if self.active_player == 1:
                    winner = 2
                else:
                    winner = 1
                self.event_manager.broadcast(Game_won_event(winner))


class Player(Event_manageable):
    def __init__(self,event_manager):
        Event_manageable.__init__(self,event_manager)
        #define player attributes such as score etc here

class Event():
    pass

class Tick_event(Event):
    pass

class Quit_event(Event):
    pass

class Click_event(Event):
    def __init__(self,cursor_position):
        self.pos = cursor_position

class Place_event(Event):
    def __init__(self,piece,square):
        self.piece = piece
        self.square = square

class Game_won_event(Event):
    def __init__(self,winner):
        self.winner = winner

def main():
    program = Program()
    program.run()

if __name__ == "__main__":
    main()