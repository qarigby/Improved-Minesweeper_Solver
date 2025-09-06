# # ''' Helper Functions '''

# # Function: Gets frontier tiles (hidden tiles that are adjacent to revealed tiles)
# def get_frontier_tiles(board):
#     frontier_tiles = set()

#     for y in range(board.rows):
#         for x in range(board.cols):
#             tile = board.get_tile(x,y)
            
#             if tile.is_number:
#                     for neighbour in board.neighbours(x,y):
#                         if neighbour.is_unrevealed: # If the neighbour is hidden
#                             frontier_tiles.add((neighbour.x, neighbour.y))
#     return frontier_tiles

# # Function: Gather tile constraints (rules specifying how many mines must be present among a certain group of tiles)
# def get_constraints(board):
#     constraints = []

#     for y in range(board.rows):
#         for x in range(board.cols):
#             tile = board.get_tile(x,y)

#             if tile.is_number:
#                     hidden_neighbours = []
#                     flagged_neighbours = 0

#                     for neighbour in board.neighbours(x,y):
#                         if neighbour.is_unrevealed:
#                             hidden_neighbours.append((neighbour.x, neighbour.y))
                        
#                         elif neighbour.is_flagged:
#                             flagged_neighbours += 1
                    
#                     total_mines = tile.number - flagged_neighbours
#                     if hidden_neighbours:
#                         constraints.append((hidden_neighbours, total_mines))
#     return constraints

# # Function: Generate all possible mine configurations for the given frontier tiles that satisfy the provied constraints - returns valid configs and the ordered frontier tile list
# def generate_valid_configs(constraints, frontiers):
#     frontier_list = list(frontiers)
#     tile_indices = {tile: i for i, tile in enumerate(frontier_list)}
#     num_tiles = len(frontier_list)
#     valid_configs = []

#     for bits in range(1 << num_tiles):
#         config = [0] * num_tiles
#         for i in range(num_tiles):
#             if bits & (1 << i):
#                 config[i] = 1

#         valid = True
#         for tiles, mine_count in constraints:
#             count = 0
#             for t in tiles:
#                 if t in tile_indices:
#                     count += config[tile_indices[t]]
#             if count != mine_count:
#                 valid = False
#                 break

#         if valid:
#             valid_configs.append(config)

#     return valid_configs, frontier_list


# # Function: Estimates the probability of each tile in the frontier list containing a mine, based on how often each tile is a mine across all valid mine configurations 
# def estimate_tile_probabilities(valid_configs, frontier_list):
#     num_configs = len(valid_configs)
#     mine_counts = [0] * len(frontier_list)

#     for config in valid_configs:
#         for i, val in enumerate(config):
#             if val == 1:
#                 mine_counts[i] += 1

#     probabilities = {}
#     for i, tile in enumerate(frontier_list):
#         probabilities[tile] = mine_counts[i] / num_configs if num_configs > 0 else 0.0

#     return probabilities

# def split_frontier_into_groups(constraints):
#     """
#     Splits the frontier tiles into groups, where each group is a set of tiles
#     connected by shared constraints.
#     Returns a list of sets, each set being a group of connected frontier tiles.
#     """
#     from collections import defaultdict, deque

#     # Build a graph: each tile is a node, edges exist if tiles appear together in a constraint
#     adjacency = defaultdict(set)
#     for tiles, _ in constraints:
#         for t1 in tiles:
#             for t2 in tiles:
#                 if t1 != t2:
#                     adjacency[t1].add(t2)

#     # Find connected components using BFS
#     visited = set()
#     groups = []

#     for tile in adjacency:
#         if tile not in visited:
#             group = set()
#             queue = deque([tile])
#             visited.add(tile)
#             while queue:
#                 current = queue.popleft()
#                 group.add(current)
#                 for neighbor in adjacency[current]:
#                     if neighbor not in visited:
#                         visited.add(neighbor)
#                         queue.append(neighbor)
#             groups.append(group)

#     return groups

