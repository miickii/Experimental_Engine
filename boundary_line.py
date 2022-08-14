import pygame
import pymunk
from utils import calculateMidpoint, calculateAngle
from object import Object

class BoundaryLine(Object):
    def __init__(self, space, win, p1, p2, width, elasticity=0.4, friction=0.5, outline=None, color=(0, 0, 0, 100), collision_type=1):
        super().__init__(space, win, collision_type=collision_type)
        self.space = space
        self.win = win
        self.p1 = p1
        self.p2 = p2
        self.midpoint = calculateMidpoint(self.p1, self.p2)
        self.angle = calculateAngle(self.p1, self.p2)
        self.width = width
        self.elasticity = elasticity
        self.friction = friction
        self.color = color

        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        #self.body.position = self.midpoint
        self.shape = self.addSegment(self.body, self.p1, self.p2, self.width, color=self.color, elasticity=self.elasticity, friction=self.friction)
        self.shape.collision_type = collision_type

        self.space.add(self.body, self.shape)





