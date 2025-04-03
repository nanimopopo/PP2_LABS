import pygame,sys
from pygame.locals import *
import random
pygame.init()

width, height = 500, 500
cell_size = 10
font_small = pygame.font.SysFont("Verdana", 20)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simple Snake')

black = (0, 0 , 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255,255,255)

snake_pos = [100, 100]
snake_body = [[100, 100], [80, 100], [60, 100]]
direction = 'RIGHT'
change_to = direction

food_pos = [random.randrange(1, width//10) * 10, random.randrange(1, height//10) * 10]
food_spawn = True

SCORE=0
SPEED=10
LEVEL=0
NEW_MILESTONE=5
time=pygame.time.get_ticks()

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
    direction = change_to

    if direction == 'UP':
        snake_pos[1] -= cell_size
    elif direction == 'DOWN':
        snake_pos[1] +=cell_size
    elif direction == 'LEFT':
        snake_pos[0] -= cell_size
    elif direction == 'RIGHT':
        snake_pos[0] += cell_size

    if snake_pos[0] < 0:
        pygame.quit()
    elif snake_pos[0] >= width:
        pygame.quit()
    elif snake_pos[1] < 0:
        pygame.quit()
    elif snake_pos[1] >= height:
        pygame.quit()
    
    snake_body.insert(0, list(snake_pos))
    snake_body.pop()

    screen.fill(black)
    scores=font_small.render(str(SCORE), True, white)
    levels=font_small.render(str(LEVEL), True, white)
    screen.blit(scores,(15,10))
    screen.blit(levels,(465,10))

    for block in snake_body:
        pygame.draw.rect(screen, green, pygame.Rect(block[0], block[1], cell_size, cell_size))
    
    for bloc in snake_body[1:]:
        if snake_pos==bloc:
            pygame.quit()
    
    if snake_pos==food_pos:
        food_spawn=False
        SCORE+=random.randint(1,5)
        snake_body.append(snake_body[-1])
    
    if food_spawn:
        pygame.draw.rect(screen, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
        
        if pygame.time.get_ticks() - time>3000:
            food_spawn=False
    else:
        while True:
            new_food_pos = [random.randrange(10, (width-40)//10) * 10, random.randrange(10, (height-40)//10) * 10]
            if new_food_pos not in snake_body:
                food_pos[:] = new_food_pos
                food_spawn = True
                time=pygame.time.get_ticks()
                break  

    
    if SCORE>=NEW_MILESTONE:
        SPEED+=1
        LEVEL+=1
        NEW_MILESTONE+=5

    pygame.display.flip()
    clock.tick(SPEED)

pygame.quit()
sys.exit()

