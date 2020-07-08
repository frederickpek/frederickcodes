# Chess - Player vs CPU

It has always been a goal of mine to create my own Chess engine. While there are some flaws, restrictions and incompletions, I am still very proud of the finished product. In this readme, I will discuss the development of my Chess engine along with some examples.



<p align="center"> <img src="https://github.com/frederickpek/frederickcodes/blob/master/Chess%20-%20with%20cpu%20player/gifs/Checkmate!.gif" width=400/> </p> 
<p align='center'> <sub>Figure 1: Checkmate by White. </p>
This example game has the cpu making random moves in order for me to make a quick Checkmate and demonstrate the additional flairs and logic i have built into my engine - the highlighting of legal moves, castling, checkmate recognition etc.

### Pawn Promotion Interface
<p align="center"> <img src="https://github.com/frederickpek/frederickcodes/blob/master/Chess%20-%20with%20cpu%20player/gifs/Pawn%20Promotion%20Interface.gif" width=400/> </p> 
<p align='center'> <sub>Figure 2: Pawn Promotion Interface. </p>
Again the cpu is making random moves to allow for the demonstration. I initially made all pawn automatically promote to Queens, but couldn't resist the implementation of a "drop-down"-like ui similar to most chess website. I particularly liked the white alpha layer which really adds to the interface.

### Restrictions and Incompletions 
1. Player is always White
2. There is no Player vs Player mode
3. En Passant has not been implemented
