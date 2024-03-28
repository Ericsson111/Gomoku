import sys
import os 
sys.path.append(os.path.dirname(os.path.realpath("__init__.py")))

from game_board import *
from winning_condition import *
from Bot import bot_logic

def clearBoard():
    Game_Board = [[' '] * board_length] * board_length
    return Game_Board

def validateInput(move):
    try:
        print(f"move: {move.split(',')}")
        row, col = move.split(',')
        if row.isdigit() and int(row) >= 0 and col.isdigit() and int(col) >= 0:
             return [int(row), int(col)] 
        else:
            print("INVALID INPUT!")
    except ValueError:
        return False 

def play_move(player):
    global Game_Board
    while True:
        move = input('{}, Select a location: '.format(player_name[player]))
        move_cord = validateInput(move) 
        if move_cord != False:
            row, col = move_cord
            break 

    if Game_Board[row][col] == ' ':
        Game_Board[row][col] = player_dict[player]
        return [row, col]
    if Game_Board[row][col] != ' ':
        print("Location already taken.")
        return play_move(player)

def GamePlay():
    global Game_Board, matchWinner, player_pieces_played
    display_board(Game_Board)
    for playerID in gameTurn:  # 0, 1, 0, 1
        if playerID == 0:
            moveCord = play_move(playerID)  # Coordinate of user's piece
            player_pieces_played.append(moveCord) 
            bot_logic.Square.evaluate_square_value()
            bot_logic.display_board(bot_logic.board)
        elif playerID == 1:
            row, col = bot_logic.Square.optimized_placement()
            Game_Board[row][col] = bot_piece
        display_board(Game_Board) 
        # Check Win Condition
        print("-"*160)
        if check_row_and_column(moveCord) or check_diagonal(moveCord):
            Game_Board = clearBoard()
            player_pieces_played = [] 
            matchWinner = player_name[playerID]
            print("{} Wins!".format(matchWinner))
            print('-------------------------------')
            break 
    if matchWinner == '':
        clearBoard()
        print("Tie Game!")
        print('-------------------------------')

GamePlay()
