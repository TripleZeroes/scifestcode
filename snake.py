from typing import List
from grid import *
from game import *

class Directions():
  NONE = 0
  UP = 1
  RIGHT = 2
  DOWN = 3
  LEFT = 4

  opposites = {
    RIGHT: LEFT,
    LEFT: RIGHT,
    UP: DOWN,
    DOWN: UP,
    NONE: NONE
  }



class Snake():
  head_loc: Location
  body: List[Location]
  direction: Directions = Directions.NONE
  should_grow: bool = False

  def __init__(self, head: Location) -> None:
    self.head_loc = head
    self.body = []
    self.direction = Directions.NONE
    self.should_grow = False

  def shift_snake(self, direction):
    self.direction = direction
    if self.direction == Directions.NONE:
      return
    
    last_body = None
    self.body.append(Location(self.head_loc.row, self.head_loc.col))
    if not self.should_grow:
      last_body = self.body[0]
      del self.body[0]
    else:
      self.should_grow = False

    def move_up():
      self.head_loc.row -= 1

    def move_down():
      self.head_loc.row += 1

    def move_left():
      self.head_loc.col -= 1

    def move_right():
      self.head_loc.col += 1

    movements = {
      Directions.UP: move_up,
      Directions.DOWN: move_down,
      Directions.LEFT: move_left,
      Directions.RIGHT: move_right,
    }

    movements[direction]() 
    return last_body
