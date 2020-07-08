import pygame as pg
import random
import datetime

class Chess:
	WHITE = 1
	BLACK = 0

	def __init__(self):
		self.board = [[None for _ in range(8)] for _ in range(8)]
		self.white_king_pos = None
		self.black_king_pos = None
		self.canvas = None
		self.display = None
		self.quit = False 
		self.is_player_turn = True
		self.is_moving = False
		self.possible_placements = []
		self.og_pos = None
		self.prev_move = []
		self.checkmate_stalemate = -1
		self.promoting_pawn = None

	def draw_board(self, board):
		for row in board:
			for piece in row:
				print(" " + str(piece) if piece else " .", end="")
			print()
		print()

	def generate_board():
		b = [[None for _ in range(8)] for _ in range(8)]
		for side in (0, 1):
			row = side * 7
			b[row][0], b[row][7] = Rook(side), Rook(side)
			b[row][1], b[row][6] = Knight(side), Knight(side)
			b[row][2], b[row][5] = Bishop(side), Bishop(side)
			b[row][3], b[row][4] = Queen(side), King(side)
			row = 1 + side * 5
			for col in range(8):
				b[row][col] = Pawn(side)
		return b

	def initialise():
		chess = Chess()
		chess.board = Chess.generate_board()
		chess.white_king_pos = (7, 4)
		chess.black_king_pos = (0, 4)
		return chess

	def reset_game(self):
		self.board = Chess.generate_board()
		self.possible_placements.clear()
		self.prev_move.clear()
		self.is_player_turn = True
		self.is_moving = False
		self.white_king_pos = (7, 4)
		self.black_king_pos = (0, 4)
		self.checkmate_stalemate = -1
		self.promoting_pawn = None

	def render_board(self, d, col_1, col_2):
		self.canvas.fill(col_1)
		
		# Tiles
		toggle = False
		for i in range(8):
			for j in range(8):
				if (toggle):
					pg.draw.rect(self.canvas, col_2, [i * d, j * d, d, d])
					toggle = False
				else:
					toggle = True
			toggle = not toggle

	def render_grid_lines(self, x, y, d):
		for i in range(1, 8):
			x_coor = i * d
			pg.draw.line(self.canvas, [0, 0, 0], (x_coor, 0), (x_coor, y), 1)

		for i in range(1, 8):
			y_coor = i * d
			pg.draw.line(self.canvas, [0, 0, 0], (0, y_coor), (x, y_coor), 1)

	def highlights(self, moves, d, alpha, colour):
		for pos in moves:
			s = pg.Surface([d, d])
			s.set_alpha(alpha)
			s.fill(colour)
			self.canvas.blit(s, [pos[1] * d, pos[0] * d])

	def render_coordinates(self, d, col_1, col_2):
		fonts = pg.font.get_fonts()
		font = pg.font.SysFont(fonts[2], 16)
		
		toggle = False
		for i in range(8):
			x_coor = i * d
			rank = 8 - i
			colour = col_1 if toggle else col_2
			text = font.render(str(rank), True, colour)
			self.canvas.blit(text, (5, i * d + 5))
			toggle = not toggle
		
		toggle = True
		for i in range(8):
			y_coor = i * d
			file = chr(ord("a") + i)
			colour = col_1 if toggle else col_2
			text = font.render(str(file), True, colour)
			self.canvas.blit(text, (i * d + d - 12, 8 * d - 19))
			toggle = not toggle

	def render_pieces(self, d):
		b = self.board
		for i in range(8):
			for j in range(8):
				if (b[i][j]):
					piece_image = pg.transform.smoothscale(b[i][j].get_image(), [d-10, d-10])
					self.canvas.blit(piece_image, [j * d+5, i * d+5])

	def render_game_over_screen(self, x, y):
		if (self.game_over()):
			s = pg.Surface([x, y])
			s.set_alpha(180)
			s.fill([255, 255, 255])
			self.canvas.blit(s, [0, 0])

			fonts = pg.font.get_fonts()
			font = pg.font.SysFont(fonts[2], 30)
			string = "The game ended in Stalemate!"
			if (self.checkmate_stalemate == 1):
				side = "White" if not self.is_player_turn else "Black"
				string = "{} has won by Checkmate!".format(side)
			text = font.render(string, True, [0, 0, 0])
			self.canvas.blit(text, (100, y // 2 - 30))

	def render_game(self):
		col_1 = [234, 233, 210]
		col_2 = [75, 115, 153]
		x, y = pg.display.get_surface().get_size()
		d = x // 8
		self.render_board(d, col_1, col_2)
		self.highlights(self.prev_move, d, 150, [20, 150, 210])
		self.highlights(self.possible_placements, d, 180, [170, 238, 187])
		self.render_grid_lines(x, y, d)
		self.render_coordinates(d, col_1, col_2)
		self.render_pieces(d)
		self.render_pawn_promotion_GUI(x, y, d)
		self.render_game_over_screen(x, y)

	def key_pressed_events_manager(self, event):
		if (event.key == pg.K_ESCAPE):
			self.quit = True

		elif (event.key == pg.K_s):
			self.screenshot()

		elif (event.key == pg.K_r):
			self.reset_game()

	def select_piece(self, mouse_pos):
		x, y = pg.display.get_surface().get_size()
		col = mouse_pos[0] // (x // 8)
		row = mouse_pos[1] // (y // 8)
		return self.board[row][col], (row, col)

	def update_possible_placements(self, piece, pos):
		self.og_pos = pos
		self.is_moving = True
		self.possible_placements = piece.move_set(self.board, pos)
		# Below line of code is required to ammend highlights of moves which go into check, 
		# this hinders gameplay experience as there will be a slight delay between 
		# piece-selection and highlighting the piece's moves.
		# The actual gameplay and legality of moves are not affected.
		#
		# self.possible_placements = list(filter(self.check_predicate(Chess.WHITE, pos), self.possible_placements))

	def try_movement(self, pos):
		if (pos in self.possible_placements):
			if(self.move_peice(self.og_pos, pos, Chess.WHITE)):
				if (not self.promoting_pawn):
					self.is_player_turn = False
		self.is_moving = False
		self.possible_placements.clear()

	def click_events_manager(self):
		if(self.is_player_turn and not self.game_over()):
			piece, pos = self.select_piece(pg.mouse.get_pos())
			
			if (self.promoting_pawn):
				self.pawn_promotion_GUI(pos)

			elif (piece and piece.side == Chess.WHITE):
				self.update_possible_placements(piece, pos)

			elif (self.is_moving):
				self.try_movement(pos)

	def castle_manager(self, frm, to, side):
		if (self.board[to[0]][to[1]].is_king()):
			if (side == Chess.WHITE):
				self.white_king_pos = (to[0], to[1])
			else:
				self.black_king_pos = (to[0], to[1])

			if (abs(to[1] - frm[1]) == 2):
				dir = frm[1] - to[1]
				if (dir == 2): # Queen-side castle
					r = (frm[0], 0)
					dr = (frm[0], 3)	
				else:
					r = (frm[0], 7)
					dr = (frm[0], 5)
				self.move_piece_(self.board, r, dr)

	def pawn_promotion_manager(self, to, side):
		if (to[0] == 0 or to[0] == 7):
			if (self.board[to[0]][to[1]].is_pawn()):
				if (self.is_player_turn):
					self.promoting_pawn = to
				else:
					self.board[to[0]][to[1]] = Queen(side)

	def pawn_promotion_manager_(self, to, side):
		# let player pawn auto be queen for minimax
		if (to[0] == 0 or to[0] == 7):
			if (self.board[to[0]][to[1]].is_pawn()):
					self.board[to[0]][to[1]] = Queen(side)

	def possible_promotions(self):
		p = self.promoting_pawn
		q = p
		r = (1, p[1])
		b = (2, p[1])
		n = (3, p[1])
		side = self.board[p[0]][p[1]].side
		return [(Queen(side), q), (Rook(side), r), (Bishop(side), b), (Knight(side), n)]

	def pawn_promotion_GUI(self, mouse_pos):
		promotions = self.possible_promotions()
		for piece, pos in promotions:
			if (mouse_pos == pos):
				p = self.promoting_pawn
				self.board[p[0]][p[1]] = piece
				self.promoting_pawn = None
				self.is_player_turn = False

	def render_pawn_promotion_GUI(self, x, y, d):
		if (self.promoting_pawn):
			s = pg.Surface([x, y])
			s.set_alpha(180)
			s.fill([255, 255, 255])
			self.canvas.blit(s, [0, 0])

			promotions = self.possible_promotions()

			for piece, pos in promotions:
				piece_image = pg.transform.smoothscale(piece.get_image(), [d-10, d-10])
				self.canvas.blit(piece_image, [pos[1] * d+5, pos[0] * d+5])

	def update_prev_move(self, frm, to):
		#
		self.prev_move = [frm, to]

	def update_mates(self, side):
		other_side = Chess.WHITE if (side == Chess.BLACK) else Chess.BLACK
		
		if (self.checkmate(other_side)):
			self.checkmate_stalemate = 1
		
		elif (self.stalemate(other_side)):
			self.checkmate_stalemate = 0

	def move_piece_(self, board, frm, to):
		board[frm[0]][frm[1]].has_moved = True
		board[to[0]][to[1]] = board[frm[0]][frm[1]]
		board[frm[0]][frm[1]] = None

	def move_peice(self, frm, to, side):
		if (not self.check(side, frm, to)):
			self.move_piece_(self.board, frm, to)
			self.castle_manager(frm, to, side)
			self.pawn_promotion_manager(to, side)
			self.update_prev_move(frm, to)
			self.update_display(True)
			if (not self.promoting_pawn):
				self.update_mates(side)
			return True
		return False

	def ai_move(self, minimax_move=False):
		if (not self.is_player_turn and not self.game_over()):
			if (minimax_move):
				self.ai_minimax_move()
			else:
				self.ai_rand_input()
			self.is_player_turn = True

	def ai_rand_input(self):
		row = [0, 1, 2, 3, 4, 5, 6, 7]
		col = [0, 1, 2, 3, 4, 5, 6, 7]
		random.shuffle(row)
		random.shuffle(col)
		b = self.board
		for r in row:
			for c in col:
				piece = b[r][c]
				if (piece and piece.side == Chess.BLACK):
					moves = piece.move_set(b, (r, c))
					if (len(moves) > 0):
						for to in moves:
							if(self.move_peice((r, c), to, Chess.BLACK)):
								return

	def update_display(self, clear_possible_placements=False):
		if (clear_possible_placements):
			self.possible_placements.clear()
		self.render_game()
		self.display.update()

	def check(self, side, frm, to):
		king_pos = None

		# copy board
		b2 = []
		for i in range(8):
			row = []
			for j in range(8):
				piece = self.board[i][j]
				if (piece):
					piece = piece.copy()
					if (piece.is_king() and piece.side == side):
						king_pos = (i, j)
				row.append(piece)
			b2.append(row)

		# make move on board2
		self.move_piece_(b2, frm, to)

		if (b2[to[0]][to[1]].is_king()):
			king_pos = (to[0], to[1])

		# check if king_pos is in !side_piece.move_set()
		for i in range(8):
			for j in range(8): 
				piece = b2[i][j]
				if (piece and not piece.side == side):
					if (king_pos in piece.move_set(b2, (i, j))):
						return True

		return False

	def no_legal_moves(self, king):
		for i in range(8):
			for j in range(8):
				piece = self.board[i][j]
				if (piece and (piece.side == king.side)):
					for pos in piece.move_set(self.board, (i, j)):
						if(not self.check(king.side, (i, j), pos)):
							return False
		return True

	def checkmate(self, side):
		king_pos = self.white_king_pos if (side == Chess.WHITE) else self.black_king_pos
		king = self.board[king_pos[0]][king_pos[1]]
		if(king.threat(self.board, king_pos, side)):
			if (self.no_legal_moves(king)):
				return True
		return False

	def stalemate(self, side):
		return False
		king_pos = self.white_king_pos if (side == Chess.WHITE) else self.black_king_pos
		king = self.board[king_pos[0]][king_pos[1]]
		if(not king.threat(self.board, king_pos, side)):
			if (self.no_legal_moves(king)):
				return True
		return False

	def check_predicate(self, side, frm):
		#
		return lambda to : not self.check(side, frm, to)

	def game_over(self):
		#
		return not self.checkmate_stalemate == -1

	def screenshot(self):
		t = datetime.datetime.now()
		day = "{0:0=2d}".format(t.day)
		month = "{0:0=2d}".format(t.month)
		year = t.year % 100
		h = "{0:0=2d}".format(t.hour)
		m = "{0:0=2d}".format(t.minute)
		s = "{0:0=2d}".format(t.second)
		pg.image.save(self.canvas, "./images/{}-{}-{},{}h{}m{}s.jpeg".format(day, month, year, h, m , s))

	def simulate(self):
		pg.init()
		self.display = pg.display
		self.display.set_caption("Chess")
		self.canvas = self.display.set_mode([600, 600])

		while not self.quit:
			
			for event in pg.event.get():

				if (event.type == pg.QUIT):
					self.quit = True

				elif (event.type == pg.KEYDOWN):
					self.key_pressed_events_manager(event)

				elif (event.type == pg.MOUSEBUTTONDOWN):
					self.click_events_manager()

			self.ai_move()

			self.update_display()

		pg.quit()

	## Chess - ai portion below ##

	def board_value(self):
		value = 0
		for i in range(8):
			for j in range(8):
				piece = self.board[i][j]
				if (piece):
					value += piece.get_value() + piece.get_piece_square_value(i, j)
		return value

	def copy(self):
		game_state = Chess()
		game_state.board = [[piece.copy() if piece else None for piece in row] for row in self.board]
		game_state.white_king_pos = self.white_king_pos
		game_state.black_king_pos = self.black_king_pos
		game_state.is_player_turn = self.is_player_turn
		game_state.checkmate_stalemate = self.checkmate_stalemate
		game_state.canvas = self.canvas
		game_state.display = self.display
		return game_state

	def child(self, frm, to, side):
		child = self.copy()
		child.move_piece_(child.board, frm, to)
		child.is_player_turn = not child.is_player_turn
		child.castle_manager(frm, to, side)
		child.pawn_promotion_manager_(to, side)
		child.update_display(True)
		child.update_mates(side)
		return child

	def child_states(self):
		states = []
		for i in range(8):
			for j in range(8):
				frm = (i, j)
				piece = self.board[i][j]
				side = Chess.WHITE if self.is_player_turn else Chess.BLACK
				if (piece and piece.side == side):
					for to in piece.move_set(self.board, (i, j)):
						if (not self.check(piece.side, frm, to)):
							child = self.child(frm, to, piece.side)
							states.append((child, frm, to))
		return states

	def minimax(self, game_state, depth, is_maximizing, alpha, beta):
		if (depth == 0 or game_state.game_over()):
			return game_state.board_value(), (None, None) # 

		if (is_maximizing):
			max_eval = -1000000
			for child, frm, to in game_state.child_states():
				eval, _ = self.minimax(child, depth - 1, False, alpha, beta)
				# print("depth:", depth, "score:", eval, frm, to)
				if (eval >= max_eval):
					max_eval = eval
					best_move = (frm, to)
				alpha = max(alpha, eval)
				if (beta <= alpha):
					break
			return max_eval, best_move
		
		else:
			min_eval = 1000000
			for child, frm, to in game_state.child_states():
				eval, _ = self.minimax(child, depth - 1, True, alpha, beta)
				# print("depth:", depth, "score:", eval, frm, to)
				if (eval <= min_eval):
					min_eval = eval
					best_move = (frm, to)
				beta = min(beta, eval)
				if (beta <= alpha):
					break
			return min_eval, best_move

	def ai_minimax_move(self):
		best_score, best_move = self.minimax(self, 3, False, -1000001, 1000001)
		frm, to = best_move
		# print("Move with best score is:", best_score, best_move)
		self.move_peice(frm, to, Chess.BLACK)

class Piece(object):
	diagonals = [(-1, -1), (1, 1), (1, -1), (-1, 1)]
	cardinals = [(-1, 0), (1, 0), (0, -1), (0, 1)]
	dict = { 1:"white", 0:"black" }
	def __init__(self, side, name):
		self.name = name
		self.side = side
		self.image = pg.image.load("./images/{}_{}.png".format(Piece.dict[side], name))
		self.has_moved = False
		self.table = None
		self.value = None

	def get_image(self):
		return self.image

	def not_own_piece(self, board):
		#
		return lambda p : (board[p[0]][p[1]] and board[p[0]][p[1]].side != self.side) or not board[p[0]][p[1]]

	def in_bounds(self):
		#
		return lambda p : p[0] < 8 and p[0] > -1 and p[1] < 8 and p[1] > -1

	def default_moves(self, board, pos):
		pass

	def relative_pos(self, pos):
		#
		return lambda p : (p[0] + pos[0], p[1] + pos[1])

	def move_set(self, board, pos):
		own_moves = self.default_moves(board, pos)
		in_bound_moves = list(filter(self.in_bounds(), own_moves))
		less_own_pieces = list(filter(self.not_own_piece(board), in_bound_moves))
		return less_own_pieces

	def threat(self, board, pos, side):
		for i in range(8):
			for j in range(8):
				piece = board[i][j]
				if (piece and not piece.side == side):
					if (pos in piece.move_set(board, (i, j))):
						return True
		return False

	def copy(self):
		pass

	def is_king(self):
		return False

	def is_pawn(self):
		return False

	def get_piece_square_value(self, i, j):
		if (self.side == Chess.WHITE):
			return self.table[i][j]
		else:
			return -self.table[7-i][7-j]
	
	def get_value(self):
		if (self.side == Chess.WHITE):
			return self.value
		else:
			return -self.value

	def __str__(self):
		return self.name[:1]

class Pawn(Piece):
	def __init__(self, side):
		super().__init__(side, "pawn")
		self.table = [[ 0,  0,  0,  0,  0,  0,  0,  0],
				 	  [50, 50, 50, 50, 50, 50, 50, 50],
				 	  [10, 10, 20, 30, 30, 20, 10, 10],
		 		 	  [ 5,  5, 10, 25, 25, 10,  5,  5],
		 		 	  [ 0,  0,  0, 20, 20,  0,  0,  0],
		 		 	  [ 5, -5,-10,  0,  0,-10, -5,  5],
		 		 	  [ 5, 10, 10,-20,-20, 10, 10,  5],
		 		 	  [ 0,  0,  0,  0,  0,  0,  0,  0]]
		self.value = 100

	def default_moves(self, board, pos):
		dir = -1 if self.side == Chess.WHITE else 1
		moves = []
		m1 = (dir + pos[0],pos[1])
		if (self.in_bounds()(m1) and not board[m1[0]][m1[1]]):
			moves.append(m1)
			m2 = (dir * 2 + pos[0], pos[1])
			if (not self.has_moved and not board[m2[0]][m2[1]]):
				moves.append(m2)
		
		# Caputures
		m1 = (dir + pos[0],pos[1] + 1)
		if (self.in_bounds()(m1) and board[m1[0]][m1[1]] and not board[m1[0]][m1[1]].side == self.side):
			moves.append(m1) 
		m1 = (dir + pos[0],pos[1] - 1)
		if (self.in_bounds()(m1) and board[m1[0]][m1[1]] and not board[m1[0]][m1[1]].side == self.side):
			moves.append(m1) 

		return moves

	def copy(self):
		pawn = Pawn(self.side)
		pawn.has_moved = self.has_moved
		return pawn

	def is_pawn(self):
		return True

class Knight(Piece):
	def __init__(self, side):
		super().__init__(side, "knight")
		self.table = [[-50,-40,-30,-30,-30,-30,-40,-50],
					  [-40,-20,  0,  0,  0,  0,-20,-40],
					  [-30,  0, 10, 15, 15, 10,  0,-30],
					  [-30,  5, 15, 20, 20, 15,  5,-30],
					  [-30,  0, 15, 20, 20, 15,  0,-30],
					  [-30,  5, 10, 15, 15, 10,  5,-30],
					  [-40,-20,  0,  5,  5,  0,-20,-40],
					  [-50,-40,-30,-30,-30,-30,-40,-50]]
		self.value = 320

	def default_moves(self, board, pos):
		moves = [(-2, 1), (-2, -1), (-1, 2), (-1, -2), (1, 2), (1, -2), (2, 1), (2, -1)]
		relative_pos = list(map(self.relative_pos(pos), moves))
		return list(filter(self.in_bounds(), relative_pos))

	def copy(self):
		knight = Knight(self.side)
		knight.has_moved = self.has_moved
		return knight

	def __str__(self):
		return self.name[1:2]

class Bishop(Piece):
	def __init__(self, side):
		super().__init__(side, "bishop")
		self.table = [[-20,-10,-10,-10,-10,-10,-10,-20],
					  [-10,  0,  0,  0,  0,  0,  0,-10],
					  [-10,  0,  5, 10, 10,  5,  0,-10],
					  [-10,  5,  5, 10, 10,  5,  5,-10],
					  [-10,  0, 10, 10, 10, 10,  0,-10],
					  [-10, 10, 10, 10, 10, 10, 10,-10],
					  [-10,  5,  0,  0,  0,  0,  5,-10],
					  [-20,-10,-10,-10,-10,-10,-10,-20]]
		self.value = 330

	def default_moves(self, board, pos):
		moves = []
		for dir in Piece.diagonals:
			for i in range(1, 8):
				relative_pos = (dir[0] * i + pos[0], dir[1] * i + pos[1])
				if (not self.in_bounds()(relative_pos)):
					break
				moves.append(relative_pos)
				if (board[relative_pos[0]][relative_pos[1]]):
					break
		return moves

	def copy(self):
		bishop = Bishop(self.side)
		bishop.has_moved = self.has_moved
		return bishop

class Rook(Piece):
	def __init__(self, side):
		super().__init__(side, "rook")
		self.table = [[ 0,  0,  0,  0,  0,  0,  0,  0],
					  [ 5, 10, 10, 10, 10, 10, 10,  5],
					  [-5,  0,  0,  0,  0,  0,  0, -5],
					  [-5,  0,  0,  0,  0,  0,  0, -5],
					  [-5,  0,  0,  0,  0,  0,  0, -5],
					  [-5,  0,  0,  0,  0,  0,  0, -5],
					  [-5,  0,  0,  0,  0,  0,  0, -5],
					  [ 0,  0,  0,  5,  5,  0,  0,  0]]
		self.value = 500

	def default_moves(self, board, pos):
		moves = []
		for dir in Piece.cardinals:
			for i in range(1, 8):
				relative_pos = (dir[0] * i + pos[0], dir[1] * i + pos[1])
				if (not self.in_bounds()(relative_pos)):
					break
				moves.append(relative_pos)
				if (board[relative_pos[0]][relative_pos[1]]):
					break
		return moves

	def copy(self):
		rook = Rook(self.side)
		rook.has_moved = self.has_moved
		return rook

class Queen(Piece):
	def __init__(self, side):
		super().__init__(side, "queen")
		self.table = [[-20,-10,-10, -5, -5,-10,-10,-20],
			  		  [-10,  0,  0,  0,  0,  0,  0,-10],
			  		  [-10,  0,  5,  5,  5,  5,  0,-10],
			  		  [ -5,  0,  5,  5,  5,  5,  0, -5],
			  		  [  0,  0,  5,  5,  5,  5,  0, -5],
			  		  [-10,  5,  5,  5,  5,  5,  0,-10],
			  		  [-10,  0,  5,  0,  0,  0,  0,-10],
			  		  [-20,-10,-10, -5, -5,-10,-10,-20]]
		self.value = 900

	def default_moves(self, board, pos):
		moves = []
		for dir in Piece.diagonals:
			for i in range(1, 8):
				relative_pos = (dir[0] * i + pos[0], dir[1] * i + pos[1])
				if (not self.in_bounds()(relative_pos)):
					break
				moves.append(relative_pos)
				if (board[relative_pos[0]][relative_pos[1]]):
					break
		for dir in Piece.cardinals:
			for i in range(1, 8):
				relative_pos = (dir[0] * i + pos[0], dir[1] * i + pos[1])
				if (not self.in_bounds()(relative_pos)):
					break
				moves.append(relative_pos)
				if (board[relative_pos[0]][relative_pos[1]]):
					break
		return moves

	def copy(self):
		queen = Queen(self.side)
		queen.has_moved = self.has_moved
		return queen

class King(Piece):
	def __init__(self, side):
		super().__init__(side, "king")
		self.table = [[-30,-40,-40,-50,-50,-40,-40,-30],
			  		  [-30,-40,-40,-50,-50,-40,-40,-30],
			  		  [-30,-40,-40,-50,-50,-40,-40,-30],
			  		  [-30,-40,-40,-50,-50,-40,-40,-30],
			  		  [-20,-30,-30,-40,-40,-30,-30,-20],
			  		  [-10,-20,-20,-20,-20,-20,-20,-10],
			  		  [ 20, 20,  0,  0,  0,  0, 20, 20],
			  		  [ 20, 30, 10,  0,  0, 10, 30, 20]]
		self.value = 20000

	def default_moves(self, board, pos):
		moves = []
		for dir in Piece.diagonals:
			moves.append((dir[0], dir[1]))
		for dir in Piece.cardinals:
			moves.append((dir[0], dir[1]))
		moves = list(map(self.relative_pos(pos), moves))
		moves = list(filter(self.in_bounds(), moves))
		moves = moves + self.castle(board, pos)
		return moves

	def copy(self):
		king = King(self.side)
		king.has_moved = self.has_moved
		return king

	def is_king(self):
		return True

	def castle(self, board, pos):
		moves = []
		if (self.has_moved):
			return moves
		king_rook = (self.relative_pos(pos)((0, 3)), self.relative_pos(pos)((0, 2)))
		queen_rook = (self.relative_pos(pos)((0, -4)), self.relative_pos(pos)((0, -2)))
		king_side_piece_pos = tuple(self.relative_pos(pos)((0, i)) for i in range(1, 3))
		queen_side_piece_pos = tuple(self.relative_pos(pos)((0, -i)) for i in range(1, 4))
		sides = [(king_rook, king_side_piece_pos), (queen_rook, queen_side_piece_pos)]

		for s in sides:
			r = s[0][0]
			piece_pos = s[1]
			rook = board[r[0]][r[1]]
			if (rook and not rook.has_moved):
				all_empty = True
				for p in piece_pos:
					if (board[p[0]][p[1]]):
						all_empty = False
				if (all_empty):
					positions = pos + r + piece_pos
					all_no_threat = True
					for p in positions:
						if (self.threat(board, p, self.side)):
							all_no_threat = False
					if (all_no_threat):
						moves.append(s[0][1])

		return moves

if __name__ == "__main__":
	game = Chess.initialise()
	game.simulate()