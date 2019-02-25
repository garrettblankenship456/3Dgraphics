# Creating 3d graphics from 2d graphics
# Imports
from graphics import *
import math
from time import sleep

# TODO:
#   Make it so when a point is farther back X and Y are reduced to give more
#       of a 3d look to the object
#   Make the entire object 3d points and have the renderer use a view and perspective
#       matrix to give the get the points for 3d

# Data classes
class Vec3:
    """Holds a position in 3d space"""
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        s = "Vector 3:\n"
        s += "  X: " + str(self.x) + "\n"
        s += "  Y: " + str(self.y) + "\n"
        s += "  Z: " + str(self.z) + "\n"
        return s

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

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

    def normalize(self):
        """Normalizes the vector"""
        # Get the magnitude
        mag = math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

        # Get the normalized vector
        if mag > 0:
            return Vec3(self.x / mag, self.y / mag, self.z / mag)

        # If not able to divide, return 0
        return Vec3(0, 0, 0)

    def cross(self, other):
        """Gets the cross product between two vectors"""
        newVec = Vec3(self.y * other.z - self.z * other.y,
                      self.x * other.z - self.z * other.x,
                      self.x * other.y - self.y * other.x)
        return newVec

    def getCopy(self):
        """Gets a copied vector"""
        return Vec3(self.x, self.y, self.z)

class Color:
    """Holds color data"""
    def __init__(self, r = 0, g = 0, b = 0):
        self.r = r
        self.g = g
        self.b = b

    def getColorRGB(self, multiplier, ambientLight):
        r = int(self.r - multiplier) + ambientLight
        g = int(self.g - multiplier) + ambientLight
        b = int(self.b - multiplier) + ambientLight
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

class Mat4:
    """A 4x4 matrix"""
    def __init__(self, matrix = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]):
        # Initialize variables
        self.matrix = matrix

    def __str__(self):
        info = "4x4 Matrix: \n"
        info += "   1: " + str(self.matrix[0]) + "\n"
        info += "   2: " + str(self.matrix[1]) + "\n"
        info += "   3: " + str(self.matrix[2]) + "\n"
        info += "   4: " + str(self.matrix[3]) + "\n"
        return info

    def __getitem__(self, item):
        # Returns the item from the position in the matrix
        return self.matrix[item]

    def __len__(self):
        # Returns the length of the matrix
        return len(self.matrix)

    def multiply4x4(self, matrix):
        """Multiplies this matrix by the one provided"""
        result = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]
        for i in range(len(self.matrix)):
            for j in range(len(matrix[0])):
                for k in range(len(matrix)):
                    result[i][j] += self.matrix[i][k] * matrix[k][j]

        return Mat4(result)

    def multiplyVec(self, vector):
        """Multiplies this matrix by the vector provided"""
        result = [[vector.x, vector.y, vector.z, 1]]
        result = self.multiply4x4(result)
        result = Vec3(result[0][0], result[0][1], result[0][2])
        return result

    def invert(self):
        """Returns the inverse of the matrix"""
        result = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        # Get lengths
        m = len(result) - 1
        n = len(result[0]) - 1

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                result[m - i][n - j] = self.matrix[i][j]

        return Mat4(result)

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

def convert3d2d(position, center):
    """Changes a 3d point into 2d"""
    # Add into point for returning
    p = Point(position.x / 2 + center.x, position.y / 2 + center.y)
    #p = Point(position.x, position.y)
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
    dz = v2.z - v1.z
    distance = math.hypot(dx, dy)
    distance = math.hypot(distance, dz)
    return distance

def distance2d(p1, p2):
    """Gets the distance between two 2d vectors"""
    dx = p2.getX() - p1.getX()
    dy = p2.getY() - p1.getY()
    return Point(dx, dy)

def loadObj(path):
    """Loads an OBJ file into vertices"""
    f = open(path, "r")

    # t_ is for temporary
    t_vertices = []
    t_indices = []

    # Read file line by name and import vertices
    line = f.readline()
    while line != None:
        # Parse data
        lineSplit = line.split(" ")
        if len(lineSplit) > 0 and lineSplit[0] == "v":
            # Its a vertex
            t_vertices.append(Vec3(float(lineSplit[1]), float(lineSplit[2]), float(lineSplit[3])))
        # Parse faces
        if len(lineSplit) > 0 and lineSplit[0] == "f":
            # Its a face, which holds indices
            splitFace1 = lineSplit[1].split("/")
            splitFace2 = lineSplit[2].split("/")
            splitFace3 = lineSplit[3].split("/")

            t_indices.append(int(splitFace1[0].rstrip()))
            t_indices.append(int(splitFace2[0].rstrip()))
            t_indices.append(int(splitFace3[0].rstrip()))

        # Exit if none
        if line == "" or line == None:
            break

        # Read next line
        line = f.readline()

    # Reindex the vertices
    vOut = []
    for i in t_indices:
        vOut.append(t_vertices[i - 1])

    # Cleanup and returning data
    f.close()
    return vOut

