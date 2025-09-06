''' Helper Functions '''

# Function: Gets frontier tiles (hidden tiles that are adjacent to revealed tiles)
def get_frontier_tiles(board):
    frontier_tiles = set()

    for y in range(board.rows):
        for x in range(board.cols):
            tile = board.get_tile(x,y)
            
            if tile.is_number:
                if not tile.is_unrevealed: # If the tile is revealed
                    for neighbour in board.neighbours(x,y):
                        if neighbour.is_unrevealed: # If the neighbour is hidden
                            frontier_tiles.add((neighbour.x, neighbour.y))

# Function: Gather tile constraints - Need to actually define what this means !!!! - Like what actually is this !
def get_constraints(board):
    constraints = []

    for y in range(board.rows):
        for x in range(board.cols):
            tile = board.get_tile(x,y)

            if tile.is_number:
                if not tile.is_unrevealed:
                    hidden_neighbours = []
                    flagged_neighbours = 0

                    for neighbour in board.neighbours(x,y):
                        if neighbour.is_unrevealed:
                            hidden_neighbours.append((neighbour.x, neighbour.y))
                        
                        elif neighbour.is_flagged:
                            flagged_neighbours += 1
                    
                    total_mines = board[x,y] - flagged_neighbours
                    if hidden_neighbours:
                        constraints.append((hidden_neighbours, total_mines))
    return constraints

# Function: 
def generate_valid_configs(constraints, frontiers):
    frontier_list = list(frontiers)
    tile_indices = {tile: i for i, tile in enumerate(frontier_list)}
    num_tiles = len(frontier_list)
    valid_configs = []

    for bits in range(1 << num_tiles):
        config = [0] * num_tiles
        for i in range(num_tiles):
            if bits & (1 << i):
                config[i] = 1

        valid = True
        for tiles, mine_count in constraints:
            count = 0
            for t in tiles:
                if t in tile_indices:
                    count += config[tile_indices[t]]
            if count != mine_count:
                valid = False
                break

        if valid:
            valid_configs.append(config)

    return valid_configs, frontier_list


# Function:  
def estimate_tile_probabilities(valid_configs, frontier):
    num_configs = len(valid_configs)
    mine_counts = [0] * len(frontier)

    for config in valid_configs:
        for i, val in enumerate(config):
            if val == 1:
                mine_counts[i] += 1

    probabilities = {}
    for i, tile in enumerate(frontier):
        probabilities[tile] = mine_counts[i] / num_configs if num_configs > 0 else 0.0

    return probabilities

# Function:
def estimate_global_probability(board, total_mines, flags_placed):
    hidden = 0
    for y in range(board.rows):
        for x in range(board.cols):
            tile = board.get_tile(x, y)
            if tile.is_unrevealed and not tile.is_flagged:
                hidden += 1
    remaining_mines = total_mines - flags_placed
    return remaining_mines / hidden if hidden else 1


''' Now we just need an actual rule function to tie all these together !!'''