# def generate_valid_configs_first_group(board):
#     frontiers, constraints = get_first_frontier_group_and_constraints(board)
#     if not frontiers:
#         return [], []
#     return generate_valid_configs(constraints, frontiers)

# def estimate_tile_probabilities_first_group(board):
#     valid_configs, frontier_list = generate_valid_configs_first_group(board)
#     if not valid_configs:
#         return {}
#     return estimate_tile_probabilities(valid_configs, frontier_list)

# def get_first_frontier_group_and_constraints(board):
#     constraints = get_constraints(board)
#     groups = split_frontier_into_groups(constraints)
#     if not groups:
#         return set(), []
#     first_group = groups[0]
#     # Only keep constraints that involve at least one tile from the first group
#     group_constraints = []
#     for tiles, mine_count in constraints:
#         if any(t in first_group for t in tiles):
#             group_constraints.append((tiles, mine_count))
#     return first_group, group_constraints



import random
import multiprocessing
from collections import defaultdict, deque
from concurrent.futures import ProcessPoolExecutor

MAX_GROUP_SIZE = 15
MONTE_CARLO_SAMPLES = 5000
MAX_WORKERS = min(multiprocessing.cpu_count(), 4)  # Cap workers for safety


# ========== Helper Functions ==========

def get_frontier_tiles(board):
    frontier_tiles = set()
    for y in range(board.rows):
        for x in range(board.cols):
            tile = board.get_tile(x, y)
            if tile.is_number:
                for neighbor in board.neighbours(x, y):
                    if neighbor.is_unrevealed:
                        frontier_tiles.add((neighbor.x, neighbor.y))
    return frontier_tiles


def get_constraints(board):
    constraints = []
    for y in range(board.rows):
        for x in range(board.cols):
            tile = board.get_tile(x, y)
            if tile.is_number:
                hidden = []
                flagged = 0
                for neighbor in board.neighbours(x, y):
                    if neighbor.is_flagged:
                        flagged += 1
                    elif neighbor.is_unrevealed:
                        hidden.append((neighbor.x, neighbor.y))
                mines = tile.number - flagged
                if hidden:
                    constraints.append((hidden, mines))
    return constraints


