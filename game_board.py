
# Define Game Board
# Game Board Size: 10x10
board_length = 10
Game_Board = [[' ' for _ in range(board_length)] for _ in range(board_length)]
gameTurn = [0, 1] * (board_length ** 2 // 2) if board_length ** 2 % 2 == 0 else [0, 1] * ((board_length ** 2 - 1) // 2) + [0]

# Define Game Piece and Player 
player_piece = 'O'
bot_piece = 'X'
player_dict = {0: 'O', 1: 'X'}
player_name = {0: 'Player', 1: 'Guest'}
player_pieces_played = [] # Coordinates of all pieces played by the player

# Define Match Winner
matchWinner = ''

# Display Board
def display_board(board):
    num_cols = len(board[0])
    num_rows = len(board)

    # Print column numbers
    col_num_str = '    '
    for col in range(num_cols):
        col_num_str += f' {col}  '
    print(col_num_str)

    # Print top border
    print('   +' + '-' * (num_cols * 4 - 1) + "+")

    # Print rows
    for row in range(num_rows):
        if row < 10:
            row_str = f'{row}  |'
        else:
            row_str = f'{row} |'
        for col in range(num_cols):
            row_str += ' {} |'.format(board[row][col])
        print(row_str)

        # Print bottom border
        print('   +' + '-' * (num_cols * 4 - 1) + "+")

def clearBoard():
    global Game_Board
    Game_Board = [[' ' for _ in range(board_length)] for _ in range(board_length)]

