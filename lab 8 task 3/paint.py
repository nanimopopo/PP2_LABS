import pygame
from pygame.locals import *
import sys

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simple Paint')

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)

RECT = pygame.Rect(200, 200, 80, 120)
SQUARE = pygame.Rect(300,200,80,80)

class Button:
    def __init__(self, x, y, width, height, text, color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 30)
        text_surface = font.render(self.text, True, white)
        screen.blit(text_surface, (self.rect.x + 12, self.rect.y + 12))
    
    def check_action(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

drawing = False
brush_color = black

def set_black():
    global brush_color
    brush_color = black

def set_green():
    global brush_color
    brush_color = green

def set_red():
    global brush_color
    brush_color = red

def set_blue():
    global brush_color
    brush_color = blue

def clear_screen():
    screen.fill(white)

def exit_app():
    pygame.quit()
    sys.exit()

def draw_rectangle():
    pygame.draw.rect(screen, brush_color, RECT)
def draw_square():
    pygame.draw.rect(screen, brush_color, SQUARE)
def draw_circle():
    pygame.draw.circle(screen, brush_color, (180,180), 60)
def draw_righttriangle():
    pygame.draw.polygon(screen, brush_color, ((25,125),(25,250),(250,250)))
def eraser():
    global brush_color
    brush_color=white
    pygame.draw.circle(screen, brush_color, (mouse_x, mouse_y), 100)
def draw_equaltriangle():
    pygame.draw.polygon(screen, brush_color, ((300,200),(150,350),(450,350)))
def draw_rhomboid():
    pygame.draw.polygon(screen, brush_color, [(400,200),(475,300),(400,400),(325,300)])

buttons = [
    Button(10, 10, 60, 30, 'Black', black, set_black),
    Button(80, 10, 60, 30, 'Green', green, set_green),
    Button(150, 10, 60, 30, 'Red', red, set_red),
    Button(220, 10, 60, 30, 'Blue', blue, set_blue),
    Button(290, 10, 60, 30, 'Clear', gray, clear_screen),
    Button(360, 10, 60, 30, 'Exit', gray, exit_app),
    Button(420,10,60,30,'Rectangle',gray,draw_rectangle),
    Button(490,10,60,30,'Square',gray,draw_square),
    Button(560,10,60,30,'Circle',gray,draw_circle),
    Button(630,10,60,30,'Right Triangle',gray,draw_righttriangle),
    Button(10,50,60,30,'Eraser',gray,eraser),
    Button(100,50,60,30,'Equal Triangle',gray,draw_equaltriangle),
    Button(220,50,60,30,'Rhomboid',gray,draw_rhomboid)
]

clear_screen()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True

        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False

        for button in buttons:
            button.check_action(event)

    if drawing:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y > 50:
            pygame.draw.circle(screen, brush_color, (mouse_x, mouse_y), 5)

 
    pygame.draw.rect(screen, gray, (0, 0, width, 100))  
    for button in buttons:
        button.draw(screen)


    pygame.display.flip()



    






