import sys
import os 
sys.path.append(os.path.dirname(os.path.realpath("__init__.py")))

from collections import deque 
import itertools

from game_board import *
from winning_condition import *

board = []  # This will hold rows of Square objects

class Square():
    def __init__(self, coordinate, score):
        self.coordinate = coordinate 
        self.score = score 

    def breaking_array(cord_array):
        # Convert coordinates array to visual(board) array -> consisting spaces/pieces
        visual_array = [Game_Board[cord[0]][cord[1]] for cord in cord_array]
        botPieceCount = visual_array.count(bot_piece)
        
        if botPieceCount >= 1: # x >= 1 case (combined)

            for _ in range(botPieceCount):
                pieceInd = visual_array.index(bot_piece) 
                row, col = cord_array[pieceInd]
                board[row][col].score = 'X'
                leftArray = visual_array[:pieceInd] 
                rightArray = visual_array[pieceInd+1:] 
                print(f"array: {visual_array}") 
                print(f"leftArray: {leftArray}, rightArray: {rightArray}") 

                if bot_piece in leftArray:
                    return Square.breaking_array(cord_array[:pieceInd])
                if bot_piece in rightArray:
                    return Square.breaking_array(cord_array[pieceInd+1:])
                else: # Bot piece in neither array 
                    # Measure length of array
                    arr = [cord_array[:pieceInd], cord_array[pieceInd+1:]]
                    arr1 = [leftArray, rightArray]
                    for arrID in range(2):  # Loop over both left/right arrays
                        if len(arr1[arrID]) >= 5:
                            if player_piece in arr1[arrID]:
                                print(f"{arr1[arrID]} is sufficient for player to win and require danger level ratings")
                                return Square.danger_level_evaluation(arr[arrID], arr1[arrID])  
                            else:
                                print(f"{arr1[arrID]} is sufficient for player to win")
                        else:
                            print(f"{arr1[arrID]} is insufficient for player to win")
        else: # x = 0 case
            print(f"{visual_array} is sufficient for player to win")
            return Square.danger_level_evaluation(cord_array, visual_array) 

    def evaluate_square_value():
        refresh_score_board() 
        player_piece_queue = deque(player_pieces_played)
        while len(player_piece_queue) != 0:
            player_coordinate = player_piece_queue.popleft() 
            horizontal, vertical, positive_diagonal, negative_diagonal = combine_directional_coordinates(player_coordinate)
            arrays = [horizontal, vertical, positive_diagonal[::-1], negative_diagonal]
            array_names = ["Horizontal", "Vertical", "Positive Diagonal", "Negative Diagonal"]

            for arrayID in range(len(arrays)):
                print(f"------------------------------ {player_coordinate}: {array_names[arrayID]} Array ------------------------------")
                if len(arrays[arrayID]) >= 5:
                    Square.breaking_array(arrays[arrayID])  
                else:
                    print(f"{arrays[arrayID]} is insufficient for player to win")

    @staticmethod
    def danger_level_evaluation(cord_array, visual_array):
        global player_coordinate
        
        player_piece_Ind = visual_array.index(player_piece)
        row, col = cord_array[player_piece_Ind]
        
        # Check if the score has already been incremented for this coordinate
        board[row][col].score = 'O' 
        
        increment = 1
        distant_decrement = -0.1

        # Score adjustment for squares before and after the player piece
        for l in range(player_piece_Ind-1, -1, -1):
            distant = player_piece_Ind - l
            row, col = cord_array[l]
            if board[row][col].score != 'O':
                current_score = max(board[row][col].score + (increment + (distant_decrement * distant)), 0)
                board[row][col].score = round(current_score, 1)

        for r in range(player_piece_Ind+1, len(cord_array)):
            distant = r - player_piece_Ind
            row, col = cord_array[r]
            if board[row][col].score != 'O':
                current_score = max(board[row][col].score + (increment + (distant_decrement * distant)), 0)
                board[row][col].score = round(current_score, 1)

    def optimized_placement():
        peaks = Square.max_square_score() 
        score = {}
        for ind in range(len(peaks)):
            row, col = peaks[ind][1]
            horizontal, vertical, positive_diagonal, negative_diagonal = combine_directional_coordinates([row, col])

            horizontal = [Game_Board[cord[0]][cord[1]] for cord in horizontal]
            vertical = [Game_Board[cord[0]][cord[1]] for cord in vertical]
            positive_diagonal = [Game_Board[cord[0]][cord[1]] for cord in positive_diagonal]
            negative_diagonal = [Game_Board[cord[0]][cord[1]] for cord in negative_diagonal]

            score[ind] = [max([horizontal.count(player_piece), vertical.count(player_piece), positive_diagonal.count(player_piece),\
                                negative_diagonal.count(player_piece)]), board[row][col].score, [row, col]]

        # Sort through score
        # Objective: Find max # of player pieces AND max square score 
        max_square_value = 0
        max_piece_count = 0
        max_coordinate = None 
        # score: {0: [1, 0.6, [0, 1]], 1: [1, 0.6, [0, 5]], 2: [1, 0.6, [0, 9]], 3: [1, 0.7, [1, 2]]}
        for ind in range(len(score)):
            piece_count, square_val, cord = score[ind] # [1, 0.6, [0, 1]]
            if square_val >= max_square_value and piece_count >= max_piece_count: # Higher danger level score
                max_square_value = square_val 
                max_piece_count = piece_count
                max_coordinate = cord  
        print(f"max_piece_count: {max_piece_count}, max_square_value: {max_square_value}, max_coordinate: {max_coordinate}") 
        return max_coordinate 

    def max_square_score():
        # Find the maximum score on each row and compare
        row_peaks = {}
        for rowID in range(board_length):
            
            max_val = max([[board[rowID][i].score, [rowID, i]] for i in range(len(board[rowID])) if isinstance(board[rowID][i].score, float)])
            max_vals = [[board[rowID][i].score, [rowID, i]] for i in range(len(board[rowID])) if board[rowID][i].score == max_val[0]]
            row_peaks[rowID] = max_vals 

        # Send row peaks through 
        return flatten_list([i for i in row_peaks.values()])