def split_frontier_into_groups(constraints):
    adjacency = defaultdict(set)
    for tiles, _ in constraints:
        for t1 in tiles:
            for t2 in tiles:
                if t1 != t2:
                    adjacency[t1].add(t2)

    visited = set()
    groups = []
    for tile in adjacency:
        if tile not in visited:
            group = set()
            queue = deque([tile])
            visited.add(tile)
            while queue:
                current = queue.popleft()
                group.add(current)
                for neighbor in adjacency[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            groups.append(group)
    return groups


def generate_valid_configs(constraints, frontiers):
    frontier_list = list(frontiers)
    tile_indices = {tile: i for i, tile in enumerate(frontier_list)}
    num_tiles = len(frontier_list)
    valid_configs = []

    for bits in range(1 << num_tiles):
        config = [(bits >> i) & 1 for i in range(num_tiles)]

        valid = True
        for tiles, mine_count in constraints:
            count = sum(config[tile_indices[t]] for t in tiles if t in tile_indices)
            if count != mine_count:
                valid = False
                break

        if valid:
            valid_configs.append(config)

    return valid_configs, frontier_list


def estimate_tile_probabilities(valid_configs, frontier_list):
    num_configs = len(valid_configs)
    mine_counts = [0] * len(frontier_list)
    for config in valid_configs:
        for i, val in enumerate(config):
            if val == 1:
                mine_counts[i] += 1
    return {
        frontier_list[i]: mine_counts[i] / num_configs
        for i in range(len(frontier_list))
    } if num_configs else {}


# ========== Parallel Monte Carlo ==========

def _monte_carlo_worker(constraints, frontier_list, samples):
    import random
    tile_indices = {tile: i for i, tile in enumerate(frontier_list)}
    num_tiles = len(frontier_list)
    mine_counts = [0] * num_tiles
    valid_count = 0

    for _ in range(samples):
        config = [random.choice([0, 1]) for _ in range(num_tiles)]

        valid = True
        for tiles, mine_count in constraints:
            count = sum(config[tile_indices[t]] for t in tiles if t in tile_indices)
            if count != mine_count:
                valid = False
                break

        if valid:
            valid_count += 1
            for i, val in enumerate(config):
                if val == 1:
                    mine_counts[i] += 1

    return valid_count, mine_counts


def monte_carlo_sample_parallel(constraints, frontier_list, total_samples=MONTE_CARLO_SAMPLES):
    samples_per_worker = total_samples // MAX_WORKERS
    futures = []

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for _ in range(MAX_WORKERS):
            futures.append(executor.submit(
                _monte_carlo_worker,
                constraints,
                frontier_list,
                samples_per_worker
            ))

        total_valid = 0
        combined_counts = [0] * len(frontier_list)

        for future in futures:
            valid, mine_counts = future.result()
            total_valid += valid
            for i in range(len(mine_counts)):
                combined_counts[i] += mine_counts[i]

    if total_valid == 0:
        return {}
    return {
        frontier_list[i]: combined_counts[i] / total_valid
        for i in range(len(frontier_list))
    }

# ========== Fallback Estimations ==========

def naive_local_probabilities(board):
    tile_probs = defaultdict(list)
    for y in range(board.rows):
        for x in range(board.cols):
            tile = board.get_tile(x, y)
            if not tile.is_number:
                continue

            hidden = []
            flagged = 0
            for neighbor in board.neighbours(x, y):
                if neighbor.is_flagged:
                    flagged += 1
                elif neighbor.is_unrevealed:
                    hidden.append((neighbor.x, neighbor.y))

            if hidden:
                remaining = tile.number - flagged
                prob = remaining / len(hidden)
                for t in hidden:
                    tile_probs[t].append(prob)

    return {
        t: sum(p) / len(p)
        for t, p in tile_probs.items()
    }


def estimate_global_mine_density(board):
    total_tiles = board.rows * board.cols
    revealed = 0
    flagged = 0
    for y in range(board.rows):
        for x in range(board.cols):
            tile = board.get_tile(x, y)
            if tile.is_flagged:
                flagged += 1
            elif not tile.is_unrevealed:
                revealed += 1

    remaining_mines = board.total_mines - flagged
    remaining_tiles = total_tiles - revealed - flagged
    return remaining_mines / remaining_tiles if remaining_tiles else 1.0


# ========== Final Bot Function ==========

def r3(board):
    frontiers = get_frontier_tiles(board)
    constraints = get_constraints(board)

    if not frontiers or not constraints:
        # Global fallback
        for y in range(board.rows):
            for x in range(board.cols):
                tile = board.get_tile(x, y)
                if tile.is_unrevealed and not tile.is_flagged:
                    return [(x, y)]

    groups = split_frontier_into_groups(constraints)
    best_tile = None
    best_prob = 1.0

    for group in sorted(groups, key=len):
        if len(group) > MAX_GROUP_SIZE:
            continue

        group_constraints = [
            (tiles, count)
            for tiles, count in constraints
            if any(t in group for t in tiles)
        ]

        try:
            valid_configs, frontier_list = generate_valid_configs(group_constraints, group)
            if valid_configs:
                probs = estimate_tile_probabilities(valid_configs, frontier_list)
            else:
                probs = monte_carlo_sample_parallel(group_constraints, list(group))
        except Exception:
            probs = monte_carlo_sample_parallel(group_constraints, list(group))

        for tile, prob in probs.items():
            if prob < best_prob:
                best_tile = tile
                best_prob = prob

        if best_prob == 0:
            break  # Found safe move

    if best_tile:
        return [best_tile]

    # Fallback: local heuristic
    local_probs = naive_local_probabilities(board)
    if local_probs:
        best_tile = min(local_probs, key=local_probs.get)
        return [best_tile]

    # Final fallback: global mine density guess
    for y in range(board.rows):
        for x in range(board.cols):
            tile = board.get_tile(x, y)
            if tile.is_unrevealed and not tile.is_flagged:
                return [(x, y)]

    return []










