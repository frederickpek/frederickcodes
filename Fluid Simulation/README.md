# Fluid Simulation by Mike Ash

As a mechanical engineer, I did take a few fluid dynamics modules. I have since been interested in trying to simulate fluids in a closed system, turns out, trying to simulate fluids is pretty difficult if you don't know what you're doing! I came across Mike Ash's open source code in C for fluid simulation in 3d and contructed a 2d version on Python instead. You can take a look at his article, [Fluid Simulation for Dummies](https://mikeash.com/pyblog/fluid-simulation-for-dummies.html). I have almost no clue regarding the specifics behind the math and physics involved but here are some renders of the end result.

<p align="center"> <img src="https://github.com/frederickpek/frederickcodes/blob/master/Fluid%20Simulation/gifs/gif3.gif" width=400/> </p> 
<p align='center'> <sub>Figure 1: Random dyes shooting out from the middle of the screen. </p>

<p align="center"> <img src="https://github.com/frederickpek/frederickcodes/blob/master/Fluid%20Simulation/gifs/gif2.gif" width=400/> </p> 
<p align='center'> <sub>Figure 2 </p>

<p align="center"> <img src="https://github.com/frederickpek/frederickcodes/blob/master/Fluid%20Simulation/gifs/gif4.gif" width=400/> </p> 
<p align='center'> <sub>Figure 3 </p>

<p align="center"> <img src="https://github.com/frederickpek/frederickcodes/blob/master/Fluid%20Simulation/gifs/gif5.gif" width=400/> </p> 
<p align='center'> <sub>Figure 4 </p>

<p align="center"> <img src="https://github.com/frederickpek/frederickcodes/blob/master/Fluid%20Simulation/gifs/gif1.gif" width=400/> </p> 
<p align='center'> <sub>Figure 5: Bright. </p>

The renders picture a dye being dropped and shot out at a certain velocity from the middle of the screen. OpenSimplex noise was used to determine the directional qualities.
