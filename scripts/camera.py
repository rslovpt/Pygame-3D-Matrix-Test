import pygame

def rotateListX(objects : list, angle : int, dt) -> list:
    rotatedList = []
    for obj in objects:
        obj.object_angle = (
            obj.object_angle[0] + (angle * dt),
            obj.object_angle[1]
        )
        
        rotatedList.append(obj)
    return rotatedList

def rotateListY(objects : list, angle : int, dt) -> list:
    rotatedList = []
    for obj in objects:
        obj.object_angle = (
            obj.object_angle[0],
            obj.object_angle[1] + (angle * dt)
        )
        
        rotatedList.append(obj)
    return rotatedList

class CameraClass:
    def __init__(self, screen):
        self.movement_sensitivity = {
            'rotation': (2,1),
            'position': (5,5)
        }

        self.angle = 0
        self.screen = screen        
    def moveCamera(self, objectMap : list, instant=None, dt=0): #instant = teleport camera
        keysPressed = pygame.key.get_pressed()
        if keysPressed[pygame.K_d]: #Right Movement 
            objectMap = rotateListX(objectMap, angle=self.movement_sensitivity['rotation'][0], dt=dt)
        elif keysPressed[pygame.K_a]: #Left Movement
            objectMap = rotateListX(objectMap, angle=-self.movement_sensitivity['rotation'][0], dt=dt)
        
        if keysPressed[pygame.K_w]: #Right Movement 
            objectMap = rotateListY(objectMap, angle=self.movement_sensitivity['rotation'][1], dt=dt)
        elif keysPressed[pygame.K_s]: #Left Movement
            objectMap = rotateListY(objectMap, angle=-self.movement_sensitivity['rotation'][1], dt=dt)
        

        return objectMap