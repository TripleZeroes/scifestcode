import pygame
import time
import random
from game import *

# UI
pygame.init()


game = GameState()

green = (0, 255, 100)
white = (255, 255, 255)
yellow = (255, 255, 102)
blue = (0, 0, 255)
red = (255,0,0)
aqua = (0, 255, 255)

# UI
snake_block = 10

dis_x = game.grid.col_num * snake_block
dis_y = game.grid.row_num * snake_block

# game data
game_over = False

# UI
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
    pygame.draw.rect(dis, red, [pos.row * snake_block, pos.col * snake_block, snake_block, snake_block])

# pure UI
def message(msg, colour): 
  mesg = font_style.render(msg, True, colour)
  dis.blit(mesg, [dis_x/6, dis_y/2])
 

def gameLoop():
  global game 
#game over is the ending quota but game close is UI
  game_over = False
  

  while not game_over:
#UI
    while game.is_game_over == True:
      dis.fill(aqua)
      message("Q: quit, C: continue", green)
      Your_score(game)

      pygame.display.update()
#UI/ ending inputs, not useful for AI
      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_q:
            game_over = True
            game = GameState()
          elif event.key == pygame.K_c:
            gameLoop()
        if event.type == pygame.QUIT:
          game_over = True
          game = GameState()

#Normal inputs, soon to be refactored      
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        game_over = True
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
          game.update(Directions.UP) 

        elif event.key == pygame.K_LEFT:
          game.update(Directions.LEFT)  

        elif event.key == pygame.K_DOWN:
          game.update(Directions.DOWN)   

        elif event.key == pygame.K_RIGHT:
          game.update(Directions.RIGHT)   

# game tick things, mostly UI 
    dis.fill(white)
    
    pygame.draw.rect(dis, green, [game.apple_loc.col * snake_block, game.apple_loc.row * snake_block, snake_block, snake_block])
# snake head is useful? otherwise UI
    # snake_head = []
    # snake_head.append(xpos)
    # snake_head.append(ypos)
    # snake_list.append(snake_head)
    # if len(snake_list) > length_of_snake:
    #     del snake_list[0]

    
 # is the head on another body part
    # for x in snake_list[:-1]:
    #     if x == snake_head:
    #       game_close = True

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
    
    clock.tick(snake_speed)

    
  pygame.quit()
  quit()
gameLoop()