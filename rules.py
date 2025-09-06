
"""
Checks if a tile is the same number as the number of adjacent hidden tiles - if so, then adjacent tiles are all bombs
"""
def r1(board_state):
    tiles_to_flag = []

    for y in range(board_state.rows):
        for x in range(board_state.cols):
            tile = board_state.get_tile(x, y)

            # Skip tiles that are not numbers
            if not tile.is_number:
                continue

            # Check if all unrevealed neighbours are bombs
            if board_state.hidden_neighbours_all_bombs(x, y):
                for neighbour in board_state.neighbours(x, y):
                    if neighbour.is_unrevealed:
                        tiles_to_flag.append((neighbour.x, neighbour.y))
                        print(f"Flagging tile at ({neighbour.x}, {neighbour.y})")
                return tiles_to_flag

    return tiles_to_flag

"""
If the number of flags adjacent to a tile is the same as the tile number, then all adjacent tiles are safe
"""
def r2(board_state):
    tiles_to_clear = []

    for y in range(board_state.rows):
        for x in range(board_state.cols):
            tile = board_state.get_tile(x, y)

            # Skip tiles that are not numbers
            if not tile.is_number:
                continue

            # Check if all unrevealed neighbours are safe
            if board_state.hidden_neighbours_all_safe(x, y):
                for neighbour in board_state.neighbours(x, y):
                    if neighbour.is_unrevealed:
                        tiles_to_clear.append((neighbour.x, neighbour.y))
                        print(f"Clearing tile at ({neighbour.x}, {neighbour.y})")
                return tiles_to_clear

    return tiles_to_clear
