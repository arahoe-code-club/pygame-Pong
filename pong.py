import pygame


class PyGameObject:
  """Represents a paddle object"""

  def __init__(self, width, height):
    self.hitbox = pygame.Rect(0 - width / 2, 0 - height / 2, width, height)
    self.movement = pygame.Vector2(0, 0)
    self.color = "white"
    self.movement_inversion_factor = 1
    self.thickness = 0

  @property
  def x(self):
    return self.hitbox.centerx

  @x.setter
  def x(self, value: float):
    self.hitbox.centerx = value

  @property
  def y(self):
    return self.hitbox.centery

  @y.setter
  def y(self, value: float):
    self.hitbox.centery = value

  @property
  def width(self):
    return self.hitbox.width

  @width.setter
  def width(self, value: float):
    self.hitbox.width = value

  @property
  def height(self):
    return self.hitbox.height

  @height.setter
  def height(self, value: float):
    self.hitbox.height = value

  def drawProperties(self):
    """Get the properties to use in pygame draw"""
    return self.color, self.hitbox, self.thickness

  def invertMovement(self):
    """change the movement direction"""
    self.movement_inversion_factor *= -1

  def changeMovement(self, movementVector):
    self.movement = movementVector

  def move(self):
    if not (self.movement.x == 0 and self.movement.y == 0):
      vector = self.movement.copy()
      vector.x *= self.movement_inversion_factor
      vector.y *= self.movement_inversion_factor
      self.hitbox.move_ip(vector.x, vector.y)

  @classmethod
  def newPaddle(cls, width, height):
    return cls(width, height)

  @classmethod
  def newBall(cls, radius):
    ball =  cls(radius, radius)
    ball.thickness = radius
    return ball
