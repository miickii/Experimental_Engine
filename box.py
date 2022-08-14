import winsound
import pygame
import pymunk
from object import Object

class Box(Object):
    def __init__(self, space, win, pos, size, mass=1, elasticity=0.4, friction=0.5, outline=None, body_type="DYNAMIC", color=(0, 0, 255, 100), collision_type=1):
        super().__init__(space, win, collision_type)
        self.space = space
        self.win = win
        self.mass = mass
        self.pos = pos
        self.w = size[0]
        self.h = size[1]
        self.color = color
        self.elasticity = elasticity
        self.friction = friction

        self.body = pymunk.Body()
        self.body.position = pos
        self.shape = self.addBox(self.body, self.w, self.h, self.color, outline=outline, elasticity=self.elasticity, friction=self.friction, mass=self.mass)
        self.shape.collision_type = collision_type
        self.setBodyType(body_type)

        self.space.add(self.body, self.shape)
    
    def setProperties(self, elasticity=None, friction=None):
        if elasticity: self.setElasticity(elasticity)
        if friction: self.setFriction(friction)

    def setElasticity(self, elasticity):
        self.elasticity = elasticity
        self.shape.elasticity = self.elasticity
    
    def setFriction(self, friction):
        self.friction = friction
        self.shape.friction = self.friction
    