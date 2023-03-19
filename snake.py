from grid import *

class Directions():
    NONE = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

class Snake():
  head_loc = None
  body = []
  direction = Directions.NONE

  def __init__(self, head: Location) -> None:
    self.head_loc = head