import math
import tkinter as tk
import random
import string

SIDE_LENGTH = 50
CANVAS_COLOR = "#%02x%02x%02x" % (100, 200, 255)  # Light blue RGB value 
MAX_TILES = 5
DICE_PROBS = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5,
              7: 6, 8: 5, 9: 4, 10: 3, 
              11: 2, 12: 1} 

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

# CatanBoard class is created with CatanTile objects
class CatanBoard():
    def __init__(self, center_x, center_y, max_tiles):
        self.canvas = tk.Canvas(width=1000, height=800, bg = CANVAS_COLOR)
        self.tiles = CatanBoard.generate_tiles(center_x, center_y, max_tiles)
        self.tile_map = None
        # self.tile_map = CatanBoard.populate_adjacency_map(self.tiles)

    @staticmethod
    def get_tile_colors():
        # RGB tuple converted to hexadecimal string as key with number count as value
        tile_colors = {
            "#%02x%02x%02x" % (0, 100, 0): 4,       #dark green
            "#%02x%02x%02x" % (127, 255, 0): 4,     #light green
            "#%02x%02x%02x" % (255, 255, 0): 4,     #yellow
            "#%02x%02x%02x" % (255, 69, 0): 3,      #orange red
            "#%02x%02x%02x" % (128, 128, 128): 3,   #grey
            "#%02x%02x%02x" % (244, 164, 96): 1     #sand yellow
        }

        colors = []
        for color, count in tile_colors.items():
            colors.extend([color] * count)  # Add color 'count' times 

        random.shuffle(colors)  # Shuffle for random order
        return colors

    @staticmethod
    def generate_tiles(center_x, center_y, max_hex):
        if max_hex % 2 != 1:
            return "Error: Needs to be central hexagon"

         # Get the list of exact tile colors
        tile_colors = CatanBoard.get_tile_colors()
        tile_names = [char for char in string.ascii_uppercase]        
   
        tiles = []
        # Dictionary to store tile refs    
        tiles.append(CatanTile(tile_names.pop(0), SIDE_LENGTH, center_x, center_y, tile_colors.pop()))
   
        # Adjacent center distance (short side of hexagon)
        y_spacing = math.sqrt(3) * SIDE_LENGTH
   
        # Center column
        for y in range(max_hex // 2):
            tiles.append(CatanTile(tile_names.pop(0), SIDE_LENGTH, center_x, center_y + y_spacing * (y+1), tile_colors.pop()))
            tiles.append(CatanTile(tile_names.pop(0), SIDE_LENGTH, center_x, center_y - y_spacing * (y+1), tile_colors.pop()))
   
        for hex_num in range(max_hex - 1, max_hex//2, -1):
            x_shift = 1.5 * (max_hex - hex_num) * SIDE_LENGTH
            if hex_num % 2 == 0:
                for i in range(hex_num // 2):
                    tiles.append(CatanTile(tile_names.pop(0), SIDE_LENGTH, center_x + x_shift, center_y + y_spacing * (i + 0.5), tile_colors.pop()))
                    tiles.append(CatanTile(tile_names.pop(0), SIDE_LENGTH, center_x + x_shift, center_y - y_spacing * (i + 0.5), tile_colors.pop()))
                    tiles.append(CatanTile(tile_names.pop(0), SIDE_LENGTH, center_x - x_shift, center_y + y_spacing * (i + 0.5), tile_colors.pop()))
                    tiles.append(CatanTile(tile_names.pop(0), SIDE_LENGTH, center_x - x_shift, center_y - y_spacing * (i + 0.5), tile_colors.pop()))
            else:  # hex_num % 2 == 1
                tiles.append(CatanTile(tile_names.pop(0), SIDE_LENGTH, center_x + x_shift, center_y, tile_colors.pop()))
                tiles.append(CatanTile(tile_names.pop(0), SIDE_LENGTH, center_x - x_shift, center_y, tile_colors.pop()))
                for i in range(hex_num // 2):
                    tiles.append(CatanTile(tile_names.pop(0), SIDE_LENGTH, center_x + x_shift, center_y + y_spacing * (i + 1), tile_colors.pop()))
                    tiles.append(CatanTile(tile_names.pop(0), SIDE_LENGTH, center_x + x_shift, center_y - y_spacing * (i + 1), tile_colors.pop()))
                    tiles.append(CatanTile(tile_names.pop(0), SIDE_LENGTH, center_x - x_shift, center_y + y_spacing * (i + 1), tile_colors.pop()))
                    tiles.append(CatanTile(tile_names.pop(0), SIDE_LENGTH, center_x - x_shift, center_y - y_spacing * (i + 1), tile_colors.pop()))  
        
        return tiles
    
    def populate_adjacency_map(self):
        tile_map = {}
        
        for tile in self.tiles:
            tile_map[tile] = []
        
        tiles_used = []   
        for i, tile in enumerate(self.tiles):
            if tile not in tiles_used:   
                adjacent_candidates = self.tiles[i+1:] 
                for other in adjacent_candidates:
                    if tile.is_adjacent(other):
                        tile_map[tile].append(other)
                        tile_map[other].append(tile)
                tiles_used.append(tile)        
        self.tile_map = tile_map

    def populate_tile_numbers(self):
        # Create local number list with specific values and shuffle
        tile_numbers = {
            2: 1, 3: 2, 4: 2, 5: 2, 6: 2, 
            8: 2, 9: 2, 10: 2, 11: 2, 12: 1
        }
        
        numbers = []
        for num, count in tile_numbers.items():
            numbers.extend([num] * count)  

        random.shuffle(numbers)

        # Populate CatanTile with number in shuffled list
        for tile in self.tiles:
            if tile.fill_color != "#%02x%02x%02x" % (244, 164, 96):
                tile.number = numbers.pop()

    def draw_board(self):        
        for tile in self.tiles:
            tile.draw_tile(self.canvas)
            if tile.fill_color != "#%02x%02x%02x" % (244, 164, 96):
                self.canvas.create_text(tile.center[0], tile.center[1] - 10, 
                    font=('Times New Roman', 15, 'bold'), text=tile.number)
                self.canvas.create_text(tile.center[0], tile.center[1] + 10, 
                    font=('Times New Roman', 15, 'bold'), text=tile.name)
            else: # 'desert' tile
                self.canvas.create_text(tile.center[0], tile.center[1], 
                    font=('Times New Roman', 15, 'bold'), text=tile.name)
                
    def drawAdjacencyLines(self):
        tiles_used = []            
        for i, tile in enumerate(self.tile_map):
            if tile not in tiles_used: 
                for adjacent in self.tile_map[tile]:
                    self.canvas.create_line(tile.center[0], tile.center[1],
                                            adjacent.center[0], adjacent.center[1], 
                                            width = 2)
                tiles_used.append(tile)

    def refresh_board(self, event):
        self.canvas.destroy()
        self.__init__(500, 400, MAX_TILES)
        self.canvas.pack()
        self.populate_adjacency_map()
        self.populate_tile_numbers()
        self.draw_board()
      
    def get_intersection_sums(self):
        intersection_sums = {}
        
        # Access dictionary of CatanTile key and list of adjacent CatanTile values  
        for tiles1, adjacent_tiles in self.tile_map.items():
            # Access list of adjacent CatanTile objects
            for tiles2 in adjacent_tiles:
                for tiles3 in adjacent_tiles:
                    if tiles3 != tiles2:
                        if tiles3 in self.tile_map[tiles2]:
                            # there may be rounding differences            
                            vertex_pair1 = tiles3.get_matching_vertices(tiles1)
                            vertex_pair2 = tiles3.get_matching_vertices(tiles2) 
                            vertex_pair3 = tiles1.get_matching_vertices(tiles2)
        
                            for vertex in vertex_pair1:
                                if (vertex in vertex_pair2) and (vertex in vertex_pair3):             
                                    tile1_prob = math.ceil(DICE_PROBS[tiles1.number] * 36) if tiles1.number is not None else 0
                                    tile2_prob = math.ceil(DICE_PROBS[tiles2.number] * 36) if tiles2.number is not None else 0
                                    tile3_prob = math.ceil(DICE_PROBS[tiles3.number] * 36) if tiles3.number is not None else 0  
                                    
                                    intersection_sums[vertex] = tile1_prob + tile2_prob + tile3_prob
            
        return intersection_sums
    
if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("1000x1000")
    board = CatanBoard(500, 400, MAX_TILES)
    board.canvas.pack()
    board.populate_adjacency_map()
    board.populate_tile_numbers()
    board.draw_board()

    button = tk.Button(window, text="Refresh")
    button.bind("<Button-1>", board.refresh_board)
    button.pack(side="right", anchor="se")

    print("\nCatanTile Adjacency Dictionary")
    for tile, neighbors in board.tile_map.items():
        neighbor_list = []
        for neighbor in neighbors: 
            neighbor_list.append(str(neighbor))
        print(tile, ": ", neighbor_list, sep="")

    # for x, y in board.get_three_way_intersections(): 
    #     board.canvas.create_text(x, y, text="Test")
        
    # for vertex, sum in board.get_intersection_sums().items(): 
    #     board.canvas.create_text(vertex[0], vertex[1], text=sum, font=("Times New Roman", 15), fill='blue')

    print("\nMATCHING VERTICES TEST")
    for tile, neighbors in board.tile_map.items():
        for neighbor in neighbors: 
            print(tile.get_matching_vertices(neighbor))
    
    window.mainloop()
