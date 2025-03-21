import pygame
import datetime


pygame.init()


WIDTH, HEIGHT = 400, 400
CENTER = (WIDTH // 2, HEIGHT // 2)

clock_image = pygame.image.load("clock.png")
minute_hand = pygame.image.load("right.png")
second_hand = pygame.image.load("left.png")

clock_image = pygame.transform.scale(clock_image, (WIDTH, HEIGHT))
minute_hand = pygame.transform.scale(minute_hand, (80, 110))  # Adjust size as needed
second_hand = pygame.transform.scale(second_hand, (50, 140))  # Adjust size as needed

minute_rect = minute_hand.get_rect(center=(100,100))
second_rect = second_hand.get_rect(center=(100,100))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")
clock = pygame.time.Clock()

running = True
while running:
    screen.fill((255, 255, 255))  
    
    now = datetime.datetime.now()
    minute_angle = -(now.minute + now.second / 60) * 6  
    second_angle = -now.second * 6
    
    
    rotated_minute = pygame.transform.rotate(minute_hand, minute_angle)
    rotated_second = pygame.transform.rotate(second_hand, second_angle)
    
    
    min_rect = rotated_minute.get_rect(center=(220,150))
    sec_rect = rotated_second.get_rect(center=(230,200))
    
    
    screen.blit(clock_image, (0, 0))
    
    
    screen.blit(rotated_minute, min_rect.topleft)
    screen.blit(rotated_second, sec_rect.topleft)
    
    
    pygame.display.flip()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    clock.tick(60)  

pygame.quit()
