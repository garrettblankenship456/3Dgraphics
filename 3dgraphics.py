# Creating 3d graphics from 2d graphics


# Imports
from graphics import *
import math
from time import sleep

# Data classes
class Vec3:
    """Holds a position in 3d space"""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def move(self, x = 0, y = 0, z = 0):
        """Moves vector"""
        self.x += x
        self.y += y
        self.z += z

# Functions
def convert3d2d(position, rotation):
    """Changes a 2d point into 3d"""
    pass

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
    def __init__(self, vertices = []):
        # Initialize the objects variables
        self.vertices = vertices # Indices are chosen via the way the points are given
        self.polys = [] # Create empty array of all the polygons
        
    def genPolygons(self):
        """When called it generates polygons from the points given"""
        # Count by threes because a triangle has three points and
        # a mesh is made out of three points
        for i in range(0, len(self.vertices), 3):
            # Push back into the polygons array
            #self.polys.append(Polygon())
            
        
    def render(self, window):
        """Draws the object to the screen"""
        pass
        
class cube(renderObject):
    """A renderable cube"""
    def __init__(self):
        # Initialize the vertices
        self.vertices = []
