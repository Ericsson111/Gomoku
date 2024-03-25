import sys
import os 
sys.path.append(os.path.dirname(os.path.realpath("__init__.py")))

from collections import deque 

from game_board import *
from winning_condition import *

""" 
Initialize Matrix that represents the probability score of each squre (start of with 0)
Identify all the player pieces on board
Create object attributes for all the pieces (Related arrays -> horizontal, vertical, diagonal and also their coordinates)
Gather all the coordinates that are within the range of all the player pieces and count the amount of reoccurance of each coordinate(# of Intersections).
Update these scores onto the matrix
Identify the coordinate(square) with the highest probability score
"""

board = []  # This will hold rows of Square objects

class Square():
    def __init__(self, coordinate, score):
        self.coordinate = coordinate 
        self.score = score 

    def breaking_array(array):
        # Convert coordinates array to visual(board) array -> consisting spaces/pieces
        array1 = [Game_Board[cord[0]][cord[1]] for cord in array]
        """ 
        array: [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9)]   array1: [' ', ' ', ' ', 'O', ' ', ' ', ' ', ' ', ' ', ' ']
        array: [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3)]   array1: [' ', ' ', 'O', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        array: [(0, 5), (1, 4), (2, 3), (3, 2), (4, 1), (5, 0)]                                   array1: [' ', ' ', 'O', ' ', ' ', ' ']
        array: [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)]           array1: [' ', ' ', 'O', 'X', 'O', ' ', ' ', ' ', ' ']
        """

        botPieceCount = array1.count(bot_piece)
        if botPieceCount >= 1: # x >= 1 case (combined)

            for _ in range(botPieceCount):
                pieceInd = array1.index(bot_piece) 
                leftArray = array1[:pieceInd] 
                rightArray = array1[pieceInd+1:] 
                print(f"array: {array1}") 
                print(f"leftArray: {leftArray}, rightArray: {rightArray}") 

                if bot_piece in leftArray:
                    return Square.breaking_array(array[:pieceInd])
                if bot_piece in rightArray:
                    return Square.breaking_array(array[pieceInd+1:])
                else: # Bot piece in neither array 
                    # Measure length of array
                    arr = [array[:pieceInd], array[pieceInd+1:]]
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
            print(f"{array1} is sufficient for player to win")

    def evaluate_square_value():
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

    def danger_level_evaluation(cord_array: list, visual_array: list):
        # The further the square is away from the player piece, the lower it gets -> decrement/square = 0.1 and begins at 1
        # Distance based dynamic scoring
        player_piece_Ind = visual_array.index(player_piece) 
        row, col = cord_array[player_piece_Ind]
        board[row][col].score += 1
        
        left_increment = 1
        right_increment = 1
        distant_decrement = -0.1

    def sort_square_score() -> list:
        # [0,0] = 0, [1,1] = 0, [1,2] = 1
        # Find the "highest score" in each row and compare them
        peak = []

        for rowID in range(len(board_length)):         

            max_score = 0
            max_row_coordinates = [] # Perchance for tied maximum score 

            # Iterate and find greatest possibility value
            for colID in range(len(board_length)):

                square = board[rowID][colID]
                square_score = square.score

                if square_score > max_score:
                    max_score = square_score
                    max_row_coordinates.append([rowID, colID]) 
            
            peak.append(max_row_coordinates)

        return peak 

# Initializing Coordinate and Score attributes into each square
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


# player_piece -> Stores all the coordinates of pieces played by player
# Queue for Scanning: Implement a queue system to efficiently manage and scan board squares. When a new piece is placed, 
# add the surrounding squares to the queue for reevaluation since the strategic value of these squares has likely changed due to the new piece.

