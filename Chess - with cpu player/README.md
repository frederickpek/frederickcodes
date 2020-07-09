# Chess - Player vs CPU

It has always been a goal of mine to create my own Chess engine. While there are some flaws, restrictions and incompletions, I am still very pleased with the finished product. I had originally used Javascript as it gave simple graphical capabilities to my engine, but have since transitted to using Python's Pygame for that purpose. In this readme, I will discuss the development of my Chess engine along with some examples.


## Gameplay
The benchmark I have set for myself was to make the user experience of my Chess game synonymous to online chess platforms. Paying attention to how the mouse clicks would interact with the pieces and board.

### Sample Game
<p align="center"> <img src="https://github.com/frederickpek/frederickcodes/blob/master/Chess%20-%20with%20cpu%20player/gifs/Checkmate!.gif" width=400/> </p> 
<p align='center'> <sub>Figure 1: Checkmate by White. </p>
This example game has the cpu making random moves in order for me to make a quick Checkmate and demonstrate the additional flairs and logic i have built into the engine - the highlighting of legal moves, highlighting the most recent move, castling, checkmate recognition etc.

### Pawn Promotion Interface
<p align="center"> <img src="https://github.com/frederickpek/frederickcodes/blob/master/Chess%20-%20with%20cpu%20player/gifs/Pawn%20Promotion%20Interface.gif" width=400/> </p> 
<p align='center'> <sub>Figure 2: Pawn Promotion Interface. </p>
Again the cpu is making random moves to allow for the demonstration. I initially made all pawns automatically promote to Queens, but couldn't resist the implementation of a "drop-down"-like ui similar to most chess website. I particularly like the white transparency layer which directs the player's attention to the clickable promotion pieces while still allowing the assessment of the current board.


## Static Board Evaluation Functions
For our ai to measure which moves are potentially better, it has to be able to measure and score a board state. This is used by out *minimax* algorithm to compare against other board states given a move, to evaluate which moves will end up in more favourable scores. A crude function could be some linear combination of the pieces on board. Taking the total value of the White pieces and subtracting away from that the values of the Black pieces on board - suggesting a greater sum favouring White and a smaller sum favouring Black. For the purpose experimenting with an ai capability on my chess engine, this was good enough but i dedided to add in another metric to the evaluation - Piece Squere Tables, which essentially score the positions of pieces as well.

### Piece valuation
Most of us have heard that pawns are worth 1 point while Knights are worth 3 and Bishops 3, etc. But tt is important to study games and verify that trading a Kight for a Bishop is "worth". A more reasonable measure of peace value is the following by Tomasz Michniewski. These values are 100x larger and would be negative for black.

|Piece| Value |
|:---|---:|
|Pawn|100|
|Knight|320|
|Bishop|330|
|Rook|500|
|Queen|900|
|King|20000|

### Piece Square Tables
These tables encourage pieces to favour some positions on board over others. I found that the ai was displaying moves you could very well find in standard openings, even though it was never taught any opening libraries. 
This is an example the Knight's table for white, notice how it is rewarded by occupying the central regions of the board. Numbers are relative to the above piece values.
```
// Knight
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  0,  0,  0,-20,-40,
-30,  0, 10, 15, 15, 10,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 10, 15, 15, 10,  5,-30,
-40,-20,  0,  5,  5,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50,
```
I see it as a probability table across thousands of analysed games and game knowledge, amazingly condensed into a simple table for each piece. The values could be adjusted to force certain openings. The white king's c1 and g1 tiles could be given a much higher score to prioritise castling if the ai could see that far into moves.
At different stages of the game like the opening, where most pieces are up, and endgame, where most pieces are down, the tables could differ.


## CPU Player Implementation
### Minimax with Alpha-Beta Pruning
The minimax algorithm is one which searches all possible game states from the current one and does so recursively for those states, for a depth *d*, to evaluate the static board score and propogate this score and sequence of moves to the parent game state. Ultimiately, it is an algorithm that looks ahead *d* moves to find the best move you can take to maximise your score after *d* moves while the oppoment tries to minimise it. 

Alpha-beta pruning strives to cut out redundant searches for game states if the computation is unnecessary and could significantly improve the efficiency of minimax. Before we analyse the time complexities, some terminologies need to be defined. The braching factor, *b*, is the number of board states that can be reached from the current board state in a single move. The number of static evaluations required for computing the minimax algorithm for a depth *d* will hence be a <img src="https://render.githubusercontent.com/render/math?math=b^d"> (*b* will differ based on board states). Chess has a braching factor of about 20 to 40, the number of possible board states get very large very fast. Alpha-beta pruning comes in to cut off large sections of the search tree by stopping evaluation of move when at least one possibility has been found that proves the move to be worse than a previously examined move. In the best case, the number of static board evaluations could come down to <img src="https://render.githubusercontent.com/render/math?math=2b^\frac{d}{2}">. This implies we could search twice as deep with no change in out conputation time!

### Unique Interactions at Different Depth of Search
Let me first clarify that a depth of *d* does not indicate searching ahead 2 of your own moves, but is shared between 2 players. So with a depth of 3, we would first analyse the the current player's own move, then the for each of those, the next players turn, then similarly back to the currently player. 

|Depth of Search| Description |
|:---|:---|
|0|Looking 0 moves ahead, the cpu simply makes any random move.|
|1|The cpu will capture the piece with the highest value or move its piece to the highest scoring tile, whichever results in a better score. ie not considering blunders.|
|2|The cpu can now analyse the players response to his, and will not allow its piece to be captured - unless it results in the capturing piece to be in in a bad position, like the king.|
|3|Again since this is an odd number, the likelyhood of a blunder is high as the cpu will capture recklessly.|

This odd-depth blunder by the cpu can be improved by *quiescence search* which extends the search depth for captures.  

### Improvements
I had employed the minimax algorithm before, on a TicTacToe game, but Chess is on a whole 'nother level. The board is much larger with pieces entities, game state variables (castled? piece's first-move? checkmated? stalemate?) and now there is move legality which we have to account for after each move. My approach to generating child board states is not be the best and actually takes significantly longer than evaluating the static board score, rendering the alpha-beta pruning redundant. One approach could be to move and undo a move to traverse the minimax search tree, allowing pruning of game states before generating them.

## Restrictions and Incompletions
1. Player is always White
2. There is no Player vs Player mode
3. En Passant has not been implemented
4. Black ai's pawn promotion will always be Queen
5. Minimax searching will always promote a pawn to a Queen for White player
