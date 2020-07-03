import pygame as pg
import random
import datetime

class TTT:
	count = 0
	n = 3
	player = "O"
	AI = "X"
	def __init__(self):
		self.grid = [[None for _ in range(TTT.n)] for _ in range(TTT.n)]

	def render_grid(self, canvas):
		canvas.fill([250, 250, 250])
		x, y = pg.display.get_surface().get_size()
		g = self.grid

		# Grid lines
		for i in range(1, len(g[1])):
			x_coor = i * x // len(g)
			pg.draw.line(canvas, [0, 0, 0], (x_coor, 0), (x_coor, y), 3)
		for i in range(1, len(g)):
			y_coor = i * y // len(g)
			pg.draw.line(canvas, [0, 0, 0], (0, y_coor), (x, y_coor), 3)

		fonts = pg.font.get_fonts()
		font = pg.font.SysFont(fonts[1], 50)

		# Grid contents
		for i in range(len(g)):
			for j in range(len(g[1])):
				string = "" if not g[i][j] else str(g[i][j])
				text = font.render(string, 0, [0, 0, 0])
				unit_x = x // len(g)
				unit_y = y // len(g)
				offset_x = unit_x / TTT.n
				offset_y = unit_y / TTT.n
				pos = (j * unit_x + offset_x, i * unit_y + offset_y)
				canvas.blit(text, pos)

	def is_valid_input(self, row, col):
		return not self.grid[row][col]

	def player_input(self, mouse_pos):
		x, y = pg.display.get_surface().get_size()
		col = mouse_pos[0] // (x // TTT.n)
		row = mouse_pos[1] // (y // TTT.n)
		if (self.is_valid_input(row, col)):
			self.grid[row][col] = TTT.player
			return True
		return False

	def full_board(self):
		all_filled = True
		for row in self.grid:
			for cell in row:
				if (not cell):
					return False
		return True

	def AI_rand_input(self):
		if (not self.full_board()):
			while True:
				row = random.randint(0, TTT.n - 1)
				col = random.randint(0, TTT.n - 1)
				if (self.is_valid_input(row, col)):
					self.grid[row][col] = TTT.AI
					break

	def AI_minimax_input(self):
		if (self.full_board()):
			return
		g = self.grid
		best_score = -1000
		for i in range(len(g)):
			for j in range(len(g[1])):
				if (not g[i][j]):
					g[i][j] = TTT.AI
					score = self.minimax(False, -1000, 1000)
					g[i][j] = None
					if (score >= best_score):
						best_score = score
						best_move = (i, j)
		g[best_move[0]][best_move[1]] = TTT.AI
		print("End-states calculated:", TTT.count)
		TTT.count = 0

	def minimax(self, is_AI, alpha, beta):
		g = self.grid
		if (not self.winner_found() == -1):
			TTT.count += 1
			if (self.winner_found() == 0):
				return 0
			return -10 if is_AI else 10

		if (is_AI):
			best_score = -1000
			for i in range(len(g)):
				for j in range(len(g[1])):
					if (not g[2-i][2-j]):
						g[2-i][2-j] = TTT.AI
						score = self.minimax(False, alpha, beta)
						g[2-i][2-j] = None
						best_score = max(score, best_score)
						alpha = max(alpha, score)
						if (beta <= alpha):
							break
				if (beta <= alpha):
					break
			return best_score
		
		else:
			best_score = 1000
			for i in range(len(g)):
				for j in range(len(g[1])):
					if (not g[i][j]):
						g[i][j] = TTT.player
						score = self.minimax(True, alpha, beta)
						g[i][j] = None
						best_score = min(score, best_score)
						beta = min(beta, score)
						if (beta <= alpha):
							break
				if (beta <= alpha):
					break
			return best_score

	def is_tie_game(self):
		# Assumes no one won yet
		g = self.grid
		for row in g:
			for cell in row:
				if (not cell):
					return False
		return True

	def winner_found(self):
		# This is where all my efforts to not hardcode params fall
		# Am just gonna use the *3*-ina-row logic
		g = self.grid
		# Rows
		for i in range(len(g)):
			if (g[i][0] and g[i][0] == g[i][1] and g[i][0] == g[i][2]):
				return 1
		# Cols
		for i in range(len(g[1])):
			if (g[0][i] and g[0][i] == g[1][i] and g[0][i] == g[2][i]):
				return 1
		
		if (g[0][0] and g[0][0] == g[1][1] and g[0][0] == g[2][2]):
			return 1

		if (g[0][2] and g[0][2] == g[1][1] and g[0][2] == g[2][0]):
			return 1

		if (self.is_tie_game()):
			return 0

		return -1

	def end_game(self, canvas, is_player_turn, is_tie):
		fonts = pg.font.get_fonts()
		font = pg.font.SysFont(fonts[1], 40)
		if (is_tie):
			string = "ITS A TIE!"
		else:
			string = (TTT.player if is_player_turn else TTT.AI) + " WON!"
		text = font.render(string, 0, [255, 0, 0])
		canvas.blit(text, (30, 5))

	def score_text(self):
		pass

	def screenshot(self, canvas):
		t = datetime.datetime.now()
		day = "{0:0=2d}".format(t.day)
		month = "{0:0=2d}".format(t.month)
		year = t.year % 100
		h = "{0:0=2d}".format(t.hour)
		m = "{0:0=2d}".format(t.minute)
		s = "{0:0=2d}".format(t.second)
		pg.image.save(canvas, "./images/{}-{}-{},{}h{}m{}s.jpeg".format(day, month, year, h, m , s))

	def simulate(self):
		pg.init()
		display = pg.display
		display.set_caption("TicTacToe")
		
		x, y = 350, 350 
		canvas = display.set_mode([x, y])

		is_player_turn = False
		game_won = -1

		window = True
		while window:
			if (is_player_turn):
				for event in pg.event.get():
					if (event.type == pg.QUIT):
						window = False
					elif (event.type == pg.KEYDOWN):
						if (event.key == pg.K_ESCAPE):
							window = False
						if (event.key == pg.K_s):
							self.screenshot(canvas)
					elif (event.type == pg.MOUSEBUTTONDOWN):
						pos = pg.mouse.get_pos()
						if (self.player_input(pos)):
							is_player_turn = False
			else:
				self.AI_minimax_input()
				# self.AI_rand_input()
				is_player_turn = True

			self.render_grid(canvas)

			if (not self.winner_found() == -1):
				self.end_game(canvas, not is_player_turn, self.winner_found() == 0)
			
			if (game_won == -1):
				display.update()

			if (not self.winner_found() == -1):
				game_won = self.winner_found()

		pg.quit()

if __name__ == "__main__":
	game = TTT()
	game.simulate()