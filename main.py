import pygame
import pymunk
import pymunk.pygame_util
import math
from utils import calculateAngle, calculateDistance, createText, removeObjectWithId, dotdict
from ball import Ball
from box import Box
from pendulum import Pendulum
from boundary_line import BoundaryLine
from shooting_ball_demo import ShootingBallDemo
from button import Button
from drop_down import DropDown
from input_box import InputBox

pygame.init()

WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))

class Game:
    def __init__(self, win, width, height):
        self.win = win
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.dt = 1 / self.fps
        self.mouse_pos = (0, 0)
        self.bg_color = (20, 21, 31)

        self.space = pymunk.Space()
        self.space.gravity = (0, 981)

        self.draw_options = pymunk.pygame_util.DrawOptions(self.win)
        self.draw_options.collision_point_color = (255, 255, 255, 0)
        self.curr_collision_type = 3

        self.running, self.pause, self.exit = 0, 1, 2
        self.state = self.running

        self.event_key = None
        self.key_typed = None
        self.mouse_down = False
        self.mouse_clicked = False
        self.mouse_joint = None
        self.shape_at_mouse = None

        self.mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.mouse_shape = pymunk.Circle(self.mouse_body, 1)
        self.mouse_shape.color = (255, 0, 0, 100)
        self.mouse_shape.sensor = True
        self.mouse_shape.collision_type = 0
        self.space.add(self.mouse_body, self.mouse_shape)

        self.demos = [ShootingBallDemo(self.space, self.win, self.width, self.height)]
        '''self.select_demo = {
            "shooting ball": self.demos[0]
        }'''
        self.current_demo = None #self.demos[0]
        if self.current_demo: self.current_demo.initialize()

        self.add_box, self.add_ball, self.add_boundary_line = 0, 1, 2
        self.shape_to_add = None
        self.continuos_add = False

        self.boxes = []
        self.balls = []
        self.boundaries = []
        self.edges = []
        self.objects = []
        self.delete_object = False

        self.adding_boundary_line = False
        self.bl_p1 = None
        self.bl_p2 = None

        # Object properties
        properties = {
            "friction": 0.4,
            "elasticity": 0.5,
            "gravity": 981,
            "edge_friction": 0.4,
            "edge_elasticity": 0.5
        }
        self.properties = dotdict(properties)

        self.buttons = []
        self.drop_downs = []
        self.input_boxes = []
        self.mouse_on_button = False

        self.controls_text = []

        self.pendulum = Pendulum(self.space, self.win, (200, 100), (200, 100), 10, rope_thickness=0.5, ball_color=(255, 0, 0, 100), collision_type=2)

        self.initFunctions()

    def run(self):
        while True:
            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_clicked = False
            self.mouse_body.position = self.mouse_pos
            #print(self.mouse_in_object)

            if self.state == self.running:
                self.handleEvents()
                self.update()
                self.clearScreen()
                self.draw()  


                self.space.step(self.dt)
                self.clock.tick(self.fps)
            elif self.state == self.pause:
                self.handleEvents()
                #self.clearScreen()
                #self.draw()

                #self.space.step(self.dt)
                self.clock.tick(self.fps)
            elif self.state == self.exit:
                break
        pygame.quit()
    
    def handleEvents(self):
        self.event_key = None
        self.key_typed = None
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = self.exit
                    break
                if self.current_demo:
                    self.current_demo.handleEvents(event)
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.mouse_down = True
                        self.mouse_clicked = True
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.mouse_down = False
                    elif event.type == pygame.KEYDOWN:
                        self.event_key = event.key
                        self.key_typed = event.unicode
                        '''if not self.key_saved: 
                            # Set key_typed to the pressed key and make sure it only gets saved once
                            self.keys_typed += event.unicode
                            self.key_saved = True
                        elif self.key_saved:
                            # If key is pressed down and has already been stored in key_typed for a frame, reset key_typed
                            self.key_typed = None'''

                        if event.key == pygame.K_ESCAPE:
                            if self.state == self.running: self.state = self.pause
                            else: self.state = self.running
                        elif event.key == pygame.K_LSHIFT:
                            self.shape_to_add = self.add_ball
                        elif event.key == pygame.K_LCTRL:
                            self.shape_to_add = self.add_box
                        elif event.key == pygame.K_SPACE:
                            self.shape_to_add = self.add_boundary_line
                        elif event.key == pygame.K_BACKSPACE:
                            self.delete_object = True

                        if event.key == pygame.K_LALT:
                            self.continuos_add = True
                    elif event.type == pygame.KEYUP:
                        self.shape_to_add = None

                        if event.key == pygame.K_LALT:
                            self.continuos_add = False
                        elif event.key == pygame.K_SPACE:
                            self.bl_p1 = None
                            self.bl_p2 = None
                        elif event.key == pygame.K_BACKSPACE:
                            self.delete_object = False



    def update(self):
        #print(self.shape_at_mouse)
        if self.current_demo:
            self.current_demo.update()
        else:
            self.space.gravity = (0, self.properties.gravity)

            for button in self.buttons:
                self.mouse_on_button = button.update(self.mouse_clicked)
            for drop_down in self.drop_downs:
                self.mouse_on_button = drop_down.update(self.mouse_clicked, self.event_key, self.key_typed, self.properties)
            for input_box in self.input_boxes:
                input_box.update(self.mouse_clicked, self.event_key, self.key_typed, self.properties)
            
            for edge in self.edges:
                edge.setProperties(self.properties.edge_elasticity, self.properties.edge_friction)

        # Updates depending on state
        if self.state == self.running and not self.mouse_on_button:
            # MOUSE CLICK ACTIONS
            if self.mouse_clicked:
                self.addShape()

                if self.shape_at_mouse and not self.shape_to_add:
                    if self.delete_object:
                        removeObjectWithId(self.objects, self.shape_at_mouse.collision_type)
                        body = self.shape_at_mouse.body # Getting the body associated with the shape

                        # Remove all shapes and constraints associated with the body
                        for c in body.constraints:
                            self.space.remove(c)
                        for s in body.shapes:
                            self.space.remove(s)
                        self.space.remove(body)
                    else:
                        self.mouse_joint = pymunk.PivotJoint(self.mouse_body, self.shape_at_mouse.body, (0, 0), (0, 0))
                        self.mouse_joint.error_bias = 0
                        #self.mouse_constraint = pymunk.Body(body_type=pymunk.Body.STATIC)
                        #self.mouse_constraint.position = self.mouse_pos
                        self.space.add(self.mouse_joint)
            elif self.mouse_down:
                if self.continuos_add:
                    self.addShape()
            else:
                # Mouse button lifted
                # Code for making objects dragged by mouse on mouse down drop themselves when mouse button is lifted
                if self.mouse_joint:
                    self.space.remove(self.mouse_joint)
                    self.mouse_joint = None

                
                #if self.mouse_in_object:
    
    def draw(self):
        self.space.debug_draw(self.draw_options)

        for i, text in enumerate(self.controls_text):
            self.win.blit(text[0], (0, text[1][1]*i))
        #(0+self.controls_text_size[0]/2, 0+self.controls_text_size[1]/2)

        if self.current_demo:
            self.current_demo.draw()
        else:
            for button in self.buttons:
                button.draw()
            for drop_down in self.drop_downs:
                drop_down.draw()
            for input_box in self.input_boxes:
                input_box.draw()
        
        pygame.display.update()
    
    def clearScreen(self):
        self.win.fill(self.bg_color)
    
    def addShape(self):
        if self.shape_to_add == self.add_box:
            self.objects.append(Box(self.space, self.win, self.mouse_pos, (20, 20), friction=self.properties.friction, elasticity=self.properties.elasticity, collision_type=self.curr_collision_type))
            self.curr_collision_type += 1
        elif self.shape_to_add == self.add_ball:
            self.objects.append(Ball(self.space, self.win, self.mouse_pos, 10, friction=self.properties.friction, elasticity=self.properties.elasticity, collision_type=self.curr_collision_type, ))
            self.curr_collision_type += 1
        elif self.shape_to_add == self.add_boundary_line:
            if self.bl_p1:
                print("hej")
                self.bl_p2 = self.mouse_pos
                self.objects.append(BoundaryLine(self.space, self.win, self.bl_p1, self.bl_p2, 5, friction=self.properties.friction, elasticity=self.properties.elasticity, collision_type=self.curr_collision_type))
                self.curr_collision_type += 1

                self.bl_p1 = None
                self.bl_p2 = None
            else:
                self.bl_p1 = self.mouse_pos
        
    
    def initFunctions(self):
        self.createEdges()
        self.createInteractives()
        self.initHandler()
        self.createControlsText()
    
    def createControlsText(self):
        ctrl1, ctrl1_size = createText(22, "SHIFT: Ball", False, color=(255, 0, 0), font_style="Arial Rounded MT Bold")
        ctrl2, ctrl2_size = createText(22, "CTRL: Box", False, color=(255, 0, 0), font_style="Arial Rounded MT Bold")
        ctrl3, ctrl3_size = createText(22, "SPACE: Boundary line", False, color=(255, 0, 0), font_style="Arial Rounded MT Bold")
        ctrl4, ctrl4_size = createText(22, "ALT: Continuos add object", False, color=(255, 0, 0), font_style="Arial Rounded MT Bold")
        ctrl5, ctrl5_size = createText(22, "DELETE: Remove object", False, color=(255, 0, 0), font_style="Arial Rounded MT Bold")
        self.controls_text.extend(((ctrl1, ctrl1_size), (ctrl2, ctrl2_size), (ctrl3, ctrl3_size), (ctrl4, ctrl4_size), (ctrl5, ctrl5_size)))
    
    def createEdges(self):
        edges = [
            [(self.width/2, self.height+10), (self.width, 40)],
            [(self.width/2, -20), (self.width, 40)],
            [(-21, self.height/2), (40, self.height)],
            [(self.width+20, self.height/2), (40, self.height)]
        ]

        for pos, size in edges:
            self.edges.append(Box(self.space, self.win, pos, size, body_type="STATIC", collision_type=1, friction=self.properties.friction, elasticity=self.properties.elasticity, color=(50, 50, 50, 100)))
    
    def createInteractives(self):
        #self.buttons.append(Button(self.win, (0, 0), 100, 50, (255, 0, 0), (255, 100, 100), lambda: print("pressed"), text="print"))
        self.drop_downs.append(DropDown(self.win, (self.width-150, 0), 150, 50, "Options", (51, 51, 60), (61, 61, 70), items=[
            InputBox(self.win, (0, 0), 50, 30, (41, 41, 50), (51, 51, 60), purpose_text="Elasticity", reference="elasticity", purpose_text_width=100, default_text=str(self.properties.elasticity), fixed_input_width=True, text_fixed="RIGHT", numbers_only=True, max_value=1),
            InputBox(self.win, (0, 0), 50, 30, (41, 41, 50), (51, 51, 60), purpose_text="Friction", reference="friction", purpose_text_width=100, default_text=str(self.properties.friction), fixed_input_width=True, text_fixed="RIGHT", numbers_only=True, max_value=1),
            InputBox(self.win, (0, 0), 50, 30, (41, 41, 50), (51, 51, 60), purpose_text="Gravity", reference="gravity", purpose_text_width=100, default_text=str(self.properties.gravity), fixed_input_width=True, text_fixed="RIGHT", numbers_only=True, min_value=1, max_value=2000),
            InputBox(self.win, (0, 0), 50, 30, (41, 41, 50), (51, 51, 60), purpose_text="Edge Elasticity", reference="edge_elasticity", purpose_text_width=100, default_text=str(self.properties.edge_elasticity), fixed_input_width=True, text_fixed="RIGHT", numbers_only=True, min_value=0.01, max_value=1),
            InputBox(self.win, (0, 0), 50, 30, (41, 41, 50), (51, 51, 60), purpose_text="Edge Friction", reference="edge_friction", purpose_text_width=100, default_text=str(self.properties.edge_friction), fixed_input_width=True, text_fixed="RIGHT", numbers_only=True, min_value=0.01, max_value=1)]))
        
        # EXAMPLES:
        #self.input_boxes.append(InputBox(self.win, (0, 400), 50, 50, (0, 255, 0), (100, 255, 100)))
        #self.drop_downs.append(DropDown(self.win, (200, 0), 100, 50, "Dropdown", (255, 0, 0), (255, 100, 100), item_buttons=[[(255, 255, 255), (150, 150, 150), "Menu Item 1"], [(255, 255, 255), (150, 150, 150), "Menu Item 2"], [(255, 255, 255), (150, 150, 150), "Menu Item 3"]]))
        #self.buttons.append(Button(self.win, (500, 0), 200, 50, (0, 255, 0), (100, 255, 100))) Button that doesn't have any action or text


    def initHandler(self):
        def collide(arbiter, space, data):
            self.shape_at_mouse = arbiter.shapes[1]
            #print(self.shape_at_mouse.collision_type)
            return True
        def separate(arbiter, space, data):
            self.shape_at_mouse = None

        self.collision_handlers = [self.space.add_collision_handler(0, i+2) for i in range(2000)]

        for handler in self.collision_handlers:
            handler.pre_solve = collide
            handler.separate = separate

if __name__ == "__main__":
    game = Game(window, WIDTH, HEIGHT)
    game.run()
    #run(window, WIDTH, HEIGHT)


