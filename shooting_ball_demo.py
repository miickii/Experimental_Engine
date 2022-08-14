import pygame
import pymunk
import math
from utils import *
from pendulum import Pendulum
from box import Box
from ball import Ball


class ShootingBallDemo:
    def __init__(self, space, win, width, height):
        self.space = space
        self.win = win
        self.width = width
        self.height = height
        self.selected = False

        self.balls = []
        self.pressed_pos = None
        self.ball = None
        self.ball_line = None

        self.boundaries = []

        self.objects = []

        if self.selected:
            self.initialize()
    
    def initialize(self):
        self.createEdges()
        self.createStructure()
        self.pendulum = Pendulum(self.space, self.win, (300, 150), (300, 150), 30)

    def run(self):
        pass

    def update(self):
        if (self.ball and self.pressed_pos):
            self.ball_line = [self.pressed_pos, pygame.mouse.get_pos()]
    
    def draw(self):
        if (self.ball_line):
            pygame.draw.line(self.win, 'black', self.ball_line[0], self.ball_line[1], 3)

    def handleEvents(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.ball:
                self.pressed_pos = pygame.mouse.get_pos()
                self.ball = Ball(self.space, self.win, self.pressed_pos, 30, mass=30, body_type="STATIC")
            elif self.pressed_pos:
                angle = calculateAngle(*self.ball_line) # * breaks the line into it's two components
                force = calculateDistance(*self.ball_line) * 100
                fx = math.cos(angle) * force
                fy = math.sin(angle) * force
                self.ball.setBodyType("DYNAMIC")
                self.ball.applyImpulse((fx, fy))
                self.pressed_pos = None
                self.ball_line = None
            else:
                self.space.remove(self.ball.body, self.ball.shape)
                self.ball = None

    def createEdges(self):
        edges = [
            [(self.width/2, self.height-10), (self.width, 20)],
            [(self.width/2, 10), (self.width, 20)],
            [(10, self.height/2), (20, self.height)],
            [(self.width-10, self.height/2), (20, self.height)]
        ]

        for pos, size in edges:
            self.boundaries.append(Box(self.space, self.win, pos, size, body_type="STATIC"))

    def createStructure(self):
        BROWN = (139, 69, 19, 100)
        rects = [
            [(500, self.height - 20-75), (30, 150), BROWN, 100],
            [(700, self.height - 20-75), (30, 150), BROWN, 100],
            [(600, self.height - 150-20-15), (230, 30), BROWN, 150]
        ]

        for pos, size, color, mass in rects:
            self.objects.append(Box(self.space, self.win, pos, size, color=color, mass=mass, elasticity=0.4, friction=0.4, outline=2))