# Marching Squares Algorithm & Terrain Generation with OpenSimplex Noise

The marching squares algorithm generates contours for a 2-dimensional space. This project has 2 parts to it, first the terrain generation and the implementation of the marching squares algorithm.

<p align="center"> <img src="https://github.com/frederickpek/frederickcodes/blob/master/Marching%20Squares%20Algorithm/gifs/MSA.gif" width=1000/> </p> 
<p align='center'> <sub>Figure 1: Terrain generation with Python's OpenSimplex noise with contours drawn with the marching squares algorithm. </p>

The terrain generated is random and continous and the contours drawn matches the profile of the edges of those terrain. I will further elaborate on the process towards this result below.

### Terrain Generation
First i needed a random terrain, I simply populated a 2d array grid with random 1s and 0s. With 1s representing that plot of grid being terrains and the opposite is true for 0s. A 24x14 square grid of points will be used from here on out to represent the grid. Note that this will result in 25x15 points representing the corners of the square tile. 

<p align="center"> <img src="https://github.com/frederickpek/frederickcodes/blob/master/Marching%20Squares%20Algorithm/images/19-07-20%2C02h06m32s.jpeg" width=1000/> </p> 
<p align='center'> <sub>Figure 2: Random Terrain Generation. </p>

### Marching Squares Algorithm
Now that we have our terrain, we can implement the marching squares algorithm to generate the contours. A big part of why the algorithm is called the marching squares algorithm is due to how the algorithm generates the contour. It looks up each square tile of grid and decides how the contour line, if any, will be drawn within the grid by means of a simple look up table. After implementing the algorithm, we will have the following static plot shown in Figure 4.

<p align="center"> <img src="https://github.com/frederickpek/frederickcodes/blob/master/Marching%20Squares%20Algorithm/images/Lookup%20Table.jpg" width=400/> </p> 
<p align='center'> <sub>Figure 3: Marching Squares Algorithm Lookup Table. </p>


<p align="center"> <img src="https://github.com/frederickpek/frederickcodes/blob/master/Marching%20Squares%20Algorithm/images/19-07-20%2C02h07m11s.jpeg" width=1000/> </p> 
<p align='center'> <sub>Figure 4: Random Terrain with MSA contours. </p>

### Morphing Terrain
The idea of this would be to simulate the slicing of a terrain's cross section over time. My initial try was to just fill the 2d grid with newly generated random values at regular time intervals.

<p align="center"> <img src="https://github.com/frederickpek/frederickcodes/blob/master/Marching%20Squares%20Algorithm/gifs/MSA_Random_Non-Interpolation.gif" width=1000/> </p> 
<p align='center'> <sub>Figure 5: Random Terrain with MSA contours, non-static. </p>

The results were not satisfying, the terrain is not changing in a continous manner. Although we want random terrain, this was definitely not the way to achieve the intended effect. I had to look for alternative noise generation algorithms for a more continous and smooth profile across 3 dimensions. 2 dimensions for the terrain generations and a third to allow for the continous 2d slices to be viewed over time.

### OpenSimplex Noise
Simplex noise is a method for constructing an n-dimensional noise function. It is able to generate random yet gradient-like values ranging from -1 to 1 in n-dimensions for us to create the terrain with. However, Simplex noise by Ken Perlin is patented and not a free software. OpenSimplex is just the open and freely usable version. After giving each point a random value of -1 to 1, the resulting plot overtime is already many times better. I marked all values < 0 as 0, and gave the points a brightness corresponding to its magnitude.

<p align="center"> <img src="https://github.com/frederickpek/frederickcodes/blob/master/Marching%20Squares%20Algorithm/gifs/MSA_SimplexNoise_Non-Interpolation.gif" width=1000/> </p> 
<p align='center'> <sub>Figure 6: OpenSimplex Noise Terrain with MSA contours, non-static. </p>

### Linear Interpolation of Contour Lines
Since now the values in the square tile's corners are no longer just 1s and 0s, the contour line differentiating terrain and non terrain should no longer reside in the exact middle of the points. We should shift the lines closer to smaller values and shift it away from larger values to indicate less and more space and terrain present. This effect will surprisingly smooth out our contour lines and give the plot a much needed aesthetic lift.

<p align="center"> <img src="https://github.com/frederickpek/frederickcodes/blob/master/Marching%20Squares%20Algorithm/gifs/MSA_SimplexNoise_Interpolation.gif" width=1000/> </p> 
<p align='center'> <sub>Figure 7: OpenSimplex Noise Terrain with Interpolated MSA contours, non-static. </p>

This is already the finished product as seen in Figure 1, except with a much highly spaced grid, gridlines and point values displayed.



