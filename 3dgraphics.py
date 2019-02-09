# Creating 3d graphics from 2d graphics
# Imports
from graphics import *
import math
from time import sleep

# TODO:
#   Fix the draw order, Right now all the polygons are drawn in the way they were
#   generated making the box transparent

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
        print("Vector: X =", self.x, " Y =", self.y, " Z = ", self.z)
        return ""

# Functions
def convert3d2d(position, rotation, centerPos = Vec3(0, 0, 0)):
    """Changes a 3d point into 2d"""
    # Convert rotation from degrees to radians
    radX = rotation.x * 3.14 / 180
    radY = rotation.y * 3.14 / 180
    radZ = rotation.z * 3.14 / 180
    # Translate point to the center
    position.x -= centerPos.x
    position.y -= centerPos.y
    position.z -= centerPos.z

    # Rotate Z
    position = Vec3(position.x * math.cos(radZ) - position.y * math.sin(radZ), # X
                    position.x * math.sin(radZ) + position.y * math.cos(radZ), # Y
                    position.z) # Z
    # Rotate Y
    position = Vec3(position.x * math.cos(radY) + position.z * math.sin(radY), # X
                    position.y, # Y
                    -position.x * math.sin(radY) + position.z * math.cos(radY)) # Z
    # Rotate X
    position = Vec3(position.x, # X
                    position.y * math.cos(radX) - position.z * math.sin(radX), # Y
                    position.y * math.sin(radX) + position.z * math.cos(radX)) # Z

    # Add into point for returning
    p = Point(position.x + centerPos.x, position.y + centerPos.y)
    # Return data
    return p

def multiply2d(p, multiplier):
    """Multiplies the point by another point"""
    p.x *= multiplier.x
    p.y *= multiplier.y
    return p

def multiply3d(vector, vector2):
    """Multiplies the 3d vector by another 3d vector"""
    newVec = Vec3(vector.x * vector2.x, vector.y * vector2.y, vector.z * vector2.z)
    return newVec

def add3d(vector, vector2):
    """Adds two 3d vectors"""
    newVec = Vec3(vector.x + vector2.x, vector.y + vector2.y, vector.z + vector2.z)
    return newVec

