'''
KLOTSKI puzzle game
The minimum number of moves for the original puzzle is 81,
if you consider sliding a single piece to any reachable position to be a single move.

This program searches for the mimimum number of moves to solve Klotski.
Searching in a breadth first search manner.
Ensures our solution requires the least number of moves.

Then replays the sequence of moves that resulted in the solution. 
'''

from threading import Thread
import os
import time

class State:
	hashed_states = {}

	def __init__(self, grid, blocks):
		self.grid = grid
		self.blocks = blocks

	def initialise():
		initial_grid = [[None for _ in range(4)] for _ in range(5)]

		# this input should require 81 moves to solve the puzzle
		initial_blocks = [Block(initial_grid, [(0, 1), (0, 2), (1, 1), (1, 2)], " R ", "R"),
					  	  Block(initial_grid, [(0, 0), (1, 0)], " @ ", "@"),
					  	  Block(initial_grid, [(2, 0), (3, 0)], " # ", "@"),
					  	  Block(initial_grid, [(0, 3), (1, 3)], " * ", "@"),
					  	  Block(initial_grid, [(2, 3), (3, 3)], " $ ", "@"),
					  	  Block(initial_grid, [(2, 1), (2, 2)], " P ", "P"),
					  	  Block(initial_grid, [(3, 1)], " o ", "G"),
					  	  Block(initial_grid, [(3, 2)], " o ", "G"),
					  	  Block(initial_grid, [(4, 0)], " o ", "G"),
					  	  Block(initial_grid, [(4, 3)], " o ", "G"),
					  	  Block(initial_grid, [(4, 1)], "   ", "g",True),
					  	  Block(initial_grid, [(4, 2)], "   ", "g",True)]

		return State(initial_grid, initial_blocks)

	def copy(self):
		new_grid = [[None for _ in range(4)] for _ in range(5)]

		new_blocks = []

		for b in self.blocks:
			new_coor = []
			for c in b.coordinates:
				new_coor.append((c[0], c[1]))
			new_blocks.append(Block(new_grid, new_coor, b.colour, b.hash_val, b.is_ghost_block()))

		return State(new_grid, new_blocks)

	def move(self, block_index, vector):
		g1 = self.blocks[len(self.blocks) - 1].coordinates[0]
		g2 = self.blocks[len(self.blocks) - 2].coordinates[0]
		all_possible_ghost_blocks_coor = [(g1[0], g1[1]),(g2[0], g2[1])] 

		block = self.blocks[block_index]

		for c in block.coordinates:
			all_possible_ghost_blocks_coor.append((c[0], c[1]))

		all_not_possible_ghost_blocks_coor = []

		for i in range(len(block.coordinates)):
			curr = block.coordinates[i]
			new_c = (curr[0] + vector[0], curr[1] + vector[1])
			block.coordinates[i] = new_c
			all_not_possible_ghost_blocks_coor.append(new_c)
		
		new_ghost_block_coor = []

		for apc in all_possible_ghost_blocks_coor:
			match = False
			for anpc in all_not_possible_ghost_blocks_coor:
				if (apc[0] == anpc[0] and apc[1] == anpc[1]):
					match = True
			if (not match):
				new_ghost_block_coor.append(apc)

		for i in range(len(new_ghost_block_coor)):
			ghost_block = self.blocks[len(self.blocks) - 2 + i]
			ghost_block.coordinates = [new_ghost_block_coor[i]]
			ghost_block.update_grid()

		block.update_grid()

	def is_solved(self):
		red_block = self.blocks[0]
		return self.grid[3][1] == red_block and self.grid[4][2] == red_block

	def __str__(self):
		output = ""
		for row in self.grid:
			output += "["
			spacer = ""
			for block in row:
				output += spacer + str(block)
				spacer = " "
			output += "]\n"
		return output

	def hash(self):
		key = ""
		for row in self.grid:
			for block in row:
				key += str(block.hash_val)
		return key

