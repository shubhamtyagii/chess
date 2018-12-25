import os
import chess.pgn
import numpy as np
from state import State
def get_dataset(data_size=None):
    gn=0
    X=[]
    Y=[]
    for fn in os.listdir('data'):
        pgn=open(os.path.join('data',fn))

        while 1:

            try:
                game=chess.pgn.read_game(pgn)
            except Exception:
                break
            gn+=1
            
            value={'1/2-1/2':0,'1-0':1,'0-1':-1}[game.headers['Result']]
            board=game.board()
            for i, move in enumerate(game.mainline_moves()):

                board.push(move)
                ser=State(board).serialize()
                X.append(ser)
                Y.append(value)
            print('parsing game no : ',gn,' got examples', len(X))
            if data_size is not None and len(X)>data_size:
                return X,Y
    return X,Y
if __name__=='__main__':
    get_dataset(1000)