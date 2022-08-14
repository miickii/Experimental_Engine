import pygame
from utils import mouseIn, createText

class Button():
    def __init__(self, win, pos, width, height, main_color, hover_color, action=None, text=None, text_size=18, text_color=(0, 0, 0, 255), border=None, border_color=(0, 0, 0)):
        self.win = win
        self.pos = pos
        self.type = "button"
        self.width = width
        self.height = height
        self.main_color = main_color
        self.hover_color = hover_color
        self.curr_color = main_color
        self.action = action
        self.text = None
        self.text_size = None
        self.border = border
        self.border_color = border_color

        if text:
            self.text, self.text_size = createText(text_size, text, True, color=text_color)

    def draw(self):
        pygame.draw.rect(self.win, self.curr_color, (self.pos[0], self.pos[1], self.width, self.height))
        if self.border_color and self.border:
            pygame.draw.rect(self.win, self.border_color, (self.pos[0], self.pos[1], self.width, self.height), width=self.border)
        if self.text:
            self.win.blit(self.text, (self.pos[0]+self.width/2-self.text_size[0]/2, self.pos[1]+self.height/2 - self.text_size[1]/2))

    def update(self, clicked, event_key=None, key=None):
        mouse_on_button = False
        if mouseIn(self.pos, self.width, self.height):
            mouse_on_button = True
            self.curr_color = self.hover_color
            if clicked and self.action:
                self.action()
        else:
            self.curr_color = self.main_color
        
        return mouse_on_button
