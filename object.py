import pygame
import pymunk

class Object:
    def __init__(self, space, win, collision_type):
        self.space = space
        self.win = win
        self.id = collision_type #id is the same as the shapes collision type
        # Collision type 0: defualt, 1: non deletable, 2: deletable, >=3: used for individual collision types
        self.body = None
        self.shape = None
        self.elasticity = None
        self.friction = None
        self.mass = None
        self.color = None
    
    def applyForce(self, force):
        self.body.apply_force_at_local_point(force, (0, 0))

    def applyImpulse(self, impulse):
        self.body.apply_impulse_at_local_point(impulse, (0, 0))
    
    def addCircle(self, body, radius, color, pos=(0, 0), elasticity=0, friction=0, mass=0):
        shape = pymunk.Circle(body, radius, pos)
        shape.mass = mass
        shape.elasticity = elasticity
        shape.friction = friction
        shape.color = color
        #self.space.add(body, shape)

        return shape
    
    def addBox(self, body, w, h, color, outline=None, pos=(0, 0), elasticity=0, friction=0, mass=0):
        shape = pymunk.Poly.create_box(body, (w, h), radius=outline) if outline else pymunk.Poly.create_box(body, (w, h))
        shape.mass = mass
        shape.elasticity = elasticity
        shape.friction = friction
        shape.color = color
        #self.space.add(body, shape)

        return shape
    
    def addSegment(self, body, a, b, thickness, color=(0, 0, 0, 100), mass=0, elasticity=0, friction=0):
        shape = pymunk.Segment(body, a, b, thickness)
        shape.mass = mass
        shape.elasticity = elasticity
        shape.friction = friction
        shape.color = color
        #self.space.add(body, shape)

        return shape
    
    def createSegment(self, mass, pos, a, b, thickness, color):
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Segment(body, a, b, thickness)
        shape.mass = mass
        shape.elasticity = self.elasticity
        shape.friction = self.friction
        shape.color = color
        #self.space.add(body, shape)

        return body, shape
    
    def createPoly(self, mass, pos, vertices, color, radius=0):
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Poly(body, vertices, radius)
        shape.mass = mass
        shape.elasticity = self.elasticity
        shape.friction = self.friction
        shape.color = color
        #self.space.add(body, shape)

        return body, shape
    
    def setBodyType(self, body_type):
        if (body_type == "DYNAMIC"):
            self.body.body_type = pymunk.Body.DYNAMIC
        elif (body_type == "KINEMATIC"):
            self.body.body_type = pymunk.Body.KINEMATIC
        elif body_type == "STATIC":
            self.body.body_type = pymunk.Body.STATIC


        '''
        shape_func = getattr(pymunk, shape_type, "Circle")
        shape = shape_func(body, radius)
        '''
    
    def getObjectFromShape(self, shape):
        return (self.shape == shape)