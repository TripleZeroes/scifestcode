import pygame
import time
import random
from game import *
import neat
from snake import *
import math
import statistics
from functools import reduce

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
  BLACK = (0, 0, 0)
  SNAKE_BLOCK = 10
  SNAKE_SPEED = 30
  DRAW_DETAILS = True

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
  def draw_from_top(self, components):
    y = 0
    for part in components:
      value = self.score_font.render(f"{part[0]}: {part[1]}", True, self.BLACK)
      self.dis.blit(value, [0, y])
      y += 30
  
  def draw_from_bottom(self, components):
    y = -60
    for part in components:
      value = self.score_font.render(f"{part[0]}: {part[1]}", True, self.BLACK)
      self.dis.blit(value, [0, (self.ROW_NUM * self.SNAKE_BLOCK) + y])
      y -= 30
  
  # still UI but snake_list is parts in snake  
  def draw_snake(self):
    for pos in self.game.snake.body:
      pygame.draw.rect(self.dis, self.RED, [pos.col * self.SNAKE_BLOCK, pos.row * self.SNAKE_BLOCK, self.SNAKE_BLOCK, self.SNAKE_BLOCK])

  # pure UI
  def draw_message(self, msg, colour): 
    mesg = self.font_style.render(msg, True, colour)
    self.dis.blit(mesg, [self.dis_x/6, self.dis_y/2])

  def get_fitness(self, **kwargs):
    parts = []
    for x in kwargs:
      parts.append((x, kwargs[x]))
    return parts

  def train_ai(self, genome, config, draw=True):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    start_time = time.time()
    duration = 0
    max_score = 150
    max_time = 60
    previous_decision = Directions.NONE
    duplicate_decisions = 0
    previous_closer = False
    good_decicion = False
    closer = False
    apple_eaten = False

    crossed_apple = {
      Directions.RIGHT: False,
      Directions.LEFT: False,
      Directions.UP: False,
      Directions.DOWN: False
    }

    def reset_map():
      crossed_apple[Directions.RIGHT] = False
      crossed_apple[Directions.LEFT] = False
      crossed_apple[Directions.DOWN] = False
      crossed_apple[Directions.UP] = False

    previous_distance_from_apple = math.sqrt(math.pow(self.game.snake.head_loc.row - self.game.apple_loc.row, 2) +
                                      math.pow(self.game.snake.head_loc.col - self.game.apple_loc.col, 2))
    first_checked = False
    amount_of_retakes = 0
    retake = False
    new_directions = 0
    new_direction = False
    ai_score = 1
    first_apple_points = 0
    ticks = 0
    while not self.game.is_game_over:
      should_break = False
      #Normal inputs, soon to be refactored      
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          quit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_d:
            AI_Game.DRAW_DETAILS = not AI_Game.DRAW_DETAILS
          elif event.key == pygame.K_b:
            should_break = True

      if should_break:
        break

      distance_from_apple = math.sqrt(math.pow(self.game.snake.head_loc.row - self.game.apple_loc.row, 2) +
                                      math.pow(self.game.snake.head_loc.col - self.game.apple_loc.col, 2))
      previous_closer = closer
      closer = previous_distance_from_apple > distance_from_apple

      if new_direction:
        good_decicion = closer
        new_direction = False
        if not good_decicion:
          reset_map()
      
      if not retake:
        ticks += 1/25

      if previous_closer and not closer:
        crossed_apple[self.game.snake.direction] = True
        crossed_apple[Directions.opposites[self.game.snake.direction]] = False

      apple_mult = 4/(self.game.score + 1)
      if new_directions > 0:
        if closer:
          if not crossed_apple[Directions.opposites[self.game.snake.direction]]:
            first_apple_points += apple_mult
        elif not good_decicion:
          first_apple_points -= apple_mult

        
      # if new_direction:
      #   previous_closer = closer
      #   closer = previous_distance_from_apple > distance_from_apple
      #   # moving closer twice in a row
      #   if closer and previous_closer:
      #     first_apple_points += 4#100/distance_from_apple
      #   elif not closer and not previous_closer:
      #     first_apple_points -= 4
      #     pass
      #   new_direction = False

          #first_apple_points -= 100/distance_from_apple
        #first_apple_points += (1/distance_from_apple) * (1 if previous_distance_from_apple > distance_from_apple else -1)
      previous_distance_from_apple = distance_from_apple

      cell_num = AI_Game.ROW_NUM * AI_Game.COL_NUM
      empty_cell_num = cell_num - 2 - self.game.score # 2 for head and apple
      # input = [0] * empty_cell_num * 2 # row and col of empty grids
      # for loc in reversed(self.game.snake.body):
      #   input.append(loc.row)
      #   input.append(loc.col)
      input = []
      # head loc/distance to top and left
      input.append(self.game.snake.head_loc.row)
      input.append(self.game.snake.head_loc.col)
      # apple loc
      input.append(self.game.apple_loc.row)
      input.append(self.game.apple_loc.col)
      # distance to right and bottom
      input.append(AI_Game.ROW_NUM - self.game.snake.head_loc.row)
      input.append(AI_Game.COL_NUM - self.game.snake.head_loc.col)
      # which way is the snake facing
      input.append(10 if self.game.snake.direction == Directions.UP else 0)
      input.append(10 if self.game.snake.direction == Directions.DOWN else 0)
      input.append(10 if self.game.snake.direction == Directions.LEFT else 0)
      input.append(10 if self.game.snake.direction == Directions.RIGHT else 0)
      # absolut distance from apple
      input.append(distance_from_apple)
      # x and y difference from head to apple
      input.append(self.game.snake.head_loc.row - self.game.apple_loc.row)
      input.append(self.game.snake.head_loc.col - self.game.apple_loc.col)
      # number of back and forth
      input.append(amount_of_retakes)
      # previous decision
      input.append(previous_decision)
      input.append(1 if not retake else -1)

      output = net.activate(input)
      decision = output.index(max(output))
      if (decision == previous_decision and decision != Directions.NONE):
        duplicate_decisions += 1
      
      previous_decision = decision

      if decision == Directions.opposites[self.game.snake.direction]:
        amount_of_retakes += 1
        if decision != Directions.NONE:
          retake = True
        if amount_of_retakes >= 50:
          break
      elif (decision != Directions.NONE and decision != self.game.snake.direction) or apple_eaten:
          new_directions += 1
          retake = False
          new_direction = True
      apple_eaten = False

      current_score = self.game.score
      self.game.update(decision)
      if self.game.score != current_score:
        apple_eaten = True
        reset_map()
        closer = False
        new_direction = False
        new_directions = 0
        retake = False
        previous_decision = Directions.NONE

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

        ai_score = self.game.score

        distance_score = first_apple_points #if new_directions > 2 else 0
        if ai_score == 1 and new_directions == 1:
            ai_score = 0
        
        fitness_parts = self.get_fitness(
          apples=ai_score * 400,
          retakes=-amount_of_retakes,
          distance=distance_score,
          decision=-duplicate_decisions,
          ticks=ticks
        )


        # mostly UI, score is kinda useful
        self.draw_snake()
        if AI_Game.DRAW_DETAILS:
          fitness_parts.append(("fitness", reduce(lambda sum, part: sum + part[1], fitness_parts, 0))) 
          self.draw_from_top(fitness_parts)

          stats = [
            ("duration", duration),
            ("good_decicion", good_decicion),
            ("new_directions", new_directions),
            ("closer", closer)
          ]

          self.draw_from_bottom(stats)
        
        pygame.draw.rect(self.dis, self.BLUE, [self.game.snake.head_loc.col * self.SNAKE_BLOCK, self.game.snake.head_loc.row * self.SNAKE_BLOCK,
                                                self.SNAKE_BLOCK, self.SNAKE_BLOCK])
        pygame.display.update()
      
      duration = time.time() - start_time

      if self.game.score == max_score or duration >= max_time:
        break
      self.clock.tick(self.SNAKE_SPEED)
      
    duration = time.time() - start_time

    new_distance_score = first_apple_points #if self.game.score == 0 else 0
    distance_score = new_distance_score #if new_directions > 2 else 0
    ai_score = self.game.score
    
    if ai_score == 1 and new_directions == 1:
        ai_score = 0
    
    new_directions -= 2

    fitness_parts = self.get_fitness(
      apples=ai_score * 400,
      retakes=-amount_of_retakes,
      distance=distance_score,
      decision=-duplicate_decisions,
      ticks=ticks
    )
    #genome.fitness = (ai_score * 100) - amount_of_retakes + new_distance_score - duplicate_decisions + ticks 
    genome.fitness = reduce(lambda sum, part: sum + part[1], fitness_parts, 0)
