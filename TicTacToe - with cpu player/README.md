# TicTacToe - Player vs CPU

My attempts to build a fully functional Chess game with a "vs CPU" option has been met with several challenges. Most of the challenges are from my attempts to create the Chess GUI. This has encouraged me to design and implement the 'AI' on a much smaller scale game first, like TicTacToe, and I'm glad i did.
<p align="center">
  <img src="https://github.com/frederickpek/frederickcodes/blob/master/TicTacToe%20-%20with%20cpu%20player/images/03-07-20%2C14h56m42s.jpeg" />
</p>
<p align='center'><sub>Figure 1: Example game board (Pygame display).</p>

The game board has a minimalist design to it, with the cpu beginning the game with "X" and the player with "O". Left-mouse-clicks will fill the corresponding tile with your mark and will trigger the CPU to make the next move. This continues until a side has won or a tie has been reached. The algorithm used for the AI is known as the **minimax** algorithm, which i have further improved the efficiency with a searching algorithm known as **alpha-beta pruning**.

## Example Game
The the following game will starts with the CPU first.
<p align="center">
  <img src="https://github.com/frederickpek/frederickcodes/blob/master/TicTacToe%20-%20with%20cpu%20player/images/03-07-20%2C14h56m32s.jpeg" />
</p>
<p align='center'><sub>Figure 2.1: The CPU starts on the bottom right.</p>
<p align="center">
  <img src="https://github.com/frederickpek/frederickcodes/blob/master/TicTacToe%20-%20with%20cpu%20player/images/03-07-20%2C14h56m38s.jpeg" />
</p>
<p align='center'><sub>Figure 2.2: Player takes the middle tile, CPU takes the bottom-middle tile.</p>
<p align="center">
  <img src="https://github.com/frederickpek/frederickcodes/blob/master/TicTacToe%20-%20with%20cpu%20player/images/03-07-20%2C14h56m42s.jpeg" />
</p>
<p align='center'><sub>Figure 2.3: Player takes the bottom-left tile, CPU takes the top-right tile.</p>
<p align="center">
  <img src="https://github.com/frederickpek/frederickcodes/blob/master/TicTacToe%20-%20with%20cpu%20player/images/03-07-20%2C14h56m47s.jpeg" />
</p>
<p align='center'><sub>Figure 2.4: Player takes the middle-right tile, CPU takes the  middle-left tile.</p>
<p align="center">
  <img src="https://github.com/frederickpek/frederickcodes/blob/master/TicTacToe%20-%20with%20cpu%20player/images/03-07-20%2C14h56m52s.jpeg" />
</p>
<p align='center'><sub>Figure 2.5: Player takes the top-middle tile, CPU takes the  top-left tile and the game results in a tie.</p>

In the above game is almost always the case if both players play optimally. If the player does not mark the middle tile on their first turn, they it will result in their lost since the AI is playing perfectly. TicTacToe is a solved game where it is literally possible to map out all possible outcomes and determine which moves would result in a win (or often a draw) for respective players. What's interesting is the algorithm behind how our AI 'thinks' and how efficient it is in doing so. These are important concepts I would like to research more on as they will help with building my Chess engine.

## Minimax Algorithm
The minimax algorithm allows us to evaluate and score the static board states in d (depth) number of moves ahead of the current board, the scores of these boards are then passed back up the tree to the parent board where the move accordingly to reach the more favourable score. It uses the notion of the *Maximising* and *Minimising* player where the  maximising player wishes to make moves towards the more positive scoring board states and the minimising player wishes to make moves towards the less positive scoring boards. The function for evaulating static board states can be very complex and non-linear in the case of Chess, a simple example for a minimax search of depth 10 for Chess could utilise the sum of your chess pieces minus the sum of your opponents chess pieces as a hueristic to score the static board states. For TicTacToe we can simply take a winning move to be a positive value for the current player and a negative value for a losing move. We can do so because total number of games of TicTacToe is very relatively small, the same approach will hardly work for chess and hence a good static board evaluation function has to be defined.

## Alpha-Beta Pruning
Alpha-Beta Pruning is layered ontop of the minimax algorithm to optimise the search process. Before we analyse the time complexities, some terminologies need to be defined. The braching factor, *b*, is the number of board states that can be reached from the current board state in a single move. The number of static evaluations required for computing the minimax algorithm for a depth *d* will hence be a <img src="https://render.githubusercontent.com/render/math?math=b^d"> (*b* will differ based on board states). While this is relatively small for TicTacToe, Chess has a braching factor of about 20 to 30, the number of possible board states get very large very fast. Alpha-Beta Pruning comes in to cut off large sections of the search tree by stopping evaluation of move when at least one possibility has been found that proves the move to be worse than a previously examined move. In the best case, the number of static board evaluations could come down to <img src="https://render.githubusercontent.com/render/math?math=2b^\frac{d}{2}">. Below is a table which shows the number of static (end-game) boards the CPU has evaluated based on the game played in Figue 2., and the improvements with alpha-beta pruning.

| CPU's Moves| Without Alpha-Beta Pruning | With Alpha-Beta Pruning |
|:---|---:|---:|
|First|255,168|8,098|
|Second|3,468|602|
|Third|94|49|
|Fourth|6|6|
|Fifth|1|1|

<sub>Table 1: Minimax Static Board Evaluations with Alpha-Beta Pruning.

A surprising 96.8% of board states have been saved from evaluation of the first move! It is important to note that the efficiency brought by Alpha-Beta Pruning is effected by the evaluation function and order of evaluation. This, however, does not mean that a better evaluation function will result in better pruning result.
