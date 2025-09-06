import threading
import keyboard
import pyautogui
import cv2
import time

from classes import Board, Tile
from classification import capture_board, crop_board, classify_board
from rules import r1, r2
from probability import ProbabilitySolver

pyautogui.PAUSE = 0

# Global Variables
import global_variables

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
    "F": cv2.cvtColor(cv2.imread("assets/flag.png"), cv2.COLOR_BGR2RGB),
    "M": cv2.cvtColor(cv2.imread("assets/mine.png"), cv2.COLOR_BGR2RGB)
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
    exit_thread = threading.Thread(target=check_for_exit)
    exit_thread.daemon = True # Thread will exit when main program exits
    exit_thread.start()

    # Start the game
    pyautogui.moveTo(global_variables.TOP_LEFT_X + ((global_variables.TILE_SIZE // 2) * global_variables.COLS) , global_variables.TOP_LEFT_Y + ((global_variables.TILE_SIZE // 2) * global_variables.ROWS)) # Start on the center tile
    pyautogui.click()

    time.sleep(0.1)

    while not should_exit:
        board_image = capture_board(global_variables.COLS, global_variables.ROWS, global_variables.TILE_SIZE, global_variables.TOP_LEFT_X, global_variables.TOP_LEFT_Y)
        # board_image.save("test.png") # Use to debug board capture

        tiles = crop_board(board_image, global_variables.ROWS, global_variables.COLS, global_variables.TILE_SIZE)
        board_state = classify_board(tiles, classification_templates)
        board_state.display()

        if not board_state.has_mines(): # If no mines have been clicked
            tiles_to_flag = r1(board_state)
            board_state.flag_tiles(tiles_to_flag)
            tiles_to_clear = r2(board_state)
            board_state.clear_tiles(tiles_to_clear)
            time.sleep(0.1) 

            if len(tiles_to_flag) == 0 and len(tiles_to_clear) == 0: # If no more moves detected
                if board_state.has_hidden_tiles(): # If the board still containes hidden tiles
                    solver = ProbabilitySolver(board_state)
                    tile, prob = solver.get_best_tile()
                    print(f"Best guess: {tile} with mine probability {prob:.2%}")








                    # print("No more actions available. Restarting...")
                    # board_state.reset() # Restart the game
                    # time.sleep(0.5)
                    # pyautogui.moveTo(global_variables.TOP_LEFT_X + ((global_variables.TILE_SIZE // 2) * global_variables.COLS) , global_variables.TOP_LEFT_Y + ((global_variables.TILE_SIZE // 2) * global_variables.ROWS)) # Start on the center tile
                    # pyautogui.click()
                    # time.sleep(0.1)
                else: # Means the game is complete
                    print("Game Complete. Exiting...")
                    should_exit = True
                    break
        else: # If a mine has been clicked, restard the game
            print("A mine has exploded. Restarting...")
            board_state.reset()
            time.sleep(0.5)
            pyautogui.moveTo(global_variables.TOP_LEFT_X + ((global_variables.TILE_SIZE // 2) * global_variables.COLS) , global_variables.TOP_LEFT_Y + ((global_variables.TILE_SIZE // 2) * global_variables.ROWS)) # Start on the center tile
            pyautogui.click()
            time.sleep(0.1)




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