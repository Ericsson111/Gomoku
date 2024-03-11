import sys
import os 
sys.path.append(os.path.dirname(os.path.realpath("__init__.py")))

from game_board import *
from winning_condition import *

board = []  # This will hold rows of Square objects

class Square():
    def __init__(self, coordinate, score):
        self.coordinate = coordinate 
        self.score = score 

    def update_square_score(playerID: int, player_coordinate: list):
        # player_piece -> Stores all the coordinates of pieces played by player
        # Dynamic Scoring: The score of each square can be dynamically updated throughout the game based on new pieces being added to the board. 
        # The score of every square that are related to the player's latest piece will be reviewed
        if playerID == 0: # Player Piece
            horizontal, vertical, positive_diagonal, negative_diagonal = combine_directional_coordinates(player_coordinate)
            combined = [horizontal, vertical, positive_diagonal, negative_diagonal]
            coordinates = horizontal + vertical + positive_diagonal + negative_diagonal

            # The further the square is away from the player piece, the lower it gets -> decrement/square = 0.1 and begins at 1
            ldecrement = 1 
            rdecrement = 1

            # Apply "Distance Based Scoring"
            for array in combined:
                # horizontal -> vertical -> positive_diagonal -> negative_diagonal
                row, col = player_coordinate
                current_ind = array.index((row, col)) 
                leftOfArray = current_ind
                rightOfArray = len(array) - (current_ind + 1) 

                # 2 for loops for travelling in both direction
                for l in range(leftOfArray + 1):
                    row, col = array[current_ind - l]
                    square = board[row][col]
                    square.score = round(square.score + ldecrement, 1)
                    ldecrement -= 0.1

                for r in range(rightOfArray + 1):
                    row, col = array[current_ind + r]
                    square = board[row][col]
                    square.score = round(square.score + rdecrement, 1)
                    rdecrement -= 0.1

                # Reset distance decrement
                ldecrement = 1
                rdecrement = 1

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
