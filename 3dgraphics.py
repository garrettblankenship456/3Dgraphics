# Creating 3d graphics from 2d graphics
# Imports
from graphics import *
import math
from time import sleep

# TODO:
#   Add obj file importer
#   Make it so when a point is farther back X and Y are reduced to give more
#       of a 3d look to the object

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

class Color:
    """Holds color data"""
    def __init__(self, r = 0, g = 0, b = 0):
        self.r = r
        self.g = g
        self.b = b

    def getColorRGB(self, multiplier):
        r = int(self.r - multiplier)
        g = int(self.g - multiplier)
        b = int(self.b - multiplier)
        if r > 255:
            r = 255
        elif r < 0:
            r = 0
        if g > 255:
            g = 255
        elif g < 0:
            g = 0
        if b > 255:
            b = 255
        elif b < 0:
            b = 0

        return color_rgb(r, g, b)

# Functions
def rotate3d(position, rotation, centerPos = Vec3(0, 0, 0)):
    """Rotates a 3d point around the center position"""
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

    # Translate point into original position
    position.x += centerPos.x
    position.y += centerPos.y
    position.z += centerPos.z

    # Return data
    return position

def convert3d2d(position, rotation, centerPos = Vec3(0, 0, 0)):
    """Changes a 3d point into 2d"""
    # Rotate the point based on rotation
    position = rotate3d(position, rotation, centerPos)

    # Add into point for returning
    p = Point(position.x, position.y)
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

def getZDepth(point, rotation, center):
    """Gets the Z value of a point"""
    point = rotate3d(point, rotation, center)
    return point.z

def distance3d(v1, v2):
    """Gets the distance between two 3d vectors"""
    dx = v2.x - v1.x
    dy = v2.y - v1.y
    distance = math.hypot(dx, dy)
    return distance

# Classes
class Window3d:
    """Creates a window used for 3d rendering"""
    def __init__(self, title, x, y):
        # Initialize the objects variables
        self.window = GraphWin(title, x, y, autoflush=False)
        self.window.setBackground("white")
        self.title = title
        self.xSize = x
        self.ySize = y
        self.ambient = 0.2 # The amount of light if no light is present

        # Initialize array for holding all the objects being drawn
        self.objects = []
        self.lights = [] # Hold all the lights

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
            drawOrder = sorted(drawOrder.items(), key=lambda kv: kv[1], reverse=True)

            # Redraw all the polygons in order of Z greatest to least
            for k, v in drawOrder:
                # Create color
                c = o.color

                # Calculate light factor for the polygon by each light
                for l in self.lights:
                    lightFactor = ((distance3d(Vec3(o.polys[k].getPoints()[0].getX(), o.polys[k].getPoints()[0].getY(), v), l.position) + self.ambient) / l.radius) * l.intensity
                    print(lightFactor)

                # Turn c into color_rgb
                c = c.getColorRGB(lightFactor)

                # Draw polygon
                o.polys[k].draw(self.window)
                o.polys[k].setFill(c)
                o.polys[k].setOutline(c)

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

    def addLight(self, light):
        """Adds a light into the scene"""
        self.lights.append(light)

class RenderObject:
    """Object that is renderable by the window3d class"""
    def __init__(self, position = Vec3(0, 0, 0), rotation = Vec3(0, 0, 0), scale = Vec3(1, 1, 1), color = color_rgb(255, 255, 255), vertices = None):
        # Initialize the objects variables
        self.vertices = [] # Indices are chosen via the way the points are given
        self.polys = [] # Create empty array of all the polygons
        self.polyAreas = [] # Create empty array of all the depths for the polygons

        # Set the variables for keeping space
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.color = color

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
            v1 = add3d(multiply3d(self.vertices[i], self.scale), self.position)
            v2 = add3d(multiply3d(self.vertices[i + 1], self.scale), self.position)
            v3 = add3d(multiply3d(self.vertices[i + 2], self.scale), self.position)

            p1 = convert3d2d(add3d(multiply3d(self.vertices[i], self.scale), self.position), self.rotation, self.position)
            p2 = convert3d2d(add3d(multiply3d(self.vertices[i + 1], self.scale), self.position), self.rotation, self.position)
            p3 = convert3d2d(add3d(multiply3d(self.vertices[i + 2], self.scale), self.position), self.rotation, self.position)

            # Get the lowest point
            zDepths = [getZDepth(v1, self.rotation, self.position), getZDepth(v2, self.rotation, self.position), getZDepth(v3, self.rotation, self.position)]
            # Populate polygon depths (more X and Y means on the screen)
            self.polyAreas.append(max(zDepths))

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

class Cube(RenderObject):
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

class Light:
    def __init__(self, position, intensity, radius):
        # Initialize variables
        self.position = position
        self.intensity = intensity
        self.radius = radius

class Camera:
    def __init__(self, position, rotation, fov):
        # Initialize variables
        self.position = position
        self.rotation = rotation
        self.fov = fov

# Run the main function if this file is ran
def main():
    print("Generating window")
    window = Window3d("Test graphics", 640, 480)

    print("Generating lights")
    l = Light(Vec3(400, 0, 200), 1, 10)
    window.addLight(l)

    print("Generating square")
    square = Cube(Vec3(320, 240, 0), Vec3(0, 0, 0), Vec3(100, 100, 100), Color(255, 0, 0))
    square.render(window)

    while True:
        keysPressed = window.window.checkKeys()
        if "w" in keysPressed:
            square.move(Vec3(0, -3, 3))
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
