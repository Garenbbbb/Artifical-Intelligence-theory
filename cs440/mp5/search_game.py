from distutils.file_util import move_file
import math

import chess.lib
from chess.lib.utils import encode, decode
from chess.lib.heuristics import evaluate
from chess.lib.core import makeMove

###########################################################################################
# Utility function: Determine all the legal moves available for the side.
# This is modified from chess.lib.core.legalMoves:
#  each move has a third element specifying whether the move ends in pawn promotion
def generateMoves(side, board, flags):
	for piece in board[side]:
		fro = piece[:2]
		for to in chess.lib.availableMoves(side, board, piece, flags):
			promote = chess.lib.getPromote(None, side, board, fro, to, single=True)
			yield [fro, to, promote]
			
###########################################################################################
# Example of a move-generating function:
# Randomly choose a move.
def random(side, board, flags, chooser):
	'''
	Return a random move, resulting board, and value of the resulting board.
	Return: (value, moveList, boardList)
	  value (int or float): value of the board after making the chosen move
	  moveList (list): list with one element, the chosen move
	  moveTree (dict: encode(*move)->dict): a tree of moves that were evaluated in the search process
	Input:
	  side (boolean): True if player1 (Min) plays next, otherwise False
	  board (2-tuple of lists): current board layout, used by generateMoves and makeMove
	  flags (list of flags): list of flags, used by generateMoves and makeMove
	  chooser: a function similar to random.choice, but during autograding, might not be random.
	'''
	moves = [ move for move in generateMoves(side, board, flags) ]
	if len(moves) > 0:
		move = chooser(moves)
		newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
		value = evaluate(newboard)
		return (value, [ move ], { encode(*move): {} })
	else:
		return (evaluate(board), [], {})

###########################################################################################
# Stuff you need to write:
# Move-generating functions using minimax, alphabeta, and stochastic search.

# side, board, flags = convertMoves("")

# # Iterate over all moves that are legal from the current  board position.  
# for move in generateMoves(side,board,flags):
#     newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
#     print(move, newflags)

def minimax(side, board, flags, depth):
	'''
	Return a minimax-optimal move sequence, tree of all boards evaluated, and value of best path.
	Return: (value, moveList, moveTree)
	  value (float): value of the final board in the minimax-optimal move sequence
	  moveList (list): the minimax-optimal move sequence, as a list of moves
	  moveTree (dict: encode(*move)->dict): a tree of moves that were evaluated in the search process
	Input:
	  side (boolean): True if player1 (Min) plays next, otherwise False
	  board (2-tuple of lists): current board layout, used by generateMoves and makeMove
	  flags (list of flags): list of flags, used by generateMoves and makeMove
	  depth (int >=0): depth of the search (number of moves)
	'''
	#raise NotImplementedError("you need to write this!")
	# if depth = 0 or node is a terminal node then
	#     return the heuristic value of node
	# if maximizingPlayer then
	#     value := âˆ’âˆž
	#     for each child of node do
	#         value := max(value, minimax(child, depth âˆ’ 1, FALSE))
	#     return value
	# else (* minimizing player *)
	#     value := +âˆž
	#     for each child of node do
	#         value := min(value, minimax(child, depth âˆ’ 1, TRUE))
	#     return value

	  #print(move, newflags)
	Mlist = []
	Mtree = {}
	a = minimax_helper(side, board, flags, depth, Mlist, Mtree)

	return a, Mlist, Mtree

def minimax_helper(side, board, flags, depth, Mlist, Mtree):
	if depth == 0:
		score = evaluate(board)
		return score
	if side:
		best_move = []	
		value = 99999
		for move in generateMoves(side,board,flags):
			#print(move)
			newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
			encoded_move = encode(move[0], move[1], move[2])
			Mtree.update({encoded_move: {}})
			cur = minimax_helper(newside, newboard, newflags, depth - 1, Mlist, Mtree[encoded_move])
			#print(Mlist, cur, value, move)
			if cur < value:
				best_move = move
				value = cur
				if depth == 1:
					continue
				if len(Mlist) > depth - 1:
					Mlist.pop(-1)
			else:
				if depth == 1:
					continue
				if len(Mlist) > depth - 1:
					Mlist.pop(-2) 
		#print("1 -",best_move)
		Mlist.insert(0, best_move)
		return value
	else:
		best_move = []
		value = -99999	
		for move in generateMoves(side,board,flags):
			newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
			encoded_move = encode(move[0], move[1], move[2])
			Mtree.update({encoded_move: {}})
			cur = minimax_helper(newside, newboard, newflags, depth - 1, Mlist, Mtree[encoded_move])
			if cur > value:
				best_move = move
				value = cur
				if depth == 1:
					continue
				if len(Mlist) > depth - 1:
					Mlist.pop(-1)
			else:
				if depth == 1:
					continue
				if len(Mlist) > depth - 1:
					Mlist.pop(-2)
		#print("2 -",best_move)
		Mlist.insert(0, best_move)
		return value
		
	
	

