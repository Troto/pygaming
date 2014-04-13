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


class Program():
    '''
    This is used as the overarching run class. This is only a generic
    implementation and requires specific additions such as menus.
    '''
    def __init__(self):
        em = Event_manager()
        pacer = Pacer(em)
        controller = Controller(em)
        view = View(em)

    def run(self):
        game = Game(em)
        game.run()
        pacer.run()

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
        Event_manageable.__init__(self)

        #initialize a timer here
        self.keep_going = True
        self.run()

    def run(self):
        #this is the while loop to limit
        while self.keep_going:
            event = Tick_event()
            self.em.broadcast(event)

    def notify(self,event):
        #checks if received event is a quit event, if so halts main loop.
        if isinstance(event,Quit_event):
            keep_going = False

class View(Event_manageable):
    def __init__(self):
        Event_manageable.__init__(self)
        #initialize display here

    def show_map(self,game_map):
        pass

    def show_avatar(self,avatar):
        pass

    def move_avatar(self,avatar):
        pass

    def notify(self,event):
        if isinstance(event,Tick_event):
            #draw everything here
            #use groups back_sprites and front_sprites
            pass

        elif isinstance(event,Move_avatar_event):
            avatar = event.avatar
            self.move_avatar(avatar)

class Controller(Event_manageable):
    def __init__(self):
        Event_manageable.__init__(self)

    def notify(self,event):
        if isinstance(event,Tick_event):
            #put input conditions such as keyboard event logic here
            pass

class Map():
    def build(self):
        #build map here
        self.components = []
        #return the map
        pass

class Map_component():
    pass

class Static_map_component(Map_component):
    pass

class Dynamic_map_component(Map_component,Event_manageable):
    def __init__(self):
        Event_manageable.__init__(self)

class Game(Event_manageable):
    def __init__(self,view):
        Event_manageable.__init__(self)
        self.view = view
        game_map = Map()
        player = Player(em)

    def run(self):
        game_map.build()
        self.view.show_map(game_map)
        for avatar in player.avatars:
            self.view.show_avatar(avatar)

class Player(Event_manageable):
    def __init__(self):
        Event_manageable.__init__(self)
        #define player attributes such as score etc here
        avatars = [Avatar(em)]

class Avatar(Event_manageable):
    def __init__(self):
        Event_manageable.__init__(self)
        #define avatar atrributes such as speed and position here

    def move(self,direction):
        #does not have to be direction, it can be whatever movement system you
        #like such as a vector or new coords

        #have moment calculation and logic here
        pass

    def notify(self,event):
        if isinstance(event,Move_avatar_event):
            self.move(event.direction)

class Event():
    def __init__(self):
        self.name == "Generic Event"

class Tick_event(Event):
    def __init__(self):
        self.name == "Tick Event"

class Quit_event(Event):
    def __init__(self):
        self.name == "Quit Event"

class Move_avatar_event(Event):
    def __init__(self,direction):
        self.name == "Move Avatar Event"
        self.direction = direction

# Here define any other events that you will use