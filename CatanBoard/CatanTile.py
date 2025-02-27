import math

# 1. Editing get_matching_vertices() to work with slight float imprecision 
# 2. Editing is_adjacent() to determine adjacency with two matching vertices and center distance
# 3. Added number instance variable to constructor
class CatanTile:
    def __init__(self, name, side_length, x_center, y_center, fill_color):
        self.side_length = side_length
        self.center = (x_center, y_center)
        self.fill_color = fill_color
        self.name = name
        self.number = None

        # Calculate offset to center hexagon around x,y coords
        x_offset = 0.5 * side_length
        y_offset = (math.sqrt(3) / 2) * side_length

        # Vertex dictionary, adjusted with offsets
        self.vertices = {
            'A': (x_center - x_offset, y_center - y_offset),
            'B': (x_center + x_offset, y_center - y_offset),
            'C': (x_center + 2 * x_offset, y_center),
            'D': (x_center + x_offset, y_center + y_offset),
            'E': (x_center - x_offset, y_center + y_offset),
            'F': (x_center - 2 * x_offset, y_center)
        }

    def __str__(self): 
        return f"CatanTile {self.name}"
    
    def draw_tile(self, canvas):
        coords = []
        for vertex in self.vertices.values():
            coords.extend(vertex)
        canvas.create_polygon(coords, outline="black", fill=self.fill_color)

    def label_vertices(self, canvas):
        for key, value in self.vertices.items():
            x, y = value
            canvas.create_text(x, y, text=f"{key}: {round(value, 2)}")
    
    def is_adjacent(self, other_tile):
        expected_distance = math.sqrt(3) * self.side_length
        # Calculate actual distance between centers
        distance_x = abs(self.center[0] - other_tile.center[0])
        distance_y = abs(self.center[1] - other_tile.center[1])
        actual_distance = math.sqrt(distance_x**2 + distance_y**2)

        if abs(actual_distance - expected_distance) > 0.0001:
            return False
        
        matching_vertices = self.get_matching_vertices(other_tile)
        return len(matching_vertices) == 2
    
    def get_matching_vertices(self, other_tile):
        matching = [] 
        TOLERANCE = 0.001
        for v1 in self.vertices.values():
            for v2 in other_tile.vertices.values():
                if (abs(v1[0] - v2[0]) < TOLERANCE and 
                    abs(v1[1] - v2[1]) < TOLERANCE):
                    matching.append(v1)
        return matching
