# Creating 3d graphics from 2d graphics

# Plans and ideas
"""
I want to make each point an offset from the position thats provided in the
renderObject class, that way the position is in the center and not top left front
of the object.
"""

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

    def set(self, x = 0, y = 0, z = 0):
        """Set the vector"""
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        print("Vector: X = " + self.x + "; Y = " + self.y + "; Z = " + self.z)

# Functions
def convert3d2d(position, rotation):
    """Changes a 2d point into 3d"""
    return Point(position.x, position.y)

def multiply2d(p, multiplier):
    """Multiplies the point by another point"""
    p.x *= multiplier.x
    p.y *= multiplier.y
    return p

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
        self.objects = []

    def update(self):
        """Updates all the objects by undrawing and redrawing to the window"""
        for o in self.objects:
            for p in o.polys:
                p.undraw()
                p.draw(self.window)

    def drawObj(self, obj):
        """Adds an object to draw into the objects array"""
        # Draw all the polygons
        for p in obj.polys:
            p.draw(self.window)

        # Add object to the internal objects array
        self.objects.append(obj)

class renderObject:
    """Object that is renderable by the window3d class"""
    def __init__(self, vertices = [], position = Vec3(0, 0, 0), rotation = Vec3(0, 0, 0)):
        # Initialize the objects variables
        self.vertices = vertices # Indices are chosen via the way the points are given
        self.polys = [] # Create empty array of all the polygons

        # Set the variables for keeping space
        self.position = position
        self.rotation = rotation
        self.scale = 1

    def genPolygons(self):
        """When called it generates polygons from the points given"""
        # Count by threes because a triangle has three points and
        # a mesh is made out of three points
        for i in range(0, len(self.vertices), 3):
            # Get the position of all the seperate points
            p1 = multiply2d(convert3d2d(self.vertices[i], self.rotation), Point(self.scale, self.scale))
            p2 = multiply2d(convert3d2d(self.vertices[i + 1], self.rotation), Point(self.scale, self.scale))
            p3 = multiply2d(convert3d2d(self.vertices[i + 2], self.rotation), Point(self.scale, self.scale))

            # Push back into the polygons array
            self.polys.append(Polygon(p1, p2, p3))

    def render(self, window):
        """Draws the object to the screen"""
        pass

    def setScale(self, scale):
        """Sets the scale of the vertices"""
        self.scale = scale

class cube(renderObject):
    """A renderable cube"""
    def __init__(self):
        # Initialize the vertices
        self.vertices = []


# Run the main function if this file is ran
def main():
    print("Generating window")
    window = window3d("Test graphics", 640, 480)

    # Generate object
    print("Generating triangle")
    tri = renderObject([Vec3(0.5, 0, 1), Vec3(0, 1, 1), Vec3(1, 1, 1)], Vec3(320, 240, 0), Vec3(0, 0, 0))
    tri.setScale(100)
    tri.genPolygons()
    tri.render(window)

    #window.drawObj(tri)
    window.update()


    window.window.getMouse()


if __name__ == "__main__":
    main()
