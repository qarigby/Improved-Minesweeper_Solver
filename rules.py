from prob_helpers import get_frontier_tiles, get_constraints, generate_valid_configs, estimate_tile_probabilities, split_frontier_into_groups

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



'''
Determines (using probability) the best tile to clear when no deterministic moves can be made  
'''
# def r3(board_state):
#     frontiers = get_frontier_tiles(board_state)
#     constraints = get_constraints(board_state)
#     best_tiles = []

#     if not frontiers:
#         for y in range(board_state.rows):
#             for x in range(board_state.cols):
#                 tile = board_state.get_tile(x, y)
#                 if tile.is_unrevealed and not tile.is_flagged:
#                     return [(x, y)]  # Probability is unknown, so return 1.0
                

#     # Split the frontier into independent groups
#     groups = split_frontier_into_groups(constraints)
#     min_prob = 1.0
#     best_tile = None
                
#     # # Generate all valid mine configurations for the frontier
#     # valid_configs, frontier_list = generate_valid_configs(constraints, frontiers)

#     # # Estimate probabilities for each frontier tile
#     # tile_probs = estimate_tile_probabilities(valid_configs, frontier_list)

#     # # Find the tile(s) with the lowest probability of being a mine
#     # min_prob = min(tile_probs.values())
#     # for tile, prob in tile_probs.items():
#     #     if prob == min_prob:
#     #         best_tiles.append((x,y))
#     # # best_tiles = [tile for tile, prob in tile_probs.items() if prob == min_prob]

#     # # If multiple, pick one (e.g., first)
#     # # best_tile = best_tiles[0]

#     # return best_tiles

# def r3(board_state):
#     """
#     Determines (using probability) the best tile to clear when no deterministic moves can be made.
#     This version only considers the first group of frontier tiles to improve performance.
#     """
#     frontiers = get_frontier_tiles(board_state)
#     constraints = get_constraints(board_state)

#     if not frontiers:
#         # No frontier tiles, use global probability for all hidden, unflagged tiles
#         for y in range(board_state.rows):
#             for x in range(board_state.cols):
#                 tile = board_state.get_tile(x, y)
#                 if tile.is_unrevealed and not tile.is_flagged:
#                     return [(x, y)]

#     # Split the frontier into independent groups and only use the first group
#     groups = split_frontier_into_groups(constraints)
#     if not groups:
#         # Fallback to global probability if no groups found
#         for y in range(board_state.rows):
#             for x in range(board_state.cols):
#                 tile = board_state.get_tile(x, y)
#                 if tile.is_unrevealed and not tile.is_flagged:
#                     return [(x, y)]
#         return []

#     # Only process the first group
#     first_group = groups[0]
#     group_constraints = []
#     for tiles, mine_count in constraints:
#         if any(t in first_group for t in tiles):
#             group_constraints.append((tiles, mine_count))
#     valid_configs, frontier_list = generate_valid_configs(group_constraints, first_group)
#     if not valid_configs:
#         # Fallback to global probability if no valid configs
#         for y in range(board_state.rows):
#             for x in range(board_state.cols):
#                 tile = board_state.get_tile(x, y)
#                 if tile.is_unrevealed and not tile.is_flagged:
#                     return [(x, y)]
#         return []

#     tile_probs = estimate_tile_probabilities(valid_configs, frontier_list)
#     min_prob = min(tile_probs.values())
#     for tile, prob in tile_probs.items():
#         if prob == min_prob:
#             return [tile]

#     return []