import pygame
import keyboard as k


pygame.init()
screen = pygame.display.set_mode((720,720))
pygame.display.set_caption('Мёртвая точка')

x_save = 0
y_save = 0

def player(x_save, y_save, w=20, h=50, speed=5):
    if k.is_pressed('w'):
        x_save += 0
        y_save += -speed
    elif k.is_pressed('s'):
        x_save += 0
        y_save += speed
    if k.is_pressed('a'):
        x_save += -speed
        y_save += 0
    elif k.is_pressed('d'):
        x_save += speed
        y_save += 0

    Hit_box = pygame.Rect(x_save, y_save, w, h)
    pygame.draw.rect(screen, (0, 0, 0), Hit_box)
    return (x_save, y_save)


def stena(x=0, y=0, w=100, h=75):
    stena = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, (115,66,34), stena)
    

def Dom(x=0,y=0,w_dom=1.25,h_dom=1.25):
    w = w_dom * 100
    h = h_dom * 75
    obsh_mnog = 100
    stena(x - w, y - h, w * 2.75, h)      # Левый верхний угол    # Верхняя стена
    stena(x - w, y + h, w * 2.75, h)      # Левый нижний угол     # Нижняя стена
    stena(x + w, y - h, h, h * 2.75) # Правый верхний угол   # Правая стена



Run = True
while Run:
    screen.fill((63, 155, 11))   # Цвет заднего фона 
    x_save, y_save = player(x_save, y_save)
    Dom(360,360)
    
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            Run = False
            pygame.quit() 
            
    pygame.time.Clock().tick(60) # Контралирует количество обрабатываемых операций в сикунду
    pygame.display.update()      # Обновляет экран











