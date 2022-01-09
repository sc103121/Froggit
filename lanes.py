"""
Lanes module for Froggit

This module contains the lane classes for the Frogger game. The lanes are the vertical
slice that the frog goes through: grass, roads, water, and the exit hedge.

Each lane is like its own level. It has hazards (e.g. cars) that the frog has to make
it past.  Therefore, it is a lot easier to program frogger by breaking each level into
a bunch of lane objects (and this is exactly how the level files are organized).

You should think of each lane as a secondary subcontroller.  The level is a subcontroller
to app, but then that subcontroller is broken up into several other subcontrollers, one
for each lane.  That means that lanes need to have a traditional subcontroller set-up.
They need their own initializer, update, and draw methods.

There are potentially a lot of classes here -- one for each type of lane.  But this is
another place where using subclasses is going to help us A LOT.  Most of your code will
go into the Lane class.  All of the other classes will inherit from this class, and
you will only need to add a few additional methods.

If you are working on extra credit, you might want to add additional lanes (a beach lane?
a snow lane?). Any of those classes should go in this file.  However, if you need additional
obstacles for an existing lane, those go in models.py instead.  If you are going to write
extra classes and are now sure where they would go, ask on Piazza and we will answer.

Shawn Chen(sc2489)
December 21, 2020
"""
from game2d import *
from consts import *
from models import *

# PRIMARY RULE: Lanes are not allowed to access anything in any level.py or app.py.
# They can only access models.py and const.py. If you need extra information from the
# level object (or the app), then it should be a parameter in your method.

class Lane(object):         # You are permitted to change the parent class if you wish
    """
    Parent class for an arbitrary lane.

    Lanes include grass, road, water, and the exit hedge.  We could write a class for
    each one of these four (and we will have classes for THREE of them).  But when you
    write the classes, you will discover a lot of repeated code.  That is the point of
    a subclass.  So this class will contain all of the code that lanes have in common,
    while the other classes will contain specialized code.

    Lanes should use the GTile class and to draw their background.  Each lane should be
    GRID_SIZE high and the length of the window wide.  You COULD make this class a
    subclass of GTile if you want.  This will make collisions easier.  However, it can
    make drawing really confusing because the Lane not only includes the tile but also
    all of the objects in the lane (cars, logs, etc.)
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE
    # Attribute _tile: the GTile object that a Lane object contains
    # Invariant: _tile is a GTile object

    # Attribute _lanePos: the position that tells us which lane it is, with value 0
    # for the bottom lane
    # Invariant: _lanePos is an int >= 0 and less than or equal to the total number of lanes

    # Attribute _objs: the list of all obstacles on a particular lane
    # Invariant: _objs is a valid list of GImage objects

    # Attribute _laneSpeed: the speed of obstacles on a particular lane
    # Invariant: _laneSpeed is a valid int or float, or None if there is no obstacles

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getTile(self):
        """
        Getters for the _tile attribute.

        Returns a single GTile object that represents a tile.
        """
        return self._tile

    def getObjs(self):
        """
        Getters for the _objs attribute.

        Returns a list of GImage objects that represent obstacles on a particular lane.
        """
        return self._objs

    def getLaneSpeed(self):
        """
        Getters for the _laneSpeed attribute.

        Returns a valid int or float that represents the speed of obstacles on a lane.
        """
        return self._laneSpeed

    # INITIALIZER TO SET LANE POSITION, BACKGROUND,AND OBJECTS
    def __init__(self, width, tile, lanePos, objs):
        """
        Initializes a single lane at a given position with given obstacles

        Parameter width: the width of a single lane
        Precondition: A value width is a valid int greater than zero

        Parameter tile: the json dictionary that represents a single tile of lane
        Precondition: tile is a json dictionary

        Parameter lanePos: the position that tells us which lane it is, with value 0
        for the bottom lane
        Precondition: lanePos is an int >= 0 and less than or equal to the total
        number of lanes

        Parameter objs: the list of all obstacles on a particular lane
        Precondition: objs is a valid list of dictionaries with each dictionary specifies
        the type of the obstacle and position, or None if doesn't have any obstacles
        """
        self._lanePos = lanePos
        source = tile["type"] + '.png'
        self._tile = GTile(height = GRID_SIZE, width = width, source = source)
        self._tile.left = 0
        self._tile.bottom = lanePos * GRID_SIZE
        self._laneSpeed = None
        if "speed" in tile:
            self._laneSpeed = tile["speed"]

        self._objs = []
        if objs is not None:
            for k in objs:
                obj = GImage(y=self._tile.y, source = k["type"] + '.png')
                obj.x = (k["position"]+0.5) * GRID_SIZE
                if "speed" in tile and tile["speed"] < 0:
                    obj.angle = 180
                self._objs.append(obj)

    # ADDITIONAL METHODS (DRAWING, COLLISIONS, MOVEMENT, ETC)
    def draw(self, view):
        """
        Draws the each lane onto the screen.

        Parameter view: the game view which represents the window screen.
        Precondition: view is a valid GView object
        """
        self._tile.draw(view)
        if len(self._objs) != 0:
            for obj in self._objs:
                obj.draw(view)

    def update(self, dt, buffer):
        """
        Updates and animates the obstacles on a particular lane if there is any.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter buffer: the size of an offscreen buffer that an obstacle will wrap
        around.
        Precondition: buffer is an int that's greater than the length of the longest
        obstacle, or 0 if there is no obstacle on a particular lane
        """
        if self._laneSpeed is not None:
            d = 0
            for obj in self._objs:
                obj.x += dt * self._laneSpeed
                if obj.x > self._tile.width + buffer * GRID_SIZE:
                    d = obj.x - self._tile.width - buffer * GRID_SIZE
                    obj.x = -buffer * GRID_SIZE + d
                elif obj.x < -buffer * GRID_SIZE:
                    d = -buffer * GRID_SIZE - obj.x
                    obj.x = self._tile.width + buffer * GRID_SIZE - d


class Grass(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a 'safe' grass area.

    You will NOT need to actually do anything in this class.  You will only do anything
    with this class if you are adding additional features like a snake in the grass
    (which the original Frogger does on higher difficulties).
    """
    pass
    # ONLY ADD CODE IF YOU ARE WORKING ON EXTRA CREDIT EXTENSIONS.


