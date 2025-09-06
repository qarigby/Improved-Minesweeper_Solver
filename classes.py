import global_variables
import pyautogui

# Helper Functions
def convert_coords(x,y):
    screen_x = global_variables.TOP_LEFT_X + x * global_variables.TILE_SIZE + global_variables.TILE_SIZE // 2
    screen_y = global_variables.TOP_LEFT_Y + y * global_variables.TILE_SIZE + global_variables.TILE_SIZE // 2
    return screen_x, screen_y


class Tile:
    def __init__(self, x, y, label, confidence=None):
        self.x = x
        self.y = y
        self.label = label # Raw label from classifier
        self.confidence = confidence # Matching score from template matching
        self.is_revealed = label == 'H'
        self.is_flagged = label == 'F'
        self.number = int(label) if label.isdigit() else None

    def __repr__(self):
        return self.label
    
    @property
    def is_number(self):
        return self.number is not None and self.number > 0
    
    @property
    def is_unrevealed(self):
        # if self.label in ['H']:
        #     return True
        # return False
        return not self.is_revealed # Need to check if this works before deleting the above code



class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.total_mines = global_variables.NUM_MINES
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

    def has_hidden_tiles(self):
        return any(tile.label == "H" for row in self.grid for tile in row)
    
    def has_mines(self):
        return any(tile.label == "M" for row in self.grid for tile in row) 

    def set_tile(self, x, y, tile):
        self.grid[y][x] = tile

    def get_tile(self, x, y):
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return self.grid[y][x]
        return None

    def neighbours(self, x, y):
        offsets = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1),           (0, 1),
                   (1, -1),  (1, 0),  (1, 1)]
        return [self.get_tile(x + dx, y + dy)
                for dx, dy in offsets
                if self.get_tile(x + dx, y + dy) is not None]

    def display(self):
        for row in self.grid:
            print(" ".join(tile.label for tile in row))

    def hidden_neighbours_all_bombs(self, x, y):
        tile = self.get_tile(x, y)
        if not tile or not tile.is_number:
            return False

        hidden_neighbours = [n for n in self.neighbours(x, y) if n.is_unrevealed]
        flagged_neighbours = [n for n in self.neighbours(x, y) if n.is_flagged]

        # If no hidden neighbours, return False early
        if not hidden_neighbours:
            return False
        
        # Assume if count of hidden neighbours == number on tile → all hidden neighbours are bombs
        return len(flagged_neighbours) + len(hidden_neighbours) == tile.number
    
    def hidden_neighbours_all_safe(self, x, y):
        tile = self.get_tile(x,y)
        if not tile or not tile.is_number:
            return False
        
        flagged_neighbours = [n for n in self.neighbours(x, y) if n.is_flagged]
        hidden_neighbours = [n for n in self.neighbours(x, y) if n.is_unrevealed]
        
        # Assume if count of flagged neighbours == number on tile → all hidden neighbours are safe
        return len(flagged_neighbours) == tile.number and len(hidden_neighbours) > 0
    
    def flag_tiles(self, tiles_to_flag):
        for x,y in tiles_to_flag:
            screen_x, screen_y = convert_coords(x, y)
            pyautogui.moveTo(screen_x, screen_y)
            pyautogui.rightClick()


    def clear_tiles(self, tiles_to_clear):
        for x,y in tiles_to_clear:
            screen_x, screen_y = convert_coords(x, y)
            pyautogui.moveTo(screen_x, screen_y)
            pyautogui.click()

    def reset(self):
        # Change for different levels
        # pyautogui.moveTo(global_variables.RESTART_X_BEGINNER, global_variables.RESTART_Y_BEGINNER)
        # pyautogui.moveTo(global_variables.RESTART_X_INTERMEDIATE, global_variables.RESTART_Y_INTERMEDIATE)

        pyautogui.moveTo(global_variables.RESTART_X_EXPERT, global_variables.RESTART_Y_EXPERT)
        pyautogui.click()

    def get_remaining_mines(self):
        flag_count = sum(1 for row in self.grid for tile in row if tile.label == 'F')
        return self.total_mines - flag_count
    
    def num_hidden_tiles(self):
        hidden_count = sum(1 for row in self.grid for tile in row if tile.label == 'H')
        return hidden_count