def alphabeta(side, board, flags, depth, alpha=-math.inf, beta=math.inf):
	'''
	Return minimax-optimal move sequence, and a tree that exhibits alphabeta pruning.
	Return: (value, moveList, moveTree)
	  value (float): value of the final board in the minimax-optimal move sequence
	  moveList (list): the minimax-optimal move sequence, as a list of moves
	  moveTree (dict: encode(*move)->dict): a tree of moves that were evaluated in the search process
	Input:
	  side (boolean): True if player1 (Min) plays next, otherwise False
	  board (2-tuple of lists): current board layout, used by generateMoves and makeMove
	  flags (list of flags): list of flags, used by generateMoves and makeMove
	  depth (int >=0): depth of the search (number of moves)
	'''
	# function alphabeta(node, depth, Î±, Î², maximizingPlayer) is
    # if depth = 0 or node is a terminal node then
    #     return the heuristic value of node
    # if maximizingPlayer then
    #     value := âˆ’âˆž
    #     for each child of node do
    #         value := max(value, alphabeta(child, depth âˆ’ 1, Î±, Î², FALSE))
    #         if value â‰¥ Î² then
    #             break (* Î² cutoff *)
    #         Î± := max(Î±, value)
    #     return value
    # else
    #     value := +âˆž
    #     for each child of node do
    #         value := min(value, alphabeta(child, depth âˆ’ 1, Î±, Î², TRUE))
    #         if value â‰¤ Î± then
    #             break (* Î± cutoff *)
    #         Î² := min(Î², value)
    #     return value=
	Mlist = []
	Mtree = {}
	value, Mlist = alphabeta_helper(side, board, flags, depth, Mlist, Mtree, alpha, beta)
	return value, Mlist, Mtree
	
	
def alphabeta_helper(side, board, flags, depth, Mlist, Mtree, alpha, beta):
	moveList = []
	if depth == 0:
		score = evaluate(board)
		return score, moveList
	if side:
		best_move = []	
		value = math.inf
		for move in generateMoves(side,board,flags):
			#print(move)
			newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
			encoded_move = encode(move[0], move[1], move[2])
			Mtree.update({encoded_move: {}})
			cur, Mlist= alphabeta_helper(newside, newboard, newflags, depth - 1, Mlist, Mtree[encoded_move], alpha, beta)
			#print(Mlist, cur, value, move)
			if cur < value:
				best_move = move
				moveList = Mlist
				value = cur
			if value <= alpha:
				break
			beta = min(beta, value)
		#print("1 -",best_move)
		Mlist = [best_move] + moveList
		return value, Mlist
	else:
		best_move = []
		value = -math.inf	
		for move in generateMoves(side,board,flags):
			newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
			encoded_move = encode(move[0], move[1], move[2])
			Mtree.update({encoded_move: {}})
			cur, Mlist = alphabeta_helper(newside, newboard, newflags, depth - 1, Mlist, Mtree[encoded_move], alpha, beta)
			#print(Mlist, cur, value, move)
			if cur > value:
				best_move = move
				moveList = Mlist
				value = cur
			if value >= beta:
				break
			alpha = max(alpha,value)
		#print("2 -",best_move)
		Mlist = [best_move] + moveList
		return value, Mlist

