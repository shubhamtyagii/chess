import torch
import time
from state import State
from train import Net
import chess
import chess.svg
import traceback
import base64
from flask import Flask,Response,request

class Valuator(object):
	def __init__(self):
		self.model=Net()
		vals=torch.load('./nets/value.pth', map_location=lambda storage, location: storage)
		self.model.load_state_dict(vals)
	
	def __call__(self,s):
		brd=s.serialize()[None]
		output=self.model(torch.tensor(brd).float())
		return float(output.data[0][0])
		
class DeepEvaluator(object):
	def __init__(self,depth=3):
		self.depth=depth
		
		
	
	def __call__(self,board_state,v):
		moves_scores=[]
		for move in board_state.board.legal_moves:
			board_state.board.push(move)
			res=v(board_state)
			res+=self.minimax(board_state,False,1,v)
			moves_scores.append([move,res])
			board_state.board.pop()
		moves_scores=sorted(moves_scores,key=lambda x:x[1],reverse=board_state.board.turn)
		print(moves_scores)
		return moves_scores[0][0]
			
			
			
	def minimax(self, board_state,maximize,depth,v):
		if(depth==self.depth or board_state.board.is_game_over()):
			val=v(board_state)
			#print(val)
			return val
		print(board_state.board)
		if maximize:
			value=-200000
			for move in board_state.board.legal_moves:
				
				board_state.board.push(move)
				temp=v(board_state)
				value=max(value,temp+self.minimax(board_state,False,depth+1,v))
				board_state.board.pop()
				#print(board_state.board)
				#exit(0)
				return value
		else:
			value=200000
			for move in board_state.board.legal_moves:
				board_state.board.push(move)
				temp=v(board_state)
				value=min(value,temp+self.minimax(board_state,True,depth+1,v))
				board_state.board.pop()	
				return value
		
	
def explore_leaves(s,v):
	ret=[]
	for e in s.edges():
		s.board.push(e)
		ret.append((v(s),e))
		s.board.pop()
	return ret
#board and engine
s=State()
v=Valuator()

def computer_move(s,v):
	deep=DeepEvaluator()
	#move=sorted(explore_leaves(s,v),key=lambda x:x[0],reverse=s.board.turn)[0]
	#print(move)
	move=deep(s,v)
	#s.board.push(move[1])
	s.board.push(move)
	


def to_svg(s):
	return base64.b64encode(chess.svg.board(board=s.board).encode('utf-8')).decode('utf-8')
app=Flask(__name__)


@app.route("/")
def hello():
  ret = open("index.html").read()
  return ret.replace('start', s.board.fen())
	
	

	
@app.route("/move")
def move():
  if not s.board.is_game_over():
    move = request.args.get('move',default="")
    if move is not None and move != "":
      print("human moves", move)
      try:
        s.board.push_san(move)
        computer_move(s, v)
      except Exception:
        traceback.print_exc()
      response = app.response_class(
        response=s.board.fen(),
        status=200
      )
      return response
  else:
    print("GAME IS OVER")
    response = app.response_class(
      response="game over",
      status=200
    )
    return response
  print("hello ran")
  return hello()
  
  
@app.route("/newgame")
def newgame():
  s.board.reset()
  response = app.response_class(
    response=s.board.fen(),
    status=200
  )
  return response
		
@app.route('/selfplay')
def self_play():
	s=State()
	
	ret='<html>'
	while not s.board.is_game_over():
		computer_move(s,v)
		board_svg=to_svg(s)
		
		ret+='<body><img height="500" width="500" src="data:image/svg+xml;base64,%s"?/></img>'% board_svg
	print(s.board.result())
	return ret
	
	
@app.route("/move_coordinates")
def move_coordinates():
  if not s.board.is_game_over():
    source = int(request.args.get('from', default=''))
    target = int(request.args.get('to', default=''))
    promotion = True if request.args.get('promotion', default='') == 'true' else False

    move = s.board.san(chess.Move(source, target, promotion=chess.QUEEN if promotion else None))

    if move is not None and move != "":
      print("human moves", move)
      try:
        s.board.push_san(move)
        computer_move(s, v)
      except Exception:
        traceback.print_exc()
    response = app.response_class(
      response=s.board.fen(),
      status=200
    )
    return response

  print("GAME IS OVER")
  response = app.response_class(
    response="game over",
    status=200
  )
  return response
	
if __name__=="__main__":
	app.run(debug=True)

	
	

	
	
#if __name__=="__main__":
#	s=State()
#	v=Valuator()
	
#	while not s.board.is_game_over():
		
#		move=sorted(explore_leaves(s,v),key=lambda x:x[0],reverse=s.board.turn)[0]
#		s.board.push(move[1])
#		print(s.board)
#	print(s.board.result())
		
		