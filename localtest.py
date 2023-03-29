import pygame
import time
import random
from game import *

# UI
pygame.init()

COL_NUM = 51
ROW_NUM = 51

green = (0, 255, 100)
white = (255, 255, 255)
yellow = (255, 255, 102)
blue = (0, 0, 255)
red = (255,0,0)
aqua = (0, 255, 255)

# UI
snake_block = 10

dis_x = COL_NUM * snake_block
dis_y = ROW_NUM * snake_block

snake_speed = 15


dis = pygame.display.set_mode((dis_x, dis_y))
dis.fill(green)

pygame.display.set_caption('I like snake')

clock = pygame.time.Clock()


font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


#UI but score is length of snake so it could be useful
def Your_score(game):
    value = score_font.render("Your Score: " + str(game.score), True, yellow)
    dis.blit(value, [0, 0])
 
# still UI but snake_list is parts in snake  
def our_snake(game):
  for pos in game.snake.body:
    pygame.draw.rect(dis, red, [pos.col * snake_block, pos.row * snake_block, snake_block, snake_block])

# pure UI
def message(msg, colour): 
  mesg = font_style.render(msg, True, colour)
  dis.blit(mesg, [dis_x/6, dis_y/2])
 

def checkGameClose(game):
  while True:
    dis.fill(aqua)
    message("Q: quit, C: continue", green)
    Your_score(game)

    pygame.display.update()
    #UI/ ending inputs, not useful for AI
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
          return True
        elif event.key == pygame.K_c:
          return False
      if event.type == pygame.QUIT:
        return True

def gameLoop():
  game = GameState(ROW_NUM, COL_NUM) 

  while not game.is_game_over:
    input_given = False
    #Normal inputs, soon to be refactored      
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
          game.update(Directions.UP) 
          input_given = True
        elif event.key == pygame.K_LEFT:
          game.update(Directions.LEFT)  
          input_given = True

        elif event.key == pygame.K_DOWN:
          game.update(Directions.DOWN)   
          input_given = True

        elif event.key == pygame.K_RIGHT:
          game.update(Directions.RIGHT)   
          input_given = True

    if not input_given:
      game.update(Directions.NONE)

    # game tick things, mostly UI 
    dis.fill(white)
    
    pygame.draw.rect(dis, green, [game.apple_loc.col * snake_block, game.apple_loc.row * snake_block, snake_block, snake_block])
    # snake head is useful? otherwise UI



    # mostly UI, score is kinda useful
    our_snake(game)
    Your_score(game)
    
    pygame.draw.rect(dis, blue, [game.snake.head_loc.col * snake_block, game.snake.head_loc.row * snake_block, snake_block, snake_block])
    pygame.display.update()

  #check for eating food
    # if xpos == foodx and ypos == foody:
    #     foodx = round(random.randrange(0, dis_x - snake_block) / 10.0) * 10.0
    #     foody = round(random.randrange(0, dis_y - snake_block) / 10.0) * 10.0
    #     length_of_snake += 1
    #if not input_given:
    clock.tick(snake_speed)
  return game  

def mainLoop():
  game_close = False
  while not game_close:
    game = gameLoop() 
    game_close = checkGameClose(game)
  pygame.quit()
  quit()
     
mainLoop()