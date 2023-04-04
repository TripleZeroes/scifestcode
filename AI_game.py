import pygame
import time
import random
from game import *
import neat
from snake import *
import math
import statistics

pygame.init()

class AI_Game:
  COL_NUM = 51
  ROW_NUM = 51
  GREEN = (0, 255, 100)
  WHITE = (255, 255, 255)
  YELLOW = (255, 255, 102)
  BLUE = (0, 0, 255)
  RED = (255,0,0)
  AQUA = (0, 255, 255)
  SNAKE_BLOCK = 10
  SNAKE_SPEED = 30

  def __init__(self):
    self.dis_x = AI_Game.COL_NUM * AI_Game.SNAKE_BLOCK
    self.dis_y = AI_Game.ROW_NUM * AI_Game.SNAKE_BLOCK
    self.dis = pygame.display.set_mode((self.dis_x, self.dis_y))
    self.dis.fill(AI_Game.GREEN)
    self.game = GameState(AI_Game.ROW_NUM, AI_Game.COL_NUM) 

    pygame.display.set_caption('I like snake')

    self.clock = pygame.time.Clock()


    self.font_style = pygame.font.SysFont("bahnschrift", 25)
    self.score_font = pygame.font.SysFont("comicsansms", 35)


    #UI but score is length of snake so it could be useful
  def draw_score(self):
    value = self.score_font.render("Your Score: " + str(self.game.score), True, self.YELLOW)
    self.dis.blit(value, [0, 0])
  
  # still UI but snake_list is parts in snake  
  def draw_snake(self):
    for pos in self.game.snake.body:
      pygame.draw.rect(self.dis, self.RED, [pos.col * self.SNAKE_BLOCK, pos.row * self.SNAKE_BLOCK, self.SNAKE_BLOCK, self.SNAKE_BLOCK])

  # pure UI
  def draw_message(self, msg, colour): 
    mesg = self.font_style.render(msg, True, colour)
    self.dis.blit(mesg, [self.dis_x/6, self.dis_y/2])



  def train_ai(self, genome, config, draw=True):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    start_time = time.time()

    max_score = 150
    max_time = 60

  
    first_checked = False
    amount_of_retakes = 0
    new_directions = 0
    ai_score = 1
    distances = []
    move_penalty = 0
    while not self.game.is_game_over:
      #Normal inputs, soon to be refactored      
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          quit()

      input = [j for sub in self.game.grid.cells for j in sub]
      input.append(self.game.snake.direction)
      output = net.activate(input)
      decision = output.index(max(output))

      if decision == Directions.opposites[self.game.snake.direction]:
        amount_of_retakes += 1
        if amount_of_retakes >= 20:
          move_penalty = 1000
          break
      elif decision != Directions.NONE and decision != self.game.snake.direction:
          new_directions += 1
      


      self.game.update(decision)

      distance_from_apple = math.sqrt(math.pow(self.game.snake.head_loc.row - self.game.apple_loc.row, 2) +
                                      math.pow(self.game.snake.head_loc.col - self.game.apple_loc.col, 2))
      distances.append(distance_from_apple)

      if first_checked == False:
        if decision == 0:
          break
        else:
          first_checked = True
      if draw:
      
        # game tick things, mostly UI 
        self.dis.fill(self.WHITE)
        
        pygame.draw.rect(self.dis, self.GREEN, [self.game.apple_loc.col * self.SNAKE_BLOCK, self.game.apple_loc.row * self.SNAKE_BLOCK,
                                                 self.SNAKE_BLOCK, self.SNAKE_BLOCK])
        # snake head is useful? otherwise UI



        # mostly UI, score is kinda useful
        self.draw_snake()
        self.draw_score()
        
        pygame.draw.rect(self.dis, self.BLUE, [self.game.snake.head_loc.col * self.SNAKE_BLOCK, self.game.snake.head_loc.row * self.SNAKE_BLOCK,
                                                self.SNAKE_BLOCK, self.SNAKE_BLOCK])
        pygame.display.update()
      
      duration = time.time() - start_time

      if self.game.score == max_score or duration >= max_time:
        break
      self.clock.tick(self.SNAKE_SPEED)
      
    duration = time.time() - start_time

    mean_distance = distances[0] - statistics.mean(distances)  
    new_distance_score = (1/(mean_distance if mean_distance != 0 else 1)) * 20
    
    ai_score = self.game.score

    if ai_score == 1 and new_directions == 1:
        ai_score = 0

    genome.fitness = (ai_score * 100) + duration - amount_of_retakes + (new_directions * 1.5) + new_distance_score - move_penalty
