import pygame
from utils import mouseIn

class InputBox:
    def __init__(self, win, pos, input_width, height, main_color, hover_color, reference=None, fixed_input_width=False, text_fixed="CENTER", default_text="", purpose_text=None, purpose_text_width=0, text_size=18, font=None, text_color=(100, 100, 100, 255), active_text_color=(255, 255, 255), border=None, border_color=None, text_field_color=(255, 255, 255), numbers_only=False, max_value=999, min_value=0):
        self.win = win
        self.pos = pos
        self.type = "input_box"
        self.input_width = input_width
        self.original_input_width = self.input_width
        self.purpose_text_width = purpose_text_width
        self.width = self.input_width + self.purpose_text_width
        self.height = height
        self.main_color = main_color
        self.hover_color = hover_color
        self.curr_color = self.main_color
        self.reference = reference
        self.fixed_input_width = fixed_input_width
        self.max_chars = self.input_width//9 if self.fixed_input_width else 999
        self.text_fixed = text_fixed
        self.text_field_color = text_field_color
        self.text = default_text
        self.purpose_text = purpose_text
        self.text_size = text_size
        self.text_color = text_color
        self.active_text_color = active_text_color
        self.curr_text_color = text_color
        self.font = font
        self.border = border
        self.border_color = border_color
        self.active = False
        self.numbers_only = numbers_only
        self.min_value = min_value
        self.max_value = max_value

        if not self.font:
            self.font = pygame.font.SysFont(None, self.text_size)
        
        if purpose_text:
            self.purpose_text = self.font.render(purpose_text, True, self.text_color)

    
    def checkNumber(self):
        number = 0
        try:
            number = float(self.text)
            if number <= self.min_value: number = self.min_value
            elif number >= self.max_value: number = self.max_value

            return str(number), number
        except:
            return str(self.min_value), self.min_value


    def update(self, clicked, event_key, key, properties=None):
        self.width = self.input_width + self.purpose_text_width
        if mouseIn((self.pos[0]+self.purpose_text_width, self.pos[1]), self.input_width, self.height):
            self.curr_color = self.hover_color
            if clicked:
                self.active = True
                self.curr_text_color = self.active_text_color

                if self.numbers_only:
                    self.text = ""
        else:
            if clicked:
                self.active = False
                self.curr_text_color = self.text_color
                if self.reference: setattr(properties, self.reference, self.text)

                if self.numbers_only:
                    self.text, number = self.checkNumber()
                    if self.reference: setattr(properties, self.reference, number)
            if not self.active:
                self.curr_color = self.main_color
        
        if self.active and event_key:
            if event_key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) <= self.max_chars:
                    self.text += key
            
        return self.active
    
    def draw(self):
        text_surface = self.font.render(self.text, True, self.curr_text_color)
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()
        #width = max(self.width, text_width+10)

        #self.width = width
        if not self.fixed_input_width:
            if self.input_width < self.original_input_width:
                self.input_width = self.original_input_width
            elif self.input_width < text_width+10 or self.input_width > text_width and self.input_width > self.original_input_width:
                self.input_width = text_width+10

        pygame.draw.rect(self.win, self.main_color, (self.pos[0], self.pos[1], self.purpose_text_width, self.height))
        pygame.draw.rect(self.win, self.curr_color, (self.pos[0] + self.purpose_text_width, self.pos[1], self.input_width, self.height))
        if self.border_color and self.border:
            pygame.draw.rect(self.win, self.border_color, (self.pos[0], self.pos[1], self.width, self.height), width=self.border)
        
        if self.purpose_text:
            self.win.blit(self.purpose_text, (self.pos[0]+5, self.pos[1]+self.height/2 - self.purpose_text.get_height()/2))

        if self.text_fixed == "LEFT":
            self.win.blit(text_surface, (self.pos[0]+self.purpose_text_width + 2, self.pos[1]+self.height/2 - text_height/2))
        elif self.text_fixed == "RIGHT":
            self.win.blit(text_surface, (self.pos[0]+self.purpose_text_width + self.input_width-text_width-2, self.pos[1]+self.height/2 - text_height/2))
        else:
            self.win.blit(text_surface, (self.pos[0]+self.purpose_text_width + self.input_width/2-text_width/2, self.pos[1]+self.height/2 - text_height/2))


