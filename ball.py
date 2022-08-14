import pygame
import pymunk
from object import Object

class Ball(Object):
    def __init__(self, space, win, pos, radius, mass=1, elasticity=0.9, friction=0.5, body_type="DYNAMIC", color=(255, 0, 0, 100), collision_type=1):
        super().__init__(space, win, collision_type)
        self.space = space
        self.win = win
        self.mass = mass
        self.pos = pos
        self.radius = radius
        self.color = color
        self.elasticity = elasticity
        self.friction = friction

        self.body = pymunk.Body()
        self.body.position = pos
        #self.body, self.shape = self.createCircle(self.mass, self.pos, self.radius, self.color)
        self.shape = self.addCircle(self.body, radius, color, elasticity=self.elasticity, friction=self.friction, mass=self.mass)
        self.shape.collision_type = collision_type
        self.setBodyType(body_type)

        self.space.add(self.body, self.shape)

    def show(self, win):
        pygame.draw.circle(win, self.color, self.body.position, self.radius)