class Block:
	def __init__(self, grid, coordinates, colour, hash_val, is_ghost_block = False):
		self.grid = grid
		self.coordinates = coordinates 
		self.colour = colour
		self.hash_val = hash_val
		self.__is_ghost_block = is_ghost_block
		self.update_grid()

	def can_move(self, vector):
		if (self.is_ghost_block()):
			return False

		for coor in self.coordinates:
			r, c = vector[0] + coor[0], vector[1] + coor[1]
			if (r > -1 and r < len(self.grid) and c > -1 and c < len(self.grid[0])):
				if (not (self.grid[r][c].is_ghost_block() or self.grid[r][c] == self)):
					return False
			else:
				return False

		return True

	def update_grid(self):
		for coor in self.coordinates:
			self.grid[coor[0]][coor[1]] = self

	def is_ghost_block(self):
		return self.__is_ghost_block

	def __str__(self):
		return str(self.colour)


def KlotskiSolver(core_index, states):
	global directions
	global is_solved
	global moves
	global next_gen_states
	global solution_state

	# print("Core: " + str(core_index) + "  States: " + str(len(states)))
	
	for state in states:
		for block_index in range(len(state.blocks)):
			for vector in directions:
				# first step
				if (state.blocks[block_index].can_move(vector)):
					curr_state = state.copy()
					curr_state.move(block_index, vector)
					if (curr_state.hash() not in State.hashed_states.keys()):
						State.hashed_states[curr_state.hash()] = (str(state), state.hash())
						next_gen_states.append(curr_state)
					if (curr_state.is_solved()):
						is_solved = True
						solution_state = curr_state

					prev_state = curr_state

					# second step
					if (prev_state.blocks[block_index].can_move(vector)):
						curr_state = prev_state.copy()
						curr_state.move(block_index, vector)
						if (curr_state.hash() not in State.hashed_states.keys()):
							State.hashed_states[curr_state.hash()] = (str(state), state.hash())
							next_gen_states.append(curr_state)

					# THRID flippin step if is a singular block
					elif (len(prev_state.blocks[block_index].coordinates) == 1):
						shift = abs(vector[0]) * 2
						if (prev_state.blocks[block_index].can_move(directions[shift])):
							curr_state = prev_state.copy()
							curr_state.move(block_index, directions[shift])
							if (curr_state.hash() not in State.hashed_states.keys()):
								State.hashed_states[curr_state.hash()] = (str(state), state.hash())
								next_gen_states.append(curr_state)
						elif (prev_state.blocks[block_index].can_move(directions[shift + 1])):
							curr_state = prev_state.copy()
							curr_state.move(block_index, directions[shift + 1])
							if (curr_state.hash() not in State.hashed_states.keys()):
								State.hashed_states[curr_state.hash()] = (str(state), state.hash())
								next_gen_states.append(curr_state)

def segment(list):
	cores = os.cpu_count()

	segments = []

	for _ in range(cores):
		segments.append([])

	segment_size = len(list) // cores

	for i in range(cores - 1):
		for j in range(i * segment_size, (i + 1) * segment_size):
			segments[i].append(list[j])
	
	for j in range((cores - 1) * segment_size, len(list)):
		segments[cores - 1].append(list[j])

	return segments

initial_state = State.initialise()
states = [initial_state]
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
moves = 0
is_solved = False
next_gen_states = []
solution_state = None

while (not is_solved):

	print("\nDepth: " + str(moves), end="")
	print(", Batch Size: " + str(len(states)), end="")
	print(", Total States: " + str(len(State.hashed_states)), end="")
	
	''' Parallel; trying out. ~2x slower lol
	state_segments = segment(states)
	
	threads = []

	for i in range(os.cpu_count()):
		threads.append(Thread(target = KlotskiSolver, args = (i, state_segments[i])))

	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()
	'''

	KlotskiSolver(0, states)

	moves += 1
	states = next_gen_states
	next_gen_states = []

print("\nSolution found!")
print("Minimum number of moves required: " + str(moves))
time.sleep(2)

# backtracking predecessor dictionary
State.hashed_states[initial_state.hash()] = (None, None)
state_key = solution_state.hash()
successor_state = solution_state
move_sequence = []

while (state_key):
	move_sequence.append(str(successor_state))
	successor_state, state_key = State.hashed_states[state_key]


# tracing the path used to reach solution
moves = 0
print("Tracing the path used to reach solution.")
print("\nMove sequence:")
time.sleep(1)
for state in move_sequence[::-1]:
	print("\nMove: " + str(moves))
	print(str(state))
	time.sleep(0.1)
	moves += 1
print("SOLVED")