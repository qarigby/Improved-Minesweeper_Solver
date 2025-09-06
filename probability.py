from itertools import product

class ProbabilitySolver:
    def __init__(self, board):
        self.board = board
        self.frontiers = set()
        self.constraints = []

    def in_bounds(self, r, c):
        return 0 <= r < self.board.rows and 0 <= c < self.board.cols
     
    def get_frontier_tiles(self):
        self.frontiers.clear()
        for y in range(self.board.rows):
            for x in range(self.board.cols):
                tile = self.board.get_tile(x,y)
                if tile.is_number:
                    if not tile.is_unrevealed:
                        for neighbour in self.board.neighbours(x,y):
                            if neighbour.is_unrevealed:
                                self.frontiers.add((neighbour.x, neighbour.y))

    def get_constraints(self):
        self.constraints.clear()
        for y in range(self.board.rows):
            for x in range(self.board.cols):
                if self.board.is_revealed_number(r, c):
                    covered_neighbors = []
                    flagged_neighbors = 0
                    for dr, dc in self.directions:
                        nr, nc = r + dr, c + dc
                        if not self.in_bounds(nr, nc):
                            continue
                        if self.board.is_covered(nr, nc):
                            covered_neighbors.append((nr, nc))
                        elif self.board.is_flagged(nr, nc):
                            flagged_neighbors += 1

                    clue = self.board.grid[r][c].number
                    remaining_mines = clue - flagged_neighbors
                    if covered_neighbors and remaining_mines >= 0:
                        self.constraints.append((covered_neighbors, remaining_mines))

    def generate_valid_configs(self):
        tile_list = list(self.frontiers)
        tile_index = {tile: i for i, tile in enumerate(tile_list)}
        num_tiles = len(tile_list)
        configs = []

        for bits in product([0, 1], repeat=num_tiles):
            config = list(bits)
            valid = True
            for tiles, mines in self.constraints:
                count = sum(config[tile_index[t]] for t in tiles if t in tile_index)
                if count != mines:
                    valid = False
                    break
            if valid:
                configs.append(config)

        return configs, tile_list
    
    def estimate_probabilities(self):
        self.get_frontier_tiles()
        self.get_constraints()

        if not self.frontiers:
            return {}

        configs, tile_list = self.generate_valid_configs()
        if not configs:
            return {}

        mine_counts = [0] * len(tile_list)
        for config in configs:
            for i, val in enumerate(config):
                if val == 1:
                    mine_counts[i] += 1
        num_configs = len(configs)
        probabilities = {
            tile_list[i]: mine_counts[i] / num_configs
            for i in range(len(tile_list))
        }
        return probabilities

    def get_best_tile(self):
        probabilities = self.estimate_probabilities()
        unopened = set(self.board.get_unopened_tiles())
        frontier_tiles = set(probabilities.keys())
        non_frontier = unopened - frontier_tiles

        if probabilities:
            best_tile = min(probabilities.items(), key=lambda x: x[1])
            min_prob = best_tile[1]
        else:
            best_tile = None
            min_prob = None

        if non_frontier:
            remaining_mines = self.board.get_remaining_mines()
            remaining_tiles = len(unopened)
            global_prob = remaining_mines / remaining_tiles if remaining_tiles > 0 else 1.0

            if min_prob is None or global_prob < min_prob:
                return list(non_frontier)[0], global_prob
            else:
                return best_tile
        else:
            return best_tile