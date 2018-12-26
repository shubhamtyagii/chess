import os
import chess.pgn
import numpy as np
from state import State
def get_dataset(data_size=None):
	gn=0
	X=[]
	Y=[]
	values={'1/2-1/2':0,'1-0':1,'0-1':-1}
	for fn in os.listdir('./../data'):
		pgn=open(os.path.join('./../data',fn))
	
		while 1:
	
			try:
				game=chess.pgn.read_game(pgn)
			except Exception:
				break
			gn+=1
			if game is None:
				break
			
			res=game.headers['Result']
			if res not in values:
				continue
			value=values[res]
			board=game.board()
			for i, move in enumerate(game.mainline_moves()):
	
				board.push(move)
				ser=State(board).serialize()
				X.append(ser)
				Y.append(value)
			print('parsing game no : ',gn,' got examples', len(X))
			if data_size is not None and len(X)>data_size:
				X=np.array(X)
				Y=np.array(Y)
				return X,Y
	X = np.array(X)
	Y = np.array(Y)
	return X,Y
if __name__=='__main__':
    X,Y=get_dataset(1000000)
    np.savez('./processed/dataset_1M.npz',X,Y)