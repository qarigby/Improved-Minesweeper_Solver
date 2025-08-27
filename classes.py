class Tile:
    def __init__(self, x, y, label, confidence=None):
        self.x = x
        self.y = y
        self.label = label # Raw label from classifier
        self.confidence = confidence # Matching score from template matching
        self.is_revealed = label not in ['H', 'E'] # 'H' = hidden, 'E' = empty
        self.is_flagged = label == 'F'
        # self.is_mine = label == 'M'
        self.number = int(label) if label.isdigit() else None

    def __repr__(self):
        return self.label
    
    @property
    def is_number(self):
        return self.number is not None and self.number > 0
    
    @property
    def is_unrevealed(self):
        return not self.is_revealed and not self.is_flagged



class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

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
        # If no hidden neighbours, return False early
        if not hidden_neighbours:
            return False

        # Assume if count of hidden neighbours == number on tile → all hidden neighbours are bombs
        return len(hidden_neighbours) == tile.number
    
    def hidden_neighbours_all_safe(self, x, y):
        tile = self.get_tile(x,y)
        if not tile or not tile.is_number:
            return False
        
        flagged_neighbours = [n for n in self.neighbours(x, y) if n.is_flagged]
        hidden = [n for n in self.neighbors(x, y) if n.is_unrevealed]
        
        # Assume if count of flagged neighbours == number on tile → all hidden neighbours are safe
        return len(flagged_neighbours) == tile.number and len(hidden) > 0
        