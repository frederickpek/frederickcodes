let magnitude = 10;
let numCol;
let numRow;
let grid = [];
let numGenerations = 1;
let pGenerations;
let pause = true;

function setup() {
	createCanvas(900, 500);
	frameRate(10);
	createP('Initial population: 10%');
	pGenerations = createP('Generation: ' + numGenerations);
	numCol = width / magnitude;
	numRow = height / magnitude;
	for (let i = 0; i < numRow; i++) {
	  	for (let j = 0; j < numCol; j++) {
			grid.push(new Cell(j, i));
	  	}
	}
	populate(0.12);
	// grid = createGospelGliderGun(8,5);
}

function draw() {
  background(255);
  pGenerations.html('Generation: ' + numGenerations);
  for (cell of grid) {
	  cell.display();
  }
  let nextGeneration = [];
  for (cell of grid) {
  	let newCell = new Cell(cell.x, cell.y)
  	newCell.alive = cell.isAliveNextGeneration()
  	nextGeneration.push(newCell);
  }
  if (pause) { 
    // Yes
  } else {
  	grid = nextGeneration;
  	numGenerations++;
  }
}

function index(x, y) {
  	if (x < 0 || y < 0 || x > numCol - 1 || y > numRow - 1) {
		return -1;
  	}
  	return x + y * numCol;
}

function populate(percentage) {
  	for (let i = 0; i < numCol; i++) {
  		for (let j = 0; j < numRow; j++) {
  			if (random(1) < percentage) {
  				grid[index(i, j)].alive = true;
  			} else {
  				grid[index(i, j)].alive = false;
  			}
  		}
  	}
}

function createGospelGliderGun(x, y) {
	let newGrid = []
	for (let i = 0; i < numRow; i++) {
    	for (let j = 0; j < numCol; j++) {
    		newGrid.push(new Cell(j, i));
    	}
    }

  newGrid[index(x + 25, y + 1)].alive = true;
  newGrid[index(x + 23, y + 2)].alive = true;
  newGrid[index(x + 25, y + 2)].alive = true;
  newGrid[index(x + 13, y + 3)].alive = true;
  newGrid[index(x + 14, y + 3)].alive = true;
  newGrid[index(x + 21, y + 3)].alive = true;
  newGrid[index(x + 22, y + 3)].alive = true;
  newGrid[index(x + 35, y + 3)].alive = true;
  newGrid[index(x + 36, y + 3)].alive = true;
  newGrid[index(x + 12, y + 4)].alive = true;
  newGrid[index(x + 16, y + 4)].alive = true;
  newGrid[index(x + 21, y + 4)].alive = true;
  newGrid[index(x + 22, y + 4)].alive = true;
  newGrid[index(x + 35, y + 4)].alive = true;
  newGrid[index(x + 36, y + 4)].alive = true;
  newGrid[index(x +  1, y + 5)].alive = true;
  newGrid[index(x +  2, y + 5)].alive = true;
  newGrid[index(x + 11, y + 5)].alive = true;
  newGrid[index(x + 17, y + 5)].alive = true;
  newGrid[index(x + 21, y + 5)].alive = true;
  newGrid[index(x + 22, y + 5)].alive = true;
  newGrid[index(x +  1, y + 6)].alive = true;
  newGrid[index(x +  2, y + 6)].alive = true;
  newGrid[index(x + 11, y + 6)].alive = true;
  newGrid[index(x + 15, y + 6)].alive = true;
  newGrid[index(x + 17, y + 6)].alive = true;
  newGrid[index(x + 18, y + 6)].alive = true;
  newGrid[index(x + 23, y + 6)].alive = true;
  newGrid[index(x + 25, y + 6)].alive = true;
  newGrid[index(x + 11, y + 7)].alive = true;
  newGrid[index(x + 17, y + 7)].alive = true;
  newGrid[index(x + 25, y + 7)].alive = true;
  newGrid[index(x + 12, y + 8)].alive = true;
  newGrid[index(x + 16, y + 8)].alive = true;
  newGrid[index(x + 13, y + 9)].alive = true;
  newGrid[index(x + 14, y + 9)].alive = true;

  return newGrid;
}

function keyPressed() {
	if (key == ' ') {
		pause = !pause;
	}
}

class Cell {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.alive = false;
  }

  numLiveNeighbours() {
    let count = 0;
    for (let i = -1; i < 2; i++) {
      for (let j = -1; j < 2; j++) {
        if (!(i == 0 && j == 0)) {
          if (grid[index(this.x + i, this.y + j)]) {
            if (grid[index(this.x + i, this.y + j)].alive) {
              count++;
            }
          }
        }
      }
    }
    return count;
  }

  isAliveNextGeneration() {
    let n = this.numLiveNeighbours();
    if (this.alive) {
      return (n >= 2) && (n <= 3);
    } else {
      return (n == 3);
    }
  }

  display() {
    let X = this.x * magnitude;
    let Y = this.y * magnitude;
    strokeWeight(0.11);
    stroke(0);
    if (this.alive) {
      fill(255, 125, 0, 150);
      rect(X, Y, magnitude, magnitude);
    }
    else {
      noFill();
      rect(X, Y, magnitude, magnitude);
    }
  }
}
