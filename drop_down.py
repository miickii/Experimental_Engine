import enum
import pygame
from button import Button

class DropDown:
    def __init__(self, win, pos, width, height, menu_text, main_color, hover_color, items=[], item_buttons=[], input_boxes=None):
        # items is a list of tuples that each contain an object, string of either LEFT or RIGHT and row. E.g InputBox(....), "LEFT", 3
        # that will be the items of the drop down. E.g Button(), InputBox()
        # item_butons is a list with tuples of length 3 that contain: (main_color, hover_color, text). E.g [((255, 255, 255), (150, 150, 150), "Menu Item 1")]
        self.win = win
        self.pos = pos
        self.width, self.height = width, height
        self.menu_text = menu_text
        self.main_color = main_color
        self.hover_color = hover_color
        self.dropped = False

        self.menu_button = Button(self.win, self.pos, self.width, self.height, self.main_color, self.hover_color, self.dropDown, text=self.menu_text)
        self.item_buttons = []
        self.items = []
        
        curr_y_pos = self.height
        for i, item in enumerate(items):
            item.pos = (self.pos[0]+self.width-item.width, self.pos[1]+curr_y_pos)
            self.items.append(item)
            curr_y_pos += item.height

            #if item.type == "input_box" and input_boxes: input_boxes.append(item)

        for i, button in enumerate(item_buttons):
            self.item_buttons.append(Button(self.win, (self.pos[0], self.height+self.pos[1]+self.height*i), self.width, self.height, button[0], button[1], lambda: print("pressed"), text=button[2]))
            
    def update(self, clicked, event_key, key, properties=None):
        mouse_on_button = None

        if self.dropped:
            for button in self.item_buttons:
                mouse_on_button = button.update(clicked)
                #if mouse_on_button: break
            
            for item in self.items:
                item.update(clicked, event_key, key, properties)

        if not mouse_on_button: mouse_on_button = self.menu_button.update(clicked)
        
        return mouse_on_button


    def draw(self):
        if self.dropped:
            self.menu_button.curr_color = self.menu_button.hover_color
            for button in self.item_buttons:
                button.draw()

            for item in self.items:
                item.draw()
        
        self.menu_button.draw()

    def dropDown(self):
        self.dropped = not self.dropped
