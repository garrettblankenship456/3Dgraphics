# Creating 3d graphics from 2d graphics


# Imports
from graphics import *
import math
from time import sleep

# Classes
class window3d:
    """Creates a window used for 3d rendering"""
    def __init__(self, title, x, y):
        # Initialize the objects variables
        self.window = GraphWin(title, x, y)
        self.title = title
        self.xSize = x
        self.ySize = y

        # Initialize array for holding all the objects being drawn
        objects = []

class renderObject:
    """Object that is renderable by the window3d class"""
    def __init__(self, *vertices):
        # Initialize the objects variables
        self.vertices = vertices # Indices are chosen via the way the points are given

