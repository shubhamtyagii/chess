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
		vals=torch.load('./nets/value.pth')
		self.model.load_state_dict(vals)
	
	def __call__(self,s):
		brd=s.serialize()[None]
		output=self.model(torch.tensor(brd).float())
		return float(output.data[0][0])
		
		
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
	move=sorted(explore_leaves(s,v),key=lambda x:x[0],reverse=s.board.turn)[0]
	print(move)
	s.board.push(move[1])
	


def to_svg(s):
	return base64.b64encode(chess.svg.board(board=s.board).encode('utf-8')).decode('utf-8')
app=Flask(__name__)
@app.route('/')
def hello():
	board_svg=to_svg(s)
	
	ret='<html>'
	ret+='<head><script src="https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.3.1.min.js"></script></head>'
	ret+='<body><a href="/self">play vs itself</a></br>'
	ret+='<img height="500" width="500" src="data:image/svg+xml;base64,%s"?/></img>'% board_svg
	ret+='<form action="/move"><input type="text" name="human_move"></input><input type="submit" value="MOVE"/></from>'
	
	#ret+='<button onclick=\'$.post("/move"); location.reload();\'>MOVE</button>
	ret+='</body></html>'
	return ret
	
	

	
@app.route('/move')
def move():
	if not s.board.is_game_over():
		move=request.args.get('human_move',default='')
		print('human moves ',move)
		if move is not None and move!='':
			try:
				s.board.push_san(move)
				computer_move(s,v)
			except Exception:
				traceback.print_exc()
	else:
		print('game is over')
	return hello()
	
@app.route('/self')	
def self_play():
	s=State()
	
	ret='<html>'
	while not s.board.is_game_over():
		computer_move(s,v)
		board_svg=to_svg(s)
		
		ret+='<body><img height="500" width="500" src="data:image/svg+xml;base64,%s"?/></img>'% board_svg
	print(s.board.result())
	return ret
	
	
	
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
		
		