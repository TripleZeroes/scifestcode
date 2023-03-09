import pygame
import time
import random

pygame.init()

green = (0, 255, 100)
white = (255, 255, 255)
yellow = (255, 255, 102)
blue = (0, 0, 255)
red = (255,0,0)
aqua = (0, 255, 255)

new_y = 0
new_x = 0
ypos = 20
xpos = 20

dis_x = 500
dis_y = 500

game_over = False

snake_block = 10
snake_speed = 30

dis = pygame.display.set_mode((dis_x, dis_y))
dis.fill(green)

pygame.display.set_caption('I like snake')

clock = pygame.time.Clock()


font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
 
 
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])
 
 
def our_snake(snake_block, snake_list):
  for x in snake_list:
    pygame.draw.rect(dis, red, [x[0], x[1], snake_block, snake_block])

def message(msg, colour): 
  mesg = font_style.render(msg, True, colour)
  dis.blit(mesg, [dis_x/6, dis_y/2])
 
def gameLoop():
  game_over = False
  game_close = False
  
  xpos = dis_x/2
  ypos = dis_y/2

  new_x = 0
  new_y = 0

  snake_list=[]
  length_of_snake = 1
  
  foodx = round(random.randrange(0, dis_x - snake_block) / 10.0) * 10.0
  foody = round(random.randrange(0, dis_y - snake_block) / 10.0) * 10.
  
  while not game_over:

    while game_close == True:
      dis.fill(aqua)
      message("Q: quit, C: continue")
      Your_score(length_of_snake - 1)

      pygame.display.update()

      for event in pygame.event.get():
        if pygame.event.type == pygame.KEYDOWN:
          if event.type == pygame.K_q:
            game_over = True
            game_close = False
          elif event.type == pygame.K_c:
            gameLoop()

          
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        game_over = True
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
          if new_y == snake_block and length_of_snake > 1:
            break
          else:
            new_x = 0
            new_y = -snake_block
        elif event.key == pygame.K_LEFT:
          if new_x == snake_block and length_of_snake > 1:
            break
          else:
            new_x = -snake_block
            new_y = 0
        elif event.key == pygame.K_DOWN:
          if new_y == -snake_block and length_of_snake > 1:
            break
          else:
            new_x = 0
            new_y = snake_block
        elif event.key == pygame.K_RIGHT:
          if new_x == -snake_block and length_of_snake > 1:
            break
          else:
            new_x = snake_block
            new_y = 0
  
   
    if xpos >= dis_x or xpos < 0 or ypos >= dis_y or ypos < 0:
        game_close = True
   
    ypos += new_y
    xpos += new_x
    dis.fill(white)
    
    pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
    snake_head = []
    snake_head.append(xpos)
    snake_head.append(ypos)
    snake_list.append(snake_head)
    if len(snake_list) > length_of_snake:
        del snake_list[0]

    
 
    for x in snake_list[:-1]:
        if x == snake_head:
          game_close = True
 
    our_snake(snake_block, snake_list)
    Your_score(length_of_snake - 1)
    
    pygame.draw.rect(dis, blue, [xpos, ypos, snake_block, snake_block])
    pygame.display.update()


    if xpos == foodx and ypos == foody:
        foodx = round(random.randrange(0, dis_x - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_y - snake_block) / 10.0) * 10.0
        length_of_snake += 1
    
    clock.tick(snake_speed)
    
  pygame.quit()
  quit()
gameLoop()