def lookAt(eye, target, up):
    """Creates a view matrix with the given parameters"""
    vZ = (eye - target).normalize()
    vX = up.cross(vZ).normalize()
    vY = vZ.cross(vX)
    inverseMatrix = [
        [vX.x, vX.y, vX.z, 0],
        [vY.x, vY.y, vY.z, 0],
        [vZ.x, vZ.y, vY.z, 0],
        [eye.x, eye.y, eye.z, 1]
    ]
    return Mat4(inverseMatrix).invert()

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
        self.ambient = 1 # The amount of light if no light is present
        self.camera = None # Holds the data for the camera

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
            o.update(self.camera)

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
                lightFactor = 0
                for l in self.lights:
                    lightFactor += ((distance3d(Vec3(o.polys[k].getPoints()[0].getX(), o.polys[k].getPoints()[0].getY(), v), l.position) / l.radius) * l.intensity)

                # Turn c into color_rgb
                c = c.getColorRGB(lightFactor, self.ambient)

                # Draw polygon
                o.polys[k].draw(self.window)
                o.polys[k].setFill(c)

                if o.wireframe == False:
                    o.polys[k].setOutline(c)
                else:
                    o.polys[k].setOutline("black")

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

    def delLight(self, light):
        """Removes a light from the scene"""
        self.lights.remove(light)

    def addCamera(self, camera):
        """Adds a camera into the scene"""
        self.camera = camera

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
        self.wireframe = False

        # Populate vertices if none were provided
        if vertices == None:
            self._populateVertices()
        else:
            self.vertices = vertices

        # Generate polygons
        self.genPolygons()

    def genPolygons(self, camera = None):
        """When called it generates polygons from the points given"""
        # Count by threes because a triangle has three points and
        # a mesh is made out of three points

        # Create matrices
        # Initialize matrices to identity matrices
        projection = Mat4([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])
        view = Mat4([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])
        model = Mat4([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]])

        # Set projection and view
        if camera != None:
            projection = camera.getPerspective()
            view = camera.getView()

        # Convert to radians
        xRot = self.rotation.x * (3.14/180)
        yRot = self.rotation.y * (3.14/180)
        zRot = self.rotation.z * (3.14/180)

        # Translate, rotate, and scale the model matrix
        # Translate
        translateMatrix = Mat4([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [self.position.x, self.position.y, self.position.z, 1]])
        # Rotate
        rotationMatrixX = Mat4([
                                [1, 0, 0, 0],
                                [0, math.cos(xRot), -math.sin(xRot), 0],
                                [0, math.sin(xRot), math.cos(xRot), 0],
                                [0, 0, 0, 1]
                              ])
        rotationMatrixY = Mat4([
                                [math.cos(yRot), 0, math.sin(yRot), 0],
                                [0, 1, 0, 0],
                                [-math.sin(yRot), 0, math.cos(yRot), 0],
                                [0, 0, 0, 1]
                              ])
        rotationMatrixZ = Mat4([
                                [math.cos(zRot), -math.sin(zRot), 0, 0],
                                [math.sin(zRot), math.cos(zRot), 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]
                              ])
        # Scale
        scaleMatrix = Mat4([[self.scale.x, 0, 0, 0], [0, self.scale.y, 0, 0], [0, 0, self.scale.z, 0], [0, 0, 0, 1]])
        # Make one singular rotation matrix
        rotationMatrixAll = rotationMatrixX.multiply4x4(rotationMatrixY).multiply4x4(rotationMatrixZ)
        # Put it all together
        model = translateMatrix.multiply4x4(rotationMatrixAll).multiply4x4(scaleMatrix)

        # Calculate MVP matrix
        modelviewprojection = projection.multiply4x4(view).multiply4x4(model)

        # Make each polygon
        for i in range(0, len(self.vertices), 3):
            # Get the vertices from the array
            v1 = self.vertices[i].getCopy()
            v2 = self.vertices[i + 1].getCopy()
            v3 = self.vertices[i + 2].getCopy()

            # Multiply the points by the given MVP matrix
            vr1 = modelviewprojection.multiplyVec(v1)
            vr2 = modelviewprojection.multiplyVec(v2)
            vr3 = modelviewprojection.multiplyVec(v3)

            # Put points on the screen
            p1 = convert3d2d(vr1, self.position)
            p2 = convert3d2d(vr2, self.position)
            p3 = convert3d2d(vr3, self.position)

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

    def update(self, camera):
        """Updates the object"""
        # Update the vertices positions
        self.polys = [] # Clear array
        self.polyAreas = [] # Clear array
        self.genPolygons(camera)

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
            Vec3(-1, -1, 1), Vec3(-1, 1, 1), Vec3(1, 1, 1),  # Triangle 1 (left)
            Vec3(-1, -1, 1), Vec3(1, -1, 1), Vec3(1, 1, 1),  # Triangle 2 (right)
            # Left
            Vec3(-1, -1, 1), Vec3(-1, -1, -1), Vec3(-1, 1, -1),  # Triangle 1 (left)
            Vec3(-1, -1, 1), Vec3(-1, 1, 1), Vec3(-1, 1, -1),  # Triangle 2 (right)
            # Right
            Vec3(1, -1, 1), Vec3(1, -1, -1), Vec3(1, 1, -1),  # Triangle 1 (left)
            Vec3(1, -1, 1), Vec3(1, 1, 1), Vec3(1, 1, -1),  # Triangle 2 (right)
            # Top
            Vec3(-1, -1, 1), Vec3(1, -1, 1), Vec3(1, -1, -1),  # Triangle 1 (left)
            Vec3(-1, -1, 1), Vec3(-1, -1, -1), Vec3(1, -1, -1),  # Triangle 2 (right)
            # Bottom
            Vec3(-1, 1, 1), Vec3(1, 1, 1), Vec3(1, 1, -1),  # Triangle 1 (left)
            Vec3(-1, 1, 1), Vec3(-1, 1, -1), Vec3(1, 1, -1),  # Triangle 2 (right)
            # Back
            Vec3(-1, -1, -1), Vec3(-1, 1, -1), Vec3(1, 1, -1),  # Triangle 1 (left)
            Vec3(-1, -1, -1), Vec3(1, -1, -1), Vec3(1, 1, -1)  # Triangle 2 (right)
        ]