class Road(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a roadway with cars.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, roads are different
    than other lanes as they have cars that can kill the frog. Therefore, this class
    does need a method to tell whether or not the frog is safe.
    """
    # DEFINE ANY NEW METHODS HERE
    def carCollision(self, frog):
        """
        Detects if the frog has collided with a car on this specific lane. Returns True
        if indeed the frog has collided and False otherwise.

        Parameter frog: the frog object which is a instance of GObject
        Precondition: frog is a valid Frog object and a instance of GObject
        """
        for obj in self._objs:
            if obj.collides(frog):
                return True
        return False


class Water(Lane):
    """
    A class representing a waterway with logs.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, water is very different
    because it is quite hazardous. The frog will die in water unless the (x,y) position
    of the frog (its center) is contained inside of a log. Therefore, this class needs a
    method to tell whether or not the frog is safe.

    In addition, the logs move the frog. If the frog is currently in this lane, then the
    frog moves at the same rate as all of the logs.
    """
    # ADDITIONAL METHODS
    def detectLog(self, x, y):
        """
        Detects if coordinate(x,y) is inside an log object. Returns True if (x,y) is
        inside and False otherwise.

        Parameter x: a valid x-coordinate
        Precondition: x is an int or float greater than or equal to 0

        Parameter y: a valid y-coordinate
        Precondition: y is an int or float greater than or equal to 0
        """
        import introcs
        for obj in self._objs:
            if obj.contains(introcs.Point2(x,y)):
                return True
        return False


class Hedge(Lane):
    """
    A class representing the exit hedge.

    This class is a subclass of lane because it does want to use a lot of the features
    of that class. But there is a lot more going on with this class, and so it needs
    several more methods.  First of all, hedges are the win condition. They contain exit
    objects (which the frog is trying to reach). When a frog reaches the exit, it needs
    to be replaced by the blue frog image and that exit is now "taken", never to be used
    again.

    That means this class needs methods to determine whether or not an exit is taken.
    It also need to take the (x,y) position of the frog and use that to determine which
    exit (if any) the frog has reached. Finally, it needs a method to determine if there
    are any available exits at all; once they are taken the game is over.

    These exit methods will require several additional attributes. That means this class
    (unlike Road and Water) will need an initializer. Remember to user super() to combine
    it with the initializer for the Lane.
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE
    # Attribute _exits: a list of of all exits inside a hedge
    # Invariant: _exits must be a valid list of GImage objects

    # Attribute _openings: a list of of all exits inside a hedge
    # Invariant: _openings must be a valid list of GImage objects

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getExits(self):
        """
        Getters for the attribute _exits. Returns the attribute as a list
        """
        return self._exits

    # INITIALIZER TO SET ADDITIONAL EXIT INFORMATION
    def __init__(self, width, tile, lanePos, objs, usedExits):
        """
        Initializes a single hedge lane at a given position with given obstacles

        Parameter width: the width of a single hedge lane
        Precondition: A value width is a valid int greater than zero

        Parameter tile: the json dictionary that represents a single tile of hedge lane
        Precondition: tile is a json dictionary

        Parameter lanePos: the position that tells us which hedge lane it is, with value 0
        for the bottom hedge lane
        Precondition: lanePos is an int >= 0 and less than the total number of lanes

        Parameter usedExits: the list of all exits already used/occupied
        Precondition: usedExits is a valid list of GImage objects
        """
        super().__init__(width, tile, lanePos, objs)
        self._exits = []
        self._openings = []
        for k in self.getObjs():
            if k.source == 'exit.png':
                self._exits.append(k)
            elif k.source == 'open.png':
                self._openings.append(k)

        if len(usedExits) > 0 and len(self._exits) > 0:
            for exit in usedExits:
                for open in self._exits:
                    if open.contains((exit.x, exit.y)):
                        self._exits.remove(open)

    def detectOpening(self, x, y):
        """
        Detects if coordinate(x,y) is inside an opening. Returns True if (x,y) is inside and
        False otherwise.

        Parameter x: a valid x-coordinate
        Precondition: x is an int or float greater than or equal to 0

        Parameter y: a valid y-coordinate
        Precondition: y is an int or float greater than or equal to 0
        """
        import introcs
        for open in self._openings:
            if open.contains(introcs.Point2(x,y)):
                return True
        return False

    def reachExit(self, x, y):
        """
        Detects if coordinate(x,y) is inside an exit, meaning the object has reached the exit.
        Returns True if (x,y) is inside and False otherwise. If (x,y) is inside an exit, this
        method will also remove the exit from the attribute self._exits since the exit is
        considered occupied.

        Parameter x: a valid x-coordinate
        Precondition: x is an int or float greater than or equal to 0

        Parameter y: a valid y-coordinate
        Precondition: y is an int or float greater than or equal to 0
        """
        import introcs
        for open in self._exits:
            if open.contains(introcs.Point2(x,y)):
                self._exits.remove(open)
                return True
        return False

# IF YOU NEED ADDITIONAL LANE CLASSES, THEY GO HERE
