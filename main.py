import pygame, sys
import math, numpy
import pygame.docs

from scripts.object import ObjectRender
from scripts.jsonManager import jsonClass 

window_size = (1280, 720)
pygame.init()
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

ObjectMap = jsonClass().extractObjectsFromFile("map.json")
ReadyToRenderObject = []

for i in ObjectMap:
    Rendered = ObjectRender(
        size=90,
        points=i['Points'], 
        vertices=i['Vertices'], 
        position=i['Position'], 
        screen=screen
    )

    ReadyToRenderObject.append(Rendered)

while True:
    screen.fill( (0,0,0) )

    dt = clock.tick(clock.get_fps())/1000
    pygame.display.set_caption("FPS: " + str(clock.get_fps()))
    
    for i in ReadyToRenderObject:
        i.Run(dt)
        i.rotation_demonstration()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h))
            WINDOW_MAX = (event.w, event.h)
        elif event.type == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
            
    clock.tick_busy_loop(120)
    pygame.display.update()
