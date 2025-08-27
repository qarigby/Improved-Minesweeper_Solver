import threading
import keyboard
import pyautogui
import cv2
import time

from classes import Board, Tile
from classification import capture_board, crop_board, classify_board
from rules import r1, r2

# Setting the timeout between clicks (FASTER CLICKING!!!!!!!)
pyautogui.PAUSE = 0
# or do this
# pyautogui.click(clicks=10, interval=0)  # 10 rapid clicks etc...


# Global Variables
TOP_LEFT_X = 1046
TOP_LEFT_Y = 202
TILE_SIZE = 16
ROWS = 9
COLS = 9
NUM_MINES = 10

classification_templates = {
    "1": cv2.cvtColor(cv2.imread("assets/1.png"), cv2.COLOR_BGR2RGB),
    "2": cv2.cvtColor(cv2.imread("assets/2.png"), cv2.COLOR_BGR2RGB),
    "3": cv2.cvtColor(cv2.imread("assets/3.png"), cv2.COLOR_BGR2RGB),
    "4": cv2.cvtColor(cv2.imread("assets/4.png"), cv2.COLOR_BGR2RGB),
    "5": cv2.cvtColor(cv2.imread("assets/5.png"), cv2.COLOR_BGR2RGB),
    "6": cv2.cvtColor(cv2.imread("assets/6.png"), cv2.COLOR_BGR2RGB),
    "7": cv2.cvtColor(cv2.imread("assets/7.png"), cv2.COLOR_BGR2RGB),
    "8": cv2.cvtColor(cv2.imread("assets/8.png"), cv2.COLOR_BGR2RGB),
    "E": cv2.cvtColor(cv2.imread("assets/empty.png"), cv2.COLOR_BGR2RGB),
    "H": cv2.cvtColor(cv2.imread("assets/hidden.png"), cv2.COLOR_BGR2RGB),
    "F": cv2.cvtColor(cv2.imread("assets/flag.png"), cv2.COLOR_BGR2RGB)
}

should_exit = False

def check_for_exit():
    global should_exit
    keyboard.wait('q')  # Blocks until 'q' is pressed
    should_exit = True
    print("\nq key detected. Stopping program...")

# Run the program
if __name__  == "__main__":

    print("Press 'q' to stop the program.")

    # Start a thread to monitor for the exit key
    # exit_thread = threading.Thread(target=check_for_exit)
    # exit_thread.daemon = True # Thread will exit when main program exits
    # exit_thread.start()

    # Start the game
    pyautogui.moveTo(TOP_LEFT_X + ((TILE_SIZE // 2) * COLS) , TOP_LEFT_Y + ((TILE_SIZE // 2) * ROWS)) # Start on the center tile
    pyautogui.click()

    # while not should_exit:
    board_image = capture_board(COLS, ROWS, TILE_SIZE, TOP_LEFT_X, TOP_LEFT_Y)
    tiles = crop_board(board_image, ROWS, COLS, TILE_SIZE)
    board_state = classify_board(tiles, classification_templates)
    # board_state.display()
    r1(board_state)
    r2(board_state)
    # time.sleep(1)




"""
Steps:

1. Start the game by clicking on the middle tile #
2. Capture the current board state #
3. Classify the tiles based on the colour of the number / absense of pixel in each frame of the tile #
4. Update board state matrix using classifications #
5. Calculate moves based on current board state 
6. Make batch moves based on calculations
7. Repeat 2-6
8. Implement logic to detect if the game is over
9. 

"""