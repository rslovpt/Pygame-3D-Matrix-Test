import math, pygame
class ObjectRender:
    
    def __init__(self, size : int, points : list, vertices : list, position : tuple, screen):
        self.screen = screen
        self.delta_time = 0

        self.FOV = size
        self.FOV_limit = 2000

        self.points = points; self.vertices = vertices
        self.global_position = position

        self.object_angle = 0
        self.line_width = 3

    def draw_vertice_connections(self, points):
        pygame.draw.line(self.screen, (255,255,255), points[0], points[1], width=self.line_width)
    
    def draw_point(self, projected_points : list):
        for i in projected_points:
            pygame.draw.circle(self.screen, (255,255,255), i, self.line_width-1)
    
    def projection(self, point):
        z_axis = -(self.global_position[2]) + self.FOV
        return (
            self.global_position[0] + ((point[0] * self.FOV )/(point[2] + self.FOV)) * z_axis, 
            self.global_position[1] + ((point[1] * self.FOV)/(point[2] + self.FOV)) * z_axis
        )
    
    def rotateX(self, point):
        new_point = list(point)

        new_point[0] = point[0]
        new_point[1] = (math.cos(self.object_angle) * point[1] - math.sin(self.object_angle) * point[2]) 
        new_point[2] = (math.sin(self.object_angle) * point[1] + math.cos(self.object_angle) * point[2])

        return tuple(new_point)
    
    def rotateY(self, point):
        new_point = list(point)

        new_point[0] = (math.cos(self.object_angle) * point[0] - math.sin(self.object_angle) * point[2])
        new_point[1] = point[1]
        new_point[2] = (math.sin(self.object_angle) * point[0] + math.cos(self.object_angle) * point[2])

        return tuple(new_point)

    def rotation_demonstration(self):
        self.object_angle += 1 * self.delta_time

    def Run(self, delta_time):
        self.delta_time = delta_time

        for i in self.vertices:
            pointStart = self.projection( self.rotateX(self.rotateY(self.points[i[0]])) )
            pointEnd = self.projection( self.rotateX(self.rotateY(self.points[i[1]])) )

            self.draw_point([pointStart, pointEnd])
            self.draw_vertice_connections([pointStart, pointEnd])
        