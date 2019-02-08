# Creating 3d graphics from 2d graphics
# Imports
from graphics import *
import math
from time import sleep

# Data classes
class Vec3:
    """Holds a position in 3d space"""
    def __init__(self, x = 0, y = 0, z = 0):
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
def convert3d2d(position, rotation, centerPos = Vec3(0, 0, 0)):
    """Changes a 2d point into 3d"""
    # Convert rotation from degrees to radians
    radX = rotation.x * 3.14 / 180
    radY = rotation.y * 3.14 / 180
    radZ = rotation.z * 3.14 / 180
    # Translate point to the center
    position.x -= centerPos.x
    position.y -= centerPos.y
    # Get point data for rotation of the Z axis
    p = [position.x * math.cos(radZ) - position.y * math.sin(radZ), position.y * math.cos(radZ) + position.x * math.sin(radZ)]
    # Get point data for rotation of the Y axis
    p = [p[0] * math.cos(radY) - position.z * math.sin(radY), p[1] * math.cos(radX) + position.z * math.sin(radX)]
    # Move point to original location
    p[0] += centerPos.x
    p[1] += centerPos.y
    # Return data
    return Point(p[0], p[1])

def multiply2d(p, multiplier):
    """Multiplies the point by another point"""
    p.x *= multiplier.x
    p.y *= multiplier.y
    return p

def multiply3d(vector, multiplier):
    """Multiplies the 3d vector by another 3d vector"""
    newVec = Vec3(vector.x * multiplier, vector.y * multiplier, vector.z * multiplier)
    return newVec

def add3d(vector, vector2):
    """Adds two 3d vectors"""
    newVec = Vec3(vector.x + vector2.x, vector.y + vector2.y, vector.z + vector2.z)
    return newVec

# Classes
class window3d:
    """Creates a window used for 3d rendering"""
    def __init__(self, title, x, y):
        # Initialize the objects variables
        self.window = GraphWin(title, x, y)
        self.window.setBackground("white")
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
            o.update()
            for p in o.polys:
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
            p1 = convert3d2d(add3d(multiply3d(self.vertices[i], self.scale - self.position.z), self.position), self.rotation, self.position)
            p2 = convert3d2d(add3d(multiply3d(self.vertices[i + 1], self.scale - self.position.z), self.position), self.rotation, self.position)
            p3 = convert3d2d(add3d(multiply3d(self.vertices[i + 2], self.scale - self.position.z), self.position), self.rotation, self.position)

            # Push back into the polygons array
            self.polys.append(Polygon(p1, p2, p3))

    def render(self, window):
        """Draws the object to the screen"""
        window.drawObj(self)

    def update(self):
        """Updates the object"""
        # Update the position of all the vertices according to the rotation
        # Update vertices for rotation on the Z axis

        # Update the vertices positions
        self.polys = [] # Clear array
        self.genPolygons()

    def setScale(self, scale):
        """Sets the scale of the vertices"""
        self.scale = scale

    def move(self, pos):
        """Moves the object by the position given"""
        self.position.x += pos.x
        self.position.y += pos.y
        self.position.z += pos.z

    def setPos(self, pos):
        """Sets the position of the object"""
        self.position = pos

    def rotate(self, rotation):
        """Increases or decreases the rotation of the object"""
        self.rotation.x += rotation.x
        self.rotation.y += rotation.y
        self.rotation.z += rotation.z

    def setRotation(self, rotation):
        """Sets the rotation of the object"""
        self.rotation = rotation

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
    tri = renderObject([Vec3(0, -1, 1), Vec3(-1, 1, 1), Vec3(1, 1, 1)], Vec3(320, 240, 0), Vec3(0, 0, 0))
    tri.setScale(100)
    tri.genPolygons()
    #tri.render(window)

    print("Generating square")
    square = renderObject([
        # Front
        Vec3(-1, -1, 1), Vec3(-1, 1, 1), Vec3(1, 1, 1), # Triangle 1 (left)
        Vec3(-1, -1, 1), Vec3(1, -1, 1), Vec3(1, 1, 1), # Triangle 2 (right)
        # Left
        Vec3(-1, -1, 1), Vec3(-1, -1, -1), Vec3(-1, 1, -1), # Triangle 1 (left)
        Vec3(-1, -1, 1), Vec3(-1, 1, 1), Vec3(-1, 1, -1), # Triangle 2 (right)
        # Right
        Vec3(1, -1, 1), Vec3(1, -1, -1), Vec3(1, 1, -1), # Triangle 1 (left)
        Vec3(1, -1, 1), Vec3(1, 1, 1), Vec3(1, 1, -1) # Triangle 2 (right)
    ], Vec3(320, 240, 0), Vec3(0, 0, 0))
    square.setScale(100)
    square.genPolygons()
    square.render(window)

    while True:
        keysPressed = window.window.checkKeys()
        if "w" in keysPressed:
            square.move(Vec3(0, -3, 0))
        if "s" in keysPressed:
            square.move(Vec3(0, 3, 0))

        if "a" in keysPressed:
            square.move(Vec3(-3, 0, 0))
        if "d" in keysPressed:
            square.move(Vec3(3, 0, 0))

        if "q" in keysPressed:
            square.move(Vec3(0, 0, 3))
        if "e" in keysPressed:
            square.move(Vec3(0, 0, -3))

        if "c" in keysPressed:
            square.rotate(Vec3(0, -2, 0))
        if "v" in keysPressed:
            square.rotate(Vec3(0, 2, 0))

        window.update()
        sleep(0.01)

    window.window.getMouse()


if __name__ == "__main__":
    main()
