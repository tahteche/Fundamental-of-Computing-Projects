"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    def spaced_values(line):
        """Checks if there are any zeroes between non-zero numbers"""

        state = 0
        for num in line:
            if state == 2:
                break
            if num > 0 and state == 1:
                state = 2
            if num == 0:
                state = 1
        if state == 0 or state == 1:
            return False
        else:
            return True
    
    def shift_left(line):
        """Shift non-zero values to the left of list"""
        shifted_line = []

        for dummy_num in line:
            shifted_line.append(0)

        index = 0
        for num in line:
            if num > 0:
                shifted_line[index] = num
                index += 1

        return shifted_line


    merged_line = shift_left(line)
    
    for index in range(1, len(merged_line)):
        if merged_line[index] == merged_line[index-1]:
            merged_line[index-1] *= 2
            merged_line[index] = 0
    
    if spaced_values(merged_line):
        merged_line = shift_left(merged_line)
            
    return merged_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        self._initial_tiles = {
            UP : [(0, column) for column in range(self._width)],
            DOWN: [(self._height - 1, column) for column in range(self._width)],
            LEFT : [(row, 0) for row in range(self._height)],
            RIGHT : [(row, self._width - 1) for row in range(self._height)]
        }
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[ 0 for dummy_columns in range(self._width)]
                        for dummy_rows in range(self._height)]        
        for dummy_i in range(2):
            self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        string = ""
        
        for row in self._grid:
            string += str(row) + "\n"
        return string

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        grid_change = False
        for tile in self._initial_tiles[direction]:
            temp_array = []
            row = tile[0]
            column = tile[1]
            
            #Use height for merging if direction is up or down (1 and 2)
            #and width if direction is left or right (3 or 4)
            if direction <= 2:
                number_of_merges = self._height
            else:
                number_of_merges = self._width
                
            for dummy_row in range(number_of_merges):
                temp_array.append(self.get_tile(row, column))
                row += OFFSETS[direction][0]
                column += OFFSETS[direction][1]
            temp_array = merge(temp_array)

            row = tile[0]
            column = tile[1]
            for item in temp_array:
                if item != self.get_tile(row, column):
                    grid_change = True                    
                    self.set_tile(row, column, item)
                row += OFFSETS[direction][0]
                column += OFFSETS[direction][1]
        if grid_change:
            self.new_tile()
        grid_change = False
                
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        cell_value = 1
        while cell_value != 0:
                row = random.randint(0, self._height -1 )
                column = random.randint(0, self._width -1)
                cell_value = self._grid[row][column]
        
        random_value = random.randint(1, 10)
        if random_value <= 9:
            self._grid[row][column] = 2
        else:
            self._grid[row][column] = 4
            
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
