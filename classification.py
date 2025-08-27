import mss
from PIL import Image
import cv2
import numpy as np

from classes import Tile, Board


#Function: Capture the game board (minesweeper tiles)
def capture_board(cols, rows, tile_size, top_left_x, top_left_y):
    width = cols * tile_size
    height = rows * tile_size
    game_board = {"left": top_left_x, "top": top_left_y, "width": width, "height": height}

    with mss.mss() as sct:
        screenshot = sct.grab(game_board)
        image = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        return image

# Function: Board Cropping
def crop_board(board_img, rows, cols, tile_size):
    tiles = []
    for row in range(rows):
        row_tiles = []
        for col in range(cols):
            left = col * tile_size + 1
            top = row * tile_size + 1
            right = (col + 1) * tile_size - 1
            bottom = (row + 1) * tile_size - 1

            tile = board_img.crop((left, top, right, bottom))
            row_tiles.append(tile)
        tiles.append(row_tiles)
    return tiles

# Function: Tile Classifier
def match_tile(tile, templates):
    tile = tile.resize((15, 15))  # Resize to match template size
    tile = np.array(tile, dtype=np.uint8)

    best_label = None
    best_score = float('inf')  # Since lower is better for SQDIFF

    for label, template in templates.items():
        result = cv2.matchTemplate(tile, template, cv2.TM_SQDIFF_NORMED)
        score = result[0][0]

        if score < best_score:  # Lower is better
            best_score = score
            best_label = label

    return best_label, best_score

# Function: Turn classification output into matrix
def classify_board(tiles, templates):
    rows = len(tiles)
    cols = len(tiles[0])
    board = Board(rows, cols)
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            label, score = match_tile(tile, templates)
            tile = Tile(x, y, label, confidence=score)
            board.set_tile(x, y, tile)
    return board
