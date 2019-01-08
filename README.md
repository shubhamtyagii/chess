
# Chess Engine:
Tried to build chess engine using a neural network and some traditional value functions for state evaluation.

## Board Representation:
To represent the board state I have use a 8x8x5 bit map. 8x8 for each cell and 5 bits to represent the state of each cell.
   ### Pieces:
        1. King
        2. Queen
        3. Bishop
        4. Knight
        5. Rook
        6. Pawn
        
   ### Special Moves:
       1. En Passon
       2. Castling
       
   
## Value Function:
I have used a Convolutional Neural Network, alpha beta pruning and beam search to build my value function.

### Neural Network:
I have used a convolutional NN. Networks takes the current chess board state as input and returns a real value between [-1,+1] here </br>
    1. -1= black wins
    2. +1= white wins
    3. 0=draw

### alpha-beta pruning:
To prune the search tree I have used alpha-beta minimax, It is used to eliminate the tree branches from where we know we won't get best results.

### Beam Search:
To further reduce the computation, I have used the beam search using which I only traverse top 'N' branches.

### Give weight to each piece:
I have given weights to each category of pieces. Hence after simulating each possible move I also adds up the sum of pieces available on the board. If its white's turn then idea is, simulate the possible move and check the available pieces of both sides and return the *weighted sum of available white pieces - weighted sum of available black pieces* and vice versa.

## Libraries used:
    1. python-chess
    2. pytorch
    3. Numpy
    4. Flask
    
## How to use:
1. clone the repository
2. Install all the required Libraries
3. use the following command ```python play.py```
4. Paste the follwing URL in your browser:
   http://localhost:5000/

## Output:
![Output Image not found](README_images/output.JPG?raw=true "Output")
