import pygame
import pymunk
from object import Object

class Pendulum(Object):
    def __init__(self, space, win, joint_pos, rope_pos, ball_radius, ball_color=(0, 0, 0, 100), rope_thickness=4, collision_type=1):
        super().__init__(space, win, collision_type=collision_type)
        self.rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.rotation_center_body.position = joint_pos

        self.body = pymunk.Body()
        self.body.position = rope_pos
        self.rope_shape = self.addSegment(self.body, (0, 0), (200, 0), rope_thickness, friction=1, mass=8)
        self.ball_shape = self.addCircle(self.body, ball_radius, ball_color, pos=(200, 0), friction=1, elasticity=0.95, mass=30)
        self.rope_shape.collision_type = collision_type
        self.ball_shape.collision_type = collision_type
        self.rotation_center_join = pymunk.PinJoint(self.body, self.rotation_center_body, (0, 0))

        self.space.add(self.body, self.rope_shape, self.ball_shape, self.rotation_center_join)


