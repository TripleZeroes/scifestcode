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

    def update(self, new_input):
        # if none, move in same direction
        if new_input == Directions.NONE:
            new_direction = self.snake.direction
        # else, move in new direction 
        else:
            new_direction = new_input
        
        self.snake.direction = new_direction
        if self.snake.direction == Directions.NONE:
            return

        def move_up():
            self.snake.head_loc.row -= 1

        def move_down():
            self.snake.head_loc.row += 1

        def move_left():
            self.snake.head_loc.col -= 1

        def move_right():
            self.snake.head_loc.col += 1

        movements = {
            Directions.UP: move_up,
            Directions.DOWN: move_down,
            Directions.LEFT: move_left,
            Directions.RIGHT: move_right,
        }

        self.grid.update_cell(self.snake.head_loc, Cellstate.EMPTY)
        movements[self.snake.direction]()
        self.grid.update_cell(self.snake.head_loc, Cellstate.SNAKE_HEAD)


    def pront(self):

        printr_value = {
            Cellstate.EMPTY: "▢",
            Cellstate.APPLE: "◑",
            Cellstate.SNAKE_HEAD: "◈"
        }
        

        for row in self.grid.cells:
            for value in row:
                print(printr_value[value], end = " ")
            print("\n")
    
    def head_check(self):
        if self.apple_loc == self.snake.head_loc:
            self.create_new_apple()

if __name__ == "__main__":
    import os
    from time import sleep

    game = GameState()
    game.apple_loc = Location(game.snake.head_loc.row - 2, game.snake.head_loc.col)
    while game.snake.head_loc.row > -1:
        os.system("cls")
        game.head_check()
        game.pront()
        sleep(1)
        game.update(Directions.UP)
        
    
