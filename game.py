import random
from grid import *
from snake import *


class GameState():
    grid = Grid(11, 11)
    snake = Snake(Location(5, 5))
    apple_loc = None
    
    def __init__(self) -> None:
        self.create_new_apple()
        self.grid.update_cell(self.snake.head_loc, Cellstate.SNAKE_HEAD)
        self.grid.update_cell(self.apple_loc, Cellstate.APPLE)


    def create_new_apple(self):
        apple_row = random.randrange(0, self.grid.row_num)
        apple_col = random.randrange(0, self.grid.col_num)
        self.apple_loc = Location(apple_row, apple_col)


    def pront(self):
        for row in self.grid.cells:
            for value in row:
                print(value, end = " ")
            print("\n")
    
    def head_check(self):
        if self.apple_loc == self.snake.head_loc:
              create_new_apple()

if __name__ == "__main__":
    game = GameState()
    game.pront()
    
