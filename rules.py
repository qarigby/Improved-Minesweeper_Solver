
"""
Checks if a tile is the same number as the number of adjacent hidden tiles - if so, then adjacent tiles are all bombs
"""
def r1(board_state):
    tiles_with_all_bomb_neighbours = []

    for y in range(board_state.rows):
        for x in range(board_state.cols):
            tile = board_state.get_tile(x, y)

            # Skip tiles that are not numbers
            if not tile.is_number:
                continue

            # Check if all unrevealed neighbours are bombs
            if board_state.hidden_neighbours_all_bombs(x, y):
                tiles_with_all_bomb_neighbours.append((x,y))
                for neighbour in board_state.neighbours(x, y):
                    if neighbour.is_unrevealed:
                        # board_state.right_click_tile(neighbour.x, neighbour.y)
                        print(f"Flagging tile at ({neighbour.x}, {neighbour.y})")
                        return tiles_with_all_bomb_neighbours

    return tiles_with_all_bomb_neighbours


"""
If the number of flags adjacent to a tile is the same as the tile number, then all adjacent tiles are safe
"""
def r2(board_state):
    tiles_with_all_safe_neighbours = []

    for y in range(board_state.rows):
        for x in range(board_state.cols):
            tile = board_state.get_tile(x, y)

            # Skip tiles that are not numbers
            if not tile.is_number:
                continue

            # Check if all unrevealed neighbours are safe
            if board_state.hidden_neighbours_all_safe(x, y):
                tiles_with_all_safe_neighbours.append((x, y))
                for neighbour in board_state.neighbours(x, y):
                    if neighbour.is_unrevealed:
                        print(f"Clearing tile at ({neighbour.x}, {neighbour.y})")
                        return tiles_with_all_safe_neighbours
                    
    return tiles_with_all_safe_neighbours