def flatten_list(nested_list):
    one_dimensional_array = []

    # Iterate through each sublist in the nested list
    for sublist in nested_list:
        # Then, iterate through each item in the sublist
        for item in sublist:
            # Add the item to the one-dimensional array
            one_dimensional_array.append(item)

    return one_dimensional_array

def refresh_score_board():
    global board 
    # Initializing Coordinate and Score attributes into each square
    board = [] 
    for rowID in range(board_length):
        row = []  # Initialize an empty row
        for colID in range(board_length):
            square = Square([rowID, colID], 0.0)  # Create a Square object for this position
            row.append(square)  # Add the Square to the row
        board.append(row)  # Add the completed row to the board


def display_board(board):
    num_rows = len(board)
    num_cols = len(board[0]) if num_rows > 0 else 0

    # Calculate the maximum score length for consistent formatting
    max_score_length = max(len(f"{square.score}") for row in board for square in row)
    column_width = max(max_score_length + 2, 5)  # Ensure minimum spacing for readability

    # Print column headers
    col_header = " " * 4 + " ".join(f"{col:^{column_width}}" for col in range(num_cols))
    print(col_header)

    # Print top border
    print("   +" + "-" * (num_cols * (column_width + 1) - 1) + "+")

    # Display each row with scores
    for row_idx, row in enumerate(board):
        # Row label
        row_str = f"{row_idx:<3}|"
        for square in row:
            # Format score with one decimal place, centered within the column
            formatted_score = f"{square.score}".center(column_width)
            row_str += f"{formatted_score}|"
        print(row_str)

        # Print row separator
        print("   +" + "-" * (num_cols * (column_width + 1) - 1) + "+")
