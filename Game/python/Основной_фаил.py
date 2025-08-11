import pygame
import keyboard as k


pygame.init()
screen = pygame.display.set_mode((720,720))
pygame.display.set_caption('Мёртвая точка')

x_save = 0
y_save = 0
def pl(x=0, y=0, x_save=300, y_save=300, rgb=(0,0,0), w=20, h=50):
    Hit_box = pygame.Rect(x, y, 0 + w, 0 + h)
    pygame.draw.rect(screen, (0, 0, 0), Hit_box)
    return x, y


def Upravlenie(x_save, y_save, speed=5):
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

    pl(x_save, y_save)
    return (x_save, y_save)





Run = True
while Run:
    screen.fill((63, 155, 11))   # Цвет заднего фона 
    x_save, y_save = Upravlenie(x_save,y_save)

    
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            Run = False
            pygame.quit() 
            
    pygame.time.Clock().tick(60) # Контралирует количество обрабатываемых операций в сикунду
    pygame.display.update()      # Обновляет экран











