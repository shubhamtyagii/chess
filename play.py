import torch
import time
from state import State
from train import Net
import chess
import chess.svg
import traceback
import base64
import os
from flask import Flask,Response,request



MAXVAL=10000
class Valuator(object):
	def __init__(self):
		self.model=Net()
		vals=torch.load('./nets/value.pth', map_location=lambda storage, location: storage)
		self.model.load_state_dict(vals)
	
	def __call__(self,s):
		brd=s.serialize()[None]
		output=self.model(torch.tensor(brd).float())
		return float(output.data[0][0])

		
def computer_minimax(s,v,depth,a,b,big=False):
	if( depth>=5 or s.board.is_game_over()):
		return v(s)
	turn=s.board.turn
	if turn==chess.WHITE:
		ret=-MAXVAL
	else:
		ret=MAXVAL
	if big:
		bret=[]
	isort=[]
	for e in s.board.legal_moves:
		s.board.push(e)
		isort.append((v(s),e))
		s.board.pop()
	move=sorted(isort,key=lambda x:x[0],reverse=s.board.turn)
	# beam search beyond depth 3
	if depth>=2:
		move=move[:5]
	for e in [x[1] for x in move]:
		s.board.push(e)
		tval=computer_minimax(s,v,depth+1,a,b)
		if big:
			bret.append((tval,e))
		s.board.pop()
		if(turn==chess.WHITE):
	
			ret= max(ret,tval)
			a=max(a,ret)
			if a>=b:
				break
			
		else:
			ret=min(ret,tval)
			b=min(ret,b)
			if a>=b:
				break
	
		
	if big:
		return ret,bret
	else:
		return ret
class DeepValuator(object):
	
	values={chess.PAWN:1,
			chess.KNIGHT:3,
			chess.BISHOP:3,
			chess.ROOK:5,
			chess.QUEEN:9,
			chess.KING:0}
	def __init__(self):
		self.reset()
		self.memo={}
	
	def reset(self):
		self.count=0
		
	#simple value func based on pieces
	#ideas: https://en.wikipedia.org/wiki/Evaluation_functions
	
	def __call__(self,s):
		key=s.key()	
		self.count+=1
		
		if key not in self.memo:
			
			self.memo[key]=self.value(s)
		return self.memo[key]
			
	def value(self,s):
		b=s.board
		if b.is_game_over():
			if b.result()=='1-0':
				return MAXVAL
			elif b.result()=='0-1':
				return -MAXVAL
			else:
				return 0
				
		val=0.0
		piece_map=b.piece_map()
		for i in piece_map:
			temp_val=self.values[piece_map[i].piece_type]
			if piece_map[i].color==chess.WHITE:
				val+=temp_val
			else:
				val-=temp_val
		#add a number of legal moves term
		bak=b.turn
		b.turn=chess.WHITE
		val+=0.1*b.legal_moves.count()
		b.turn=chess.BLACK
		val-=0.1*b.legal_moves.count()
		
		b.turn=bak
		
		return val
		
	
def explore_leaves(s,v):
	ret=[]
	v.reset()
	cval,ret=computer_minimax(s,v,depth=0,a=-MAXVAL,b=MAXVAL,big=True)
	print('explored nodes=',v.count)
	return ret
#board and engine
s=State()
v=DeepValuator()

def computer_move(s,v):
	#deep=DeepEvaluator()
	move=sorted(explore_leaves(s,v),key=lambda x:x[0],reverse=s.board.turn)
	if len(move)==0:
		return 
	#print(move)
	#move=deep(s,v)
	#s.board.push(move[1])
	for i in range(min(3,len(move))):
		print(move[i])
	s.board.push(move[0][1])
	
	


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
	SELFPLAY=False
	if SELFPLAY:
		s=State()
		while not s.board.is_game_over():
			
			computer_move(s,v)
			print(s.board)
	else: 
		app.run(debug=True)

	
	

	
	
#if __name__=="__main__":
#	s=State()
#	v=Valuator()
	
#	while not s.board.is_game_over():
		
#		move=sorted(explore_leaves(s,v),key=lambda x:x[0],reverse=s.board.turn)[0]
#		s.board.push(move[1])
#		print(s.board)
#	print(s.board.result())
		
		