class Cellstate():
    APPLE = 0
    SNAKE_HEAD = 1
    SNAKE_BODY = 2
    EMPTY = 3

class Location():
  row = 0
  col = 0

  def __init__(self, row, col) -> None:
    self.row = row
    self.col = col

class Grid():
    col_num = None
    row_num = None
    cells = []

    def __init__(self, row_num, col_num) -> None:
        self.row_num = row_num
        self.col_num = col_num
        self.cells = [[Cellstate.EMPTY for i in range(col_num)] for j in range(row_num)]

    def update_cell(self, location: Location, new_state: Cellstate):
       self.cells[location.row][location.col] = new_state
       