class Model(RenderObject):
    """A renderable object by .obj files"""
    def __init__(self, path, position=Vec3(0, 0, 0), rotation=Vec3(0, 0, 0), scale=Vec3(1, 1, 1), color=color_rgb(255, 255, 255)):
        # Initialize the objects variables
        self.vertices = []  # Indices are chosen via the way the points are given
        self.polys = []  # Create empty array of all the polygons
        self.polyAreas = []  # Create empty array of all the depths for the polygons

        # Set the variables for keeping space
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.color = color
        self.wireframe = False

        # Populate vertices with the read file
        self.path = path
        self._populateVertices()

        # Generate polygons
        self.genPolygons()

    def _populateVertices(self):
        # Initialize the vertices
        self.vertices = loadObj(self.path)

class Light:
    def __init__(self, position, intensity, radius):
        # Initialize variables
        self.position = position
        self.intensity = intensity
        self.radius = radius

class Camera:
    def __init__(self, position, rotation, fov, ratio):
        # Initialize variables
        self.position = position
        self.rotation = rotation
        self.farClip = 100
        self.nearClip = 1
        self.fov = fov
        self.ratio = ratio
        self.up = Vec3(0, 1, 0)

    def getPerspective(self):
        """Returns a perspective matrix"""
        scale = 1 / (math.tan((self.fov / 2) * (3.14 / 180)))
        result = Mat4([
            [scale, 0, 0, 0],
            [0, scale, 0, 0],
            [0, 0, -self.farClip / (self.farClip - self.nearClip), -1],
            [0, 0, -self.farClip * self.nearClip / (self.farClip - self.nearClip), 0]
        ])
        return result

    def getView(self):
        """Returns the view matrix"""
        return lookAt(self.position, self.rotation, self.up)

# Run the main function if this file is ran
def main():
    print("Generating window")
    window = Window3d("Test graphics", 640, 480)

    print("Generating camera")
    cam = Camera(Vec3(0, 0, 0), Vec3(0, 0, 1), 45, 640/480)
    window.addCamera(cam)

    print("Generating light")
    l = Light(Vec3(320, 100, 100), 1, 2)
    window.addLight(l)

    print("Generating model")
    mdl = Cube(Vec3(320, 240, 0), Vec3(0, 0, 0), Vec3(100, 100, 100), Color(255, 0, 0))
    mdl.render(window)

    while True:
        keysPressed = window.window.checkKeys()
        if "w" in keysPressed:
            mdl.rotate(Vec3(2, 0, 0))
        if "s" in keysPressed:
            mdl.rotate(Vec3(-2, 0, 0))

        if "a" in keysPressed:
            mdl.rotate(Vec3(0, 2, 0))
        if "d" in keysPressed:
            mdl.rotate(Vec3(0, -2, 0))

        if "q" in keysPressed:
            mdl.rotate(Vec3(0, 0, 2))
        if "e" in keysPressed:
            mdl.rotate(Vec3(0, 0, -2))

        if "c" in keysPressed:
            mdl.setScale(add3d(Vec3(2, 2, 2), mdl.scale))
        if "v" in keysPressed:
            mdl.setScale(add3d(Vec3(-2, -2, -2), mdl.scale))

        if "Escape" in keysPressed:
            print("Exitting")
            break

        window.update()
        sleep(0.01)

    #window.window.getMouse()


if __name__ == "__main__":
    main()
