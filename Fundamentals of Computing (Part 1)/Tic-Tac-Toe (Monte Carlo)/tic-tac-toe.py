"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 500         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 5.0   # Score for squares played by the other player
    
# Add your functions here.

def mc_trial(board, player):
    '''Runs a monte carlo tic-tac-toe trial'''
    empty_squares = board.get_empty_squares()
    for dummy_choice in list(empty_squares):
        empty_square = random.choice(empty_squares)
        board.move(empty_square[0], empty_square[1], player)
        empty_squares.remove(empty_square)
        player = provided.switch_player(player)
        winner = board.check_win()
        if winner == provided.PLAYERX or winner == provided.PLAYERO:
            break

def mc_update_scores(scores, board, player):
    '''updates the score board after the monte calo tic-tac-toe trial'''
    other_player = provided.switch_player(player)
    winner = board.check_win()
    dim = board.get_dim()
    
    if winner == player:        
        for col in ((x, y) for x in xrange(dim) for y in xrange(dim)):
            if player == board.square(col[0], col[1]):
                scores[col[0]][col[1]] += SCORE_CURRENT
            if other_player == board.square(col[0], col[1]):
                scores[col[0]][col[1]] -= SCORE_OTHER
                
    if winner == other_player:
        for col in ((x, y) for x in xrange(dim) for y in xrange(dim)):
            if player == board.square(col[0], col[1]):
                scores[col[0]][col[1]] -= SCORE_CURRENT
            if other_player == board.square(col[0], col[1]):
                scores[col[0]][col[1]] += SCORE_OTHER

def get_best_move(board, scores):
    '''chooses the best move to make on board judging from scores'''
    empty_squares = board.get_empty_squares()
    best_move = empty_squares[0]
    best_moves = []
    for square in empty_squares:
        if scores[square[0]][square[1]] == scores[best_move[0]][best_move[1]]:
            best_moves.append((square[0], square[1]))
        elif scores[square[0]][square[1]] > scores[best_move[0]][best_move[1]]:
            best_move = (square[0], square[1])
            best_moves = []
            best_moves.append((square[0], square[1]))
    print best_moves
    return random.choice(best_moves)
        
    

def mc_move(board, player, trials):
    '''Returns a square in which player should make a move'''
    dim = board.get_dim()
    score_board = [[0 for dummy_y in xrange(dim)] for dummy_x in xrange(dim)]
    
    for dummy_trial in xrange(trials):
        mc_board = board.clone()
        mc_trial(mc_board, player)
        mc_update_scores(score_board, mc_board, player)
        
    return get_best_move(board, score_board)


# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
