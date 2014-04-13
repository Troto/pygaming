import random

class ball():
    def __init__(self,diameter,colour,start_position,max_velocityx,velocityy):
        self.diameter = diameter
        self.colour = colour
        self.start_position = start_position
        self.max_velocityx = max_velocityx
        self.velocityy = velocityy
        self.reset_ball()
        
    def add_velocityx(self,velocity):
        self.velocityx += velocity
        if self.velocityx > self.max_velocityx:
            self.velocityx = self.max_velocityx
        elif self.velocityx < -self.max_velocityx:
            self.velocityx = -self.max_velocityx
            
    def reset_ball(self):
        self.positionx = self.start_position[0]
        self.positiony = self.start_position[1]
        self.velocityx = random.randint(-self.max_velocityx,self.max_velocityx)