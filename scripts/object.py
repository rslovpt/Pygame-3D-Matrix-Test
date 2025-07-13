import math, pygame

def drawText(self, screen, pos):
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('here', True, (255,255,255))
    textRect = text.get_rect()
    textRect.center = (pos)
    screen.blit(text, textRect)

def distance(p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        return (dx**2 + dy**2) ** 0.5

class ObjectRender:
    
    def __init__(self, size : int, points : list, vertices : list, faces : list, ColorList : list, position : tuple, angles : list, screen):
        self.screen = screen
        self.delta_time = 0

        self.FOV = size
        self.FOV_limit = 2000

        self.points = points; self.vertices = vertices; self.faces = faces; self.ColorList = ColorList
        self.global_position = position

        self.object_angle = angles['Global']
        self.fixed_camera_angle = angles['Camera']

        self.line_width = 2

    def draw_vertice_connections(self, points, color=(255, 255, 255)):
        pygame.draw.line(self.screen, color, points[0], points[1], width=self.line_width)
    
    def draw_point(self, projected_points : list):
        for i in projected_points:
            pygame.draw.circle(self.screen, (255,255,255), i, self.line_width-1)
    
    def edge_interpolate(self, p1, p2):
        points_in_between = []

        if p2[1] < p1[1]:
            p1, p2 = p2, p1

        dy = p2[1] - p1[1]
        dx = p2[0] - p1[0]

        if dy == 0:
            return [] 

        slope = dx / dy

        for i in range(int(dy)):
            y = p1[1] + i
            x = p1[0] + slope * i
            points_in_between.append([int(x), int(y)])

        return points_in_between
    def fill_triangle(self, p0, p1, p2, color):
        pts = sorted([p0, p1, p2], key=lambda p: p[1])
        p0, p1, p2 = pts

        left = self.edge_interpolate(p0, p2)

        right_top = self.edge_interpolate(p0, p1)
        right_bot = self.edge_interpolate(p1, p2)

        for i in range(len(right_top)):
            if i < len(left):
                self.draw_vertice_connections([left[i], right_top[i]], color)

        for i in range(len(right_bot)):
            left_idx = i + len(right_top)
            if left_idx < len(left):
                self.draw_vertice_connections([left[left_idx], right_bot[i]],color)

    def fill_sides(self):
        rotated_points = [self.rotateX(self.rotateY(p)) for p in self.points]

        def face_depth(face):
            return min([rotated_points[i][2] for i in face])

        indexed_faces = list(enumerate(self.faces))
        sorted_faces = sorted(indexed_faces, key=lambda f: face_depth(f[1]), reverse=True)

        for face_index, face in sorted_faces:
            face_rotated = [rotated_points[i] for i in face]
            projected = [self.projection(p) for p in face_rotated]

            tri1 = [projected[0], projected[1], projected[2]]
            tri2 = [projected[0], projected[2], projected[3]]

            color = self.ColorList[face_index]

            self.fill_triangle(*tri1, color)
            self.fill_triangle(*tri2, color)

    def ofill_sides(self):
        for face in self.faces:
            points = [self.projection(self.rotateX(self.rotateY(self.points[i]))) for i in face]
            points_s = sorted(points, key=lambda p: p[1])

            p0, p1, p2, p3 = points

            if distance(p0, p2) < distance(p1, p3):
                tri1 = [p0, p1, p2]
                tri2 = [p0, p2, p3]
            else:
                tri1 = [p1, p2, p3]
                tri2 = [p1, p3, p0]
            
            self.fill_triangle(*tri1)
            self.fill_triangle(*tri2)

    def projection(self, point):
        z_axis = -(self.global_position[2]) + self.FOV
        return (
            self.global_position[0] + ((point[0] * self.FOV )/(point[2] + self.FOV)) * z_axis, 
            self.global_position[1] + ((point[1] * self.FOV)/(point[2] + self.FOV)) * z_axis
        )
    
    def rotateX(self, point):
        new_point = list(point)

        new_point[0] = point[0]
        new_point[1] = (math.cos(self.object_angle[1]) * point[1] - math.sin(self.object_angle[1]) * point[2]) 
        new_point[2] = (math.sin(self.object_angle[1]) * point[1] + math.cos(self.object_angle[1]) * point[2])

        return tuple(new_point)
    
    def rotateY(self, point):
        new_point = list(point)

        new_point[0] = (math.cos(self.object_angle[0]) * point[0] - math.sin(self.object_angle[0]) * point[2])
        new_point[1] = point[1]
        new_point[2] = (math.sin(self.object_angle[0]) * point[0] + math.cos(self.object_angle[0]) * point[2])

        return tuple(new_point)

    def rotation_demonstration(self):
        self.object_angle = (self.object_angle[0] + (1 * self.delta_time), self.object_angle[1])

    def Run(self, delta_time):
        self.delta_time = delta_time

        #for i in self.vertices:
            #pointStart = self.projection( self.rotateX(self.rotateY(self.points[i[0]])) )
            #pointEnd = self.projection( self.rotateX(self.rotateY(self.points[i[1]])) )

            #self.draw_point([pointStart, pointEnd])
            #self.draw_vertice_connections([pointStart, pointEnd])

        self.fill_sides()