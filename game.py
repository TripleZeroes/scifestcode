import math
import random
from grid import *
from snake import *


class GameState(): 
    grid: Grid
    snake: Snake
    apple_loc = None
    is_game_over = False

    @property
    def score(self):
        return len(self.snake.body)

    def __init__(self, row_num, col_num) -> None:
        self.grid = Grid(row_num, col_num)
        self.snake = Snake(Location(math.floor(row_num/2), math.floor(col_num/2)))
        apple_locs = [
            Location(math.floor(.25 * row_num), math.floor(.25 * col_num)),
            Location(math.floor(.25 * row_num), math.floor(.75 * col_num)),
            Location(math.floor(.75 * row_num), math.floor(.25 * col_num)),
            Location(math.floor(.75 * row_num), math.floor(.75 * col_num)),
        ]
        self.apple_loc = apple_locs[random.randrange(0, len(apple_locs))]
        self.grid.update_cell(self.snake.head_loc, Cellstate.SNAKE_HEAD)
        self.grid.update_cell(self.apple_loc, Cellstate.APPLE)


    def create_new_apple(self):
        empty = []
        for row in range(self.grid.row_num):
            for col in range(self.grid.col_num):
                if self.grid.cells[row][col] == Cellstate.EMPTY:
                    empty.append(Location(row, col))
        index = random.randrange(0, len(empty))
        new_loc = empty[index]
        self.apple_loc = new_loc

    def update(self, new_input):
        # if none, move in same direction
        if new_input == Directions.NONE:
            new_direction = self.snake.direction
        else:
            # else, move in new direction 
            new_direction = new_input

        if len(self.snake.body) > 0 and Directions.opposites[new_direction] == self.snake.direction:
            new_direction = self.snake.direction
        

        
        last_body = self.snake.shift_snake(new_direction)
        if last_body is not None:
            self.grid.update_cell(last_body, Cellstate.EMPTY)
        self.game_over()
        self.head_check()
        if not self.is_game_over:
            self.grid.update_cell(self.snake.head_loc, Cellstate.SNAKE_HEAD)

    def game_over(self):
        #edges
        if self.snake.head_loc.row > self.grid.row_num - 1:
            self.is_game_over = True
        if self.snake.head_loc.col > self.grid.col_num - 1:
            self.is_game_over = True
        if self.snake.head_loc.row < 0:
            self.is_game_over = True
        if self.snake.head_loc.col < 0:
            self.is_game_over = True
        #head hits body
        for location in self.snake.body:
            if location == self.snake.head_loc:
                self.is_game_over = True
                break


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
            self.snake.should_grow = True

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
        
    
