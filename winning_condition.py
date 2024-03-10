from game_board import *

player_win_condition = "OOOOO"
bot_win_condition = "XXXXX"

# Identify Coordinates
def horizontal_coordinates(player_coordinate: list) -> list:
    print(player_coordinate)
    row = int(player_coordinate[0])
    
    Game_Board_Row = [(row, i) for i in range(board_length)]
    return sorted(Game_Board_Row)

def vertial_coordinates(player_coordinate: list) -> list:
    print(player_coordinate)
    col = int(player_coordinate[1])

    Game_Board_Col = [(i, col) for i in range(board_length)]
    return sorted(Game_Board_Col)

def positive_diagonal_coordinates(player_coordinate: list) -> list:
    # Pieced placed in row/col
    row = int(player_coordinate[0])
    col = int(player_coordinate[1])

    # Store points
    coordinates = []
    coordinates.append((row, col))

    # Coordinates that are Right + Up from the reference point
    rightUpRange = min(row, board_length - (col + 1)) #min(col_space, row_space)
    for _ in range(rightUpRange):
        row = row - 1
        col = col + 1
        if row >= 0 and col <= board_length - 1:
            coordinates.append((row, col))

    # Coordiantes that are Left + Down from the reference point
    leftDownRange = min(board_length - (row + 1), col)
    for _ in range(leftDownRange):
        row = row + 1
        col = col - 1
        if col >= 0 and row <= board_length - 1:
            if (row, col) not in coordinates:
                coordinates.append((row, col))
    print(f"positive diagonal: {sorted(coordinates)}")
    return sorted(coordinates)

def negative_diagonal_coordinates(player_coordinate: list) -> list:
    # Pieced placed in row/col
    row = int(player_coordinate[0])
    col = int(player_coordinate[1])

    # Store points
    coordinates = []
    coordinates.append((row, col))

    # Coordinates that are Left + Up from the reference point 
    leftUpRange = min(row, col)
    for _ in range(leftUpRange):
        row = row - 1
        col = col - 1

        if row >= 0 and col >= 0:
            coordinates.append((row, col))

    # Coordinates that are Right + Down from the reference point
    rightDownRange = min(board_length - (row + 1), board_length - (col + 1))
    for _ in range(rightDownRange):
        row = row + 1
        col = col + 1

        if row <= board_length - 1 and col <= board_length - 1:
            if (row, col) not in coordinates:
                coordinates.append((row, col))
    
    print(f"negative diagonal: {sorted(coordinates)}")
    return sorted(coordinates)

def combine_directional_coordinates(player_coordinate: list) -> list:
    horizontal = horizontal_coordinates(player_coordinate)
    vertical = vertial_coordinates(player_coordinate)
    positive_diagonal = positive_diagonal_coordinates(player_coordinate)
    negative_diagonal = negative_diagonal_coordinates(player_coordinate)
    return [horizontal, vertical, positive_diagonal, negative_diagonal]

# Winning Conditions
def check_row_and_column(player_coordinate: list) -> bool:
    # Pieced placed in row/col
    row = int(player_coordinate[0])
    col = int(player_coordinate[1])

    Game_Board_Row = ''.join(Game_Board[row])
    Game_Board_Col = ''.join([Game_Board[row][col] for row in range(0, board_length)])
    
    # Return current game status
    if player_win_condition in Game_Board_Row or player_win_condition in Game_Board_Col:
        return True 
    elif bot_win_condition in Game_Board_Row or bot_win_condition in Game_Board_Col:
        return True
    else:
        return False 
    
def check_diagonal(player_cord: list) -> bool:
    # Lists contained all coordiantes for the points
    posSlopeArr = positive_diagonal_coordinates(player_cord)
    negSlopeArr = negative_diagonal_coordinates(player_cord)
  
    # Define lists to store point value
    posSlopeVal = ''.join([Game_Board[cord[0]][cord[1]] for cord in posSlopeArr])
    negSlopeVal = ''.join([Game_Board[cord[0]][cord[1]] for cord in negSlopeArr])

    if player_win_condition in posSlopeVal or player_win_condition in negSlopeVal:
        return True 
    elif bot_win_condition in posSlopeVal or bot_win_condition in negSlopeVal:
        return True 
    else:
        return False
