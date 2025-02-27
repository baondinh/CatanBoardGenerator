# Tile and vertex logic using turtle

import math 
import turtle
 
SIDE_LENGTH = 50

class Hexagon:
    def __init__(self, side_length, x_coord, y_coord):
        self.side_length = side_length
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.vertex_dict = {}
       
        # Vertex dictionary
        self.vertex_dict['A'] = (x_coord, y_coord)                                                      #Bottom left
        self.vertex_dict['B'] = (x_coord + side_length, y_coord)                                        #Bottom right
        self.vertex_dict['C'] = (x_coord + 1.5 * side_length, y_coord + side_length * math.sqrt(3)/2)   #Right
        self.vertex_dict['D'] = (x_coord + side_length, y_coord + side_length * math.sqrt(3))           #Top right
        self.vertex_dict['E'] = (x_coord, y_coord + side_length * math.sqrt(3))                         #Top Left
        self.vertex_dict['F'] = (x_coord - 0.5 * side_length, y_coord + side_length * math.sqrt(3)/2)   #Left

    def get_vertices(self):
        return self.vertex_dict
    
    def label_vertices(self): 
        vertices = self.get_vertices()
        print(vertices)
        turtle.penup()
                
        for key, value in vertices.items():
            turtle.write(f"{key}: {value}")    
            turtle.forward(self.side_length)
            turtle.left(60)

    def draw_hexagon(self):
        turtle.penup()
        turtle.setpos(self.x_coord, self.y_coord)
        turtle.pendown()

        for i in range(6):
            turtle.forward(self.side_length)
            turtle.left(60)

# testing testing