def stochastic_helper(side, board, flags, depth, Mlist, Mtree, breadth, chooser, judge):
	moveList = []
	if depth == 0:
		score = evaluate(board)
		return score, moveList
	if side:
		best_move = []	
		value = math.inf
		if judge == 0:
			for move in generateMoves(side,board,flags):
				newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
				encoded_move = encode(move[0], move[1], move[2])
				Mtree.update({encoded_move: {}})
				cur, Mlist= stochastic_helper(newside, newboard, newflags, depth - 1, Mlist, Mtree[encoded_move], breadth, chooser, 1)
			
				if cur < value:
					best_move = move
					moveList = Mlist
					value = cur
			Mlist = [best_move] + moveList
			return value, Mlist
		elif judge == 1:# random choose 1 
			tol = 0
			moves = [move for move in generateMoves(side,board,flags)]
			for i in range(breadth):
				move = chooser(moves)
				encoded_move = encode(move[0], move[1], move[2])
				Mtree.update({encoded_move: {}})
				newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
				cur, Mlist = stochastic_helper(newside, newboard, newflags, depth - 1, Mlist, Mtree[encoded_move], breadth, chooser, 2)
				tol += cur
				if cur < value:
					best_move = move
					moveList = Mlist
					value = cur
			Mlist = [best_move] + moveList
			return tol/breadth, Mlist
		else:
			moves = [move for move in generateMoves(side,board,flags)]
			move = chooser(moves)
			encoded_move = encode(move[0], move[1], move[2])
			Mtree.update({encoded_move: {}})
			newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
			cur, Mlist = stochastic_helper(newside, newboard, newflags, depth - 1, Mlist, Mtree[encoded_move], breadth, chooser, 2)
			Mlist = [move] + Mlist
			return cur, Mlist
	else:
		best_move = []
		value = -math.inf	
		if judge == 0:
			for move in generateMoves(side,board,flags):
				newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
				encoded_move = encode(move[0], move[1], move[2])
				Mtree.update({encoded_move: {}})
				cur, Mlist = stochastic_helper(newside, newboard, newflags, depth - 1, Mlist, Mtree[encoded_move],  breadth, chooser, 1)
				#print(Mlist, cur, value, move)
				if cur > value:
					best_move = move
					moveList = Mlist
					value = cur
			#print("2 -",best_move)
			Mlist = [best_move] + moveList
			return value, Mlist
		elif judge == 1:# random choose 1 
			tol = 0
			moves = [move for move in generateMoves(side,board,flags)]
			for i in range(breadth):
				move = chooser(moves)
				encoded_move = encode(move[0], move[1], move[2])
				Mtree.update({encoded_move: {}})
				newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
				cur, Mlist = stochastic_helper(newside, newboard, newflags, depth - 1, Mlist, Mtree[encoded_move], breadth, chooser, 2)
				tol += cur
				if cur > value:
					best_move = move
					moveList = Mlist
					value = cur
			Mlist = [best_move] + moveList
			return tol/breadth, Mlist
		else:
			moves = [move for move in generateMoves(side,board,flags)]
			move = chooser(moves)
			encoded_move = encode(move[0], move[1], move[2])
			Mtree.update({encoded_move: {}})
			newside, newboard, newflags = makeMove(side, board, move[0], move[1], flags, move[2])
			cur, Mlist = stochastic_helper(newside, newboard, newflags, depth - 1, Mlist, Mtree[encoded_move], breadth, chooser, 2)
			Mlist = [move] + Mlist
			return cur, Mlist


def stochastic(side, board, flags, depth, breadth, chooser):
	'''
	Choose the best move based on breadth randomly chosen paths per move, of length depth-1.
	Return: (value, moveList, moveTree)
	  value (float): average board value of the paths for the best-scoring move
	  moveLists (list): any sequence of moves, of length depth, starting with the best move
	  moveTree (dict: encode(*move)->dict): a tree of moves that were evaluated in the search process
	Input:
	  side (boolean): True if player1 (Min) plays next, otherwise False
	  board (2-tuple of lists): current board layout, used by generateMoves and makeMove
	  flags (list of flags): list of flags, used by generateMoves and makeMove
	  depth (int >=0): depth of the search (number of moves)
	  breadth: number of different paths 
	  chooser: a function similar to random.choice, but during autograding, might not be random.
	'''
	Alist = []
	Atree = {}
	a, Alist = stochastic_helper(side, board, flags, depth, Alist, Atree, breadth, chooser, 0)

	return a, Alist, Atree
