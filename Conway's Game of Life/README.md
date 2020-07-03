# Game of Life by John Horton Conway
Game of Life is a cellular automaton - a grid of cells with state properties, and rules to govern what the states of the next generation cells should be.

In the Game of Life, cells are either alive or dead. They are initially populated over the grid and the rules to create each generation are as follows.

1. If a live cell has 2 or 3 neighbours, it survives to the next generation. Else it dies of "loneliness/overpopulation".

2. If a dead cell has exactly 3 neighbours, it comes to live in the next generation. Else it remains dead. A cell's neighbours are the 8 adjacent cells, excluding itself

The simulation seemingly depicts a life-like growth and decay, almost like bacteria in a petri dish. Probably due to the fact that the rules in the Game of Life were chosen to mimic life, such as an overcrowding situation and a birth mechanism.

Many configurations exists in the Game of Life, some cell patterns are cyclic, some are still and never changing. The latter is often what is left after a simulation runs for some time, a stable state of sorts. Some are known as "gliders" and are configurations that crawl across the grid forever (or until it meets a wall...). A more notable configuration would be known as the Gosper Glider Gun. Originally conjectured by Conway that no configuration of cells could grow indefinitely, it was shown otherwise by Bill Gosper. The Gosper Glider Gun has a cycle of 120 generations which create gliders indefinitely.

If you're interested, here is Conway himself speaking about his invention. https://www.youtube.com/watch?v=R9Plq-D1gEk&t=330s
