# 🌄 Settlers of Catan Board Generator and Visualizer (Python + Tkinter)

This project generates and visualizes a randomized Settlers of Catan board using Python and the tkinter library. It follows OOP principles to add layers of abstraction and uses the tkinter GUI toolkit to create an interactive visualization for the user. At a glance, the code includes logic for hexagonal tile generation, the board layout, tile coloring, number placement, adjacency mapping, and shared vertex calculations.

### Features:
- Hexagonal Tile Generation: Individual tile objects hold information used for board generation. Adjacency and vertex-tile center logic used to compute coordinates of hexagonal tiles.
- Randomized Tile Colors: Tiles are randomly assigned colors (representing resource types from Settlers of Catan) from a predefined distribution of each resource type.
- Dice Number Assignment: Numbers (2–12, excluding 7) are randomly distributed among resource tiles. Every number except 2 and 12 (and 7) are shown twice. 
- Adjacency Mapping: Efficiently computes which tiles are adjacent to each other based on tile center-to-center distance.
- Vertex Sharing Logic: Identifies shared vertices between tiles using floating-point coordinate comparisons with a strict tolerance.
- Vertex Probability Sums: Calculates the summed dice roll probabilities for three-way tile intersections — useful for strategy analysis.
- GUI: Draws the full board using tkinter.

### Sample Generation: 
There is a refresh button, but video with demo is not included yet
![Alt text](CatanSnippet.PNG?raw=true "GeneratedBoard")

### Object-Oriented Design:
`CatanTile` Class encapsulates the logic for an individual hex tile:
- Calculates the six vertex positions of a regular hexagon relative to its center.
- Stores color, name, number, and vertex coordinate information.
- Includes other methods for drawing itself and detecting adjacency with other tiles.

`CatanBoard` Class encapsulates logic that manages the entire game board:
- Generates a fixed-size hexagonal grid layout centered on a given coordinate.
  - Initially planned to have "spiraling outward" sequential generation from a single central coordinate, but geometrical ratios to keep fixed regular hexagons became too complicated
  - Currently generates by column
- Populates tile colors and dice values.
- Computes adjacency maps and shared vertex intersections.
- Provides drawing and refresh functionality in the GUI.

### Shared Vertex Calculation:
- Math related issues were common in this project
- Due to floating-point rounding issues, shared vertices between adjacent tiles are identified by comparing coordinate pairs within a tolerance of 0.001.
- A match is declared if both the X and Y coordinate differences fall within this margin.
- This is not the most efficient way to determine shared vertices as it indicates an underlying imperfection in tile generation (shared vertices should be exact)

### `tkinter` GUI Implementation:

    Drawing the Catan board on a resizable canvas.

    Labeling tiles with numbers and names.

    Displaying the probability distribution (based on standard 36-die combinations) of dice values.

    A Refresh button to regenerate a randomized board.

### More on Tile Layout Logic:
Tile generation is completed by column starting with a central column of tiles and symmetrical surrounding columns. Tiles are positioned based on:
- Vertical spacing: Calculated using the height of a hexagon $\sqrt(3) \cdot side_length$ (sqrt(3) * side_length).
- Horizontal offsets: Based on the row's distance from the center and the column's width (1.5 * side_length).

The current configuration supports a maximum tile row length of 5, resulting in the standard 19-hex Catan layout.
🔢 Dice Roll Probabilities

Tile numbers are distributed with the following frequencies, matching standard Settlers of Catan rules:
Number	Probability (out of 36)
2 / 12	1
3 / 11	2
4 / 10	3
5 / 9	4
6 / 8	5
7	Not assigned to tiles

These weights are used when summing up three-tile intersection probabilities, helpful for identifying high-value settlement spots.
▶️ How to Run

Make sure Python is installed on your machine. Then run:

python catan_visualizer.py

A GUI window will open with a randomly generated Catan board. Click the "Refresh" button to regenerate the layout and reassign tile values.
🛠️ Possible Extensions

    Add port locations and the robber mechanic.

    Allow interactive placement of settlements/roads.

    Highlight high-probability intersections visually.

    Export the board as an image or PDF.


# CatanBoardGenerator
Board state generator for popular board game Settlers of Catan
Currently working on a way to identify nodes and calculate "high-value" nodes
- Able to identify three way intersections
- Need to implement a way to rank ports
- Need a way to evaluate path distance to other "high-value" nodes
