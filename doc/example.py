import autouml
import autouml.log
import numpy

autouml.set_options(show_arguments=True, use_instance_ids=True)

# We also want to decorate all methods in numpy module
autouml.sequence_dia(numpy.random)


@autouml.sequence_dia
class Dice(object):
    '''
    Just a random point in segment [0,radius]
    '''
    radius = None

    def __str__(self):
        return 'Dice(%s)' % self.radius

    def __init__(self, radius=1):
        self.radius = radius

    def roll(self):
        return numpy.random.random() * self.radius

    def rpoint(self):
        return Point(self.roll(), self.roll())


@autouml.sequence_dia
class Circle(object):
    '''
    A circle centered in (0,0) with radius r
    '''
    radius = None

    def __init__(self, radius=1):
        self.radius = radius
        self.__inside = 0.
        self.__total = 0.
        self.dice = Dice(self.radius)

    def __str__(self):
        return 'Circle(%s)' % self.radius

    def is_inside(self, point):
        return point.x**2 + point.y**2 < self.radius**2

    def shot(self, point):
        self.__total += 1
        if self.is_inside(point):
            self.__inside += 1

    def rshot(self, n=1):
        for i in range(n):
            self.shot(self.dice.rpoint())

    @property
    def pi(self):
        return 4 * self.__inside / self.__total


@autouml.sequence_dia
class Point(object):
    x = None
    y = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'Point(%s, %s)' % (self.x, self.y)

c = Circle(1)
c.rshot(3)
print c.pi
