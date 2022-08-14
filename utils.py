import pygame
import math

def calculateDistance(p1, p2):
    diff = (p2[0] - p1[0], p2[1] - p1[1])
    distance = math.sqrt(diff[0]**2 + diff[1]**2)
    return distance
    
def calculateAngle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def calculateMidpoint(p1, p2):
    diff = (p2[0]-p1[0], p2[1]-p1[1])
    midpoint = (diff[0]/2, diff[1]/2)
    true_midpoint = (midpoint[0]+p1[0], midpoint[1]+p1[1])
    return true_midpoint

def mouseIn(object_pos, object_w, object_h):
    mouse_pos = pygame.mouse.get_pos()
    return object_pos[0] <= mouse_pos[0] <= object_pos[0] + object_w and object_pos[1] <= mouse_pos[1] <= object_pos[1] + object_h

def createText(size, text, bold, font_style="Corbel", color=(0, 0, 0)):
    font = pygame.font.SysFont(font_style, size, bold=bold)
    return font.render(text, True, color), pygame.font.Font.size(font, text)


def removeObjectWithId(lst, object_id):
    for i in range(len(lst)):
        if lst[i].id == object_id:
            lst.pop(i)
            break

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