def triangleArea(p1, p2, p3):
    x1 = p1.getX()
    y1 = p1.getY()
    x2 = p2.getX()
    y2 = p2.getY()
    x3 = p3.getX()
    y3 = p3.getY()
    area = (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2
    return abs(area)

# Classes
class window3d:
    """Creates a window used for 3d rendering"""
    def __init__(self, title, x, y):
        # Initialize the objects variables
        self.window = GraphWin(title, x, y, autoflush=False)
        self.window.setBackground("white")
        self.title = title
        self.xSize = x
        self.ySize = y

        # Initialize array for holding all the objects being drawn
        self.objects = []

    def update(self):
        """Updates all the objects by undrawing and redrawing to the window"""
        for o in self.objects:
            # Undraw all the polygons
            for p in o.polys:
                p.undraw()

            # Update the object as a whole
            o.update()

            # Sort all the polygon depths and polygons
            drawOrder = {}
            # Loop through all the depths given, and put in the max with the polygon number
            for i in range(len(o.polyAreas)):
                drawOrder[i] = o.polyAreas[i]
            drawOrder = sorted(drawOrder.items(), key=lambda kv: kv[1])
            print(drawOrder)
            # Redraw all the polygons in order of Z greatest to least
            for k, v in drawOrder:
                r = round(v / 255)
                if r < 0:
                    r = 0

                o.polys[k].draw(self.window)
                #o.polys[k].setFill(color_rgb(r, 0, 0))
                o.polys[k].setFill("white")

        # Update window framebuffer
        update(120)

    def drawObj(self, obj):
        """Adds an object to draw into the objects array"""
        # Draw all the polygons
        for p in obj.polys:
            p.draw(self.window)

        # Add object to the internal objects array
        self.objects.append(obj)

    def undrawObj(self, obj):
        """Removes an object from the window"""
        # Remove all polygons
        for p in obj.polys:
            p.undraw()

        # Remove object from the internal objects array
        self.objects.remove(obj)

class renderObject:
    """Object that is renderable by the window3d class"""
    def __init__(self, position = Vec3(0, 0, 0), rotation = Vec3(0, 0, 0), scale = Vec3(1, 1, 1), vertices = None):
        # Initialize the objects variables
        self.vertices = [] # Indices are chosen via the way the points are given
        self.polys = [] # Create empty array of all the polygons
        self.polyAreas = [] # Create empty array of all the depths for the polygons

        # Set the variables for keeping space
        self.position = position
        self.rotation = rotation
        self.scale = scale

        # Populate vertices if none were provided
        if vertices == None:
            self._populateVertices()
        else:
            self.vertices = vertices

        # Generate polygons
        self.genPolygons()

    def genPolygons(self):
        """When called it generates polygons from the points given"""
        # Count by threes because a triangle has three points and
        # a mesh is made out of three points
        for i in range(0, len(self.vertices), 3):
            # Get the position of all the seperate points
            p1 = convert3d2d(add3d(multiply3d(self.vertices[i], self.scale), self.position), self.rotation, self.position)
            p2 = convert3d2d(add3d(multiply3d(self.vertices[i + 1], self.scale), self.position), self.rotation, self.position)
            p3 = convert3d2d(add3d(multiply3d(self.vertices[i + 2], self.scale), self.position), self.rotation, self.position)

            # Populate polygon depths (more X and Y means on the screen)
            a = triangleArea(p1, p2, p3)
            self.polyAreas.append(a)

            # Push back into the polygons array
            self.polys.append(Polygon(p1, p2, p3))

        # Color all the polygons randomly
        l = 0
        for p in self.polys:
            l += 20
            p.setFill(color_rgb(l, 0, 0))

    def render(self, window):
        """Draws the object to the screen"""
        window.drawObj(self)

    def update(self):
        """Updates the object"""
        # Update the vertices positions
        self.polys = [] # Clear array
        self.polyAreas = [] # Clear array
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

    def _populateVertices(self):
        # Generates all the vertices
        pass # overriden by sub class

class cube(renderObject):
    """A renderable cube"""
    def _populateVertices(self):
        # Initialize the vertices
        self.vertices = [
            # Front
            Vec3(-1, -1, 1), Vec3(-1, 1, 1), Vec3(1, 1, 1), # Triangle 1 (left)
            Vec3(-1, -1, 1), Vec3(1, -1, 1), Vec3(1, 1, 1), # Triangle 2 (right)
            # Left
            Vec3(-1, -1, 1), Vec3(-1, -1, -1), Vec3(-1, 1, -1), # Triangle 1 (left)
            Vec3(-1, -1, 1), Vec3(-1, 1, 1), Vec3(-1, 1, -1), # Triangle 2 (right)
            # Right
            Vec3(1, -1, 1), Vec3(1, -1, -1), Vec3(1, 1, -1), # Triangle 1 (left)
            Vec3(1, -1, 1), Vec3(1, 1, 1), Vec3(1, 1, -1), # Triangle 2 (right)
            # Top
            Vec3(-1, -1, 1), Vec3(1, -1, 1), Vec3(1, -1, -1), # Triangle 1 (left)
            Vec3(-1, -1, 1), Vec3(-1, -1, -1), Vec3(1, -1, -1), # Triangle 2 (right)
            # Bottom
            Vec3(-1, 1, 1), Vec3(1, 1, 1), Vec3(1, 1, -1), # Triangle 1 (left)
            Vec3(-1, 1, 1), Vec3(-1, 1, -1), Vec3(1, 1, -1), # Triangle 2 (right)
            # Back
            Vec3(-1, -1, -1), Vec3(-1, 1, -1), Vec3(1, 1, -1), # Triangle 1 (left)
            Vec3(-1, -1, -1), Vec3(1, -1, -1), Vec3(1, 1, -1) # Triangle 2 (right)
        ]

# Run the main function if this file is ran
def main():
    print("Generating window")
    window = window3d("Test graphics", 640, 480)

    print("Generating square")
    square = cube(Vec3(320, 240, 0), Vec3(0, 0, 0), Vec3(100, 100, 100))
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
            square.rotate(Vec3(2, 2, 0))
        if "v" in keysPressed:
            square.rotate(Vec3(-2, -2, -2))

        window.update()
        sleep(0.01)

    window.window.getMouse()


if __name__ == "__main__":
    main()
