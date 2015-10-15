import autouml
import random

@autouml.sequence_dia
class Dice():
  '''
  Just a random point in segment [0,radius]
  '''
  def __init__(self, radius=1):
    self.radius = radius

  def roll(self):
    return random.random()*self.radius

  def rpoint(self):
    return Point(self.roll(), self.roll())
    
@autouml.sequence_dia
class Circle():
  '''
  A circle centered in (0,0) with radius r
  '''
  def __init__(self, radius=1):
    self.radius = radius
    self.__inside=0.
    self.__total=0.
    self.dice=Dice(self.radius)

  def is_inside(self, point):
    return  point.x**2 + point.y**2 < self.radius**2

  def shot(self, point):
    self.__total+=1
    if self.is_inside(point):
      self.__inside+=1

  def rshot(self, n=1):
    for i in range(n):
      self.shot(self.dice.rpoint())


  @property
  def pi(self):
    return 4*self.__inside/self.__total

@autouml.sequence_dia
class Point():
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __str__(self):
    return '(%s, %s)' % (self.x, self.y)

c=Circle(1)
for i in range(3):
  c.rshot(3)
  print c.pi
