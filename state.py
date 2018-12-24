import chess

    

class State(object):
    def __init__(self,board=None):
        if board is None:
            self.board=chess.Board
        else:
            self.board=board
        
    def serialize(self):
        assert self.board.is_valid()
        state=np.zeros((8,8,5))
        
        bstate=np.zeros((64))
        for r in range(8):
            for c in range(8):
                state[r,c,0:4]=bstate[r*8+c]
        #4th col is for whose turn it is
        
        state[:,:,4]=self.board.turn*1.0
        
        pp=self.board.shredder_fen()
        return pp
    
    def value(self):
        #TODO add neural network here
        return 1
    def edges(self):
        return list(self.state.legal_moves)