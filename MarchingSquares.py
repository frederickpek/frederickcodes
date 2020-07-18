import pygame as pg
import random
import datetime
from math import ceil
from opensimplex import OpenSimplex

class MarchingSquares:
	def __init__(self):
		self.x = 1200
		self.y = 700
		self.res = 20
		self.cols = 1 + self.x // self.res
		self.rows = 1 + self.y // self.res
		self.grid = [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
		self.noise = OpenSimplex()
		self.z_offset = 0
		self.z_incr = 0.05

	def make_video(self, screen):
		_image_num = 0
		while True:
			_image_num += 1
			str_num = "000" + str(_image_num)
			file_name = "./images/image" + str_num[-4:] + ".jpg"
			pg.image.save(screen, file_name)
			yield

	def render_grid(self, canvas):
		canvas.fill([0, 0, 0])
		g = self.grid

		# gridlines
		# colour = [50, 50, 50]
		# for i in range(self.cols):
		# 	x_coor = i * self.res
		# 	pg.draw.line(canvas, colour, (x_coor, 0), (x_coor, self.y), 1)
		# for i in range(self.rows):
		# 	y_coor = i * self.res
		# 	pg.draw.line(canvas, colour, (0, y_coor), (self.x, y_coor), 1)

		# points
		fonts = pg.font.get_fonts()
		font = pg.font.SysFont(fonts[2], 10)
		for i in range(len(g)):
			for j in range(len(g[i])):
				gsc = 50 + g[i][j] * 205 if g[i][j] > 0 else 0
				colour = [0, gsc, 0]
				pg.draw.circle(canvas, colour, (j * self.res, i * self.res), 2)
				# val = "{:.2f}".format(g[i][j]) if g[i][j] > 0 else "0.0"
				# text = font.render(val, True, [150, 150, 150])
				# canvas.blit(text, (j * self.res, i * self.res))

		# contours
		for i in range(len(g) - 1):
			for j in range(len(g[i]) - 1):
				x = j * self.res
				y = i * self.res

				a_val = g[i][j] + 1
				b_val = g[i][j+1] + 1
				c_val = g[i+1][j+1] + 1
				d_val = g[i+1][j] + 1

				amt = (1 - a_val) / (b_val - a_val)
				a_x = self.interpolate(x, x + self.res, amt)
				a = (a_x, y)

				amt = (1 - b_val) / (c_val - b_val)
				b_y = self.interpolate(y, y + self.res, amt)
				b = (x + self.res, b_y)

				amt = (1 - d_val) / (c_val - d_val)
				c_x = self.interpolate(x, x + self.res, amt)
				c = (c_x, y + self.res)

				amt = (1 - a_val) / (d_val - a_val)
				d_y = self.interpolate(y, y + self.res, amt)
				d = (x, d_y)

				state = self.get_state(ceil(g[i][j]), ceil(g[i][j+1]), ceil(g[i+1][j+1]), ceil(g[i+1][j]))
				self.draw_line(canvas, a, b, c, d, state)

	def get_state(self, p1, p2, p3, p4):
		return p1*8 + p2*4 + p3*2 + p4

	def draw_line(self, canvas, a, b, c, d, state):
		colour = [255, 255, 255]
		if state == 1:
			pg.draw.line(canvas, colour, c, d, 1)
		elif state == 2:
			pg.draw.line(canvas, colour, b, c, 1)
		elif state == 3:
			pg.draw.line(canvas, colour, b, d, 1)
		elif state == 4:
			pg.draw.line(canvas, colour, a, b, 1)
		elif state == 5:
			pg.draw.line(canvas, colour, a, d, 1)
			pg.draw.line(canvas, colour, b, c, 1)
		elif state == 6:
			pg.draw.line(canvas, colour, a, c, 1)
		elif state == 7:
			pg.draw.line(canvas, colour, a, d, 1)
		elif state == 8:
			pg.draw.line(canvas, colour, a, d, 1)
		elif state == 9:
			pg.draw.line(canvas, colour, a, c, 1)
		elif state == 10:
			pg.draw.line(canvas, colour, a, b, 1)
			pg.draw.line(canvas, colour, c, d, 1)
		elif state == 11:
			pg.draw.line(canvas, colour, a, b, 1)
		elif state == 12:
			pg.draw.line(canvas, colour, b, d, 1)
		elif state == 13:
			pg.draw.line(canvas, colour, b, c, 1)
		elif state == 14:
			pg.draw.line(canvas, colour, c, d, 1)

	def interpolate(self, v1, v2, amt):
		# return (v2 + v1) / 2
		return v1 * (1 - amt)  + v2 * amt

	def screenshot(self, canvas):
		t = datetime.datetime.now()
		day = "{0:0=2d}".format(t.day)
		month = "{0:0=2d}".format(t.month)
		year = t.year % 100
		h = "{0:0=2d}".format(t.hour)
		m = "{0:0=2d}".format(t.minute)
		s = "{0:0=2d}".format(t.second)
		pg.image.save(canvas, "./images/{}-{}-{},{}h{}m{}s.jpeg".format(day, month, year, h, m , s))

	def update_grid(self):
		g = self.grid
		incr = 0.1
		x = 0
		for i in range(len(g)):
			y = 0
			for j in range(len(g[i])):
				g[i][j] = self.noise.noise3d(x, y, self.z_offset)
				y += incr
			x += incr
		self.z_offset += self.z_incr

	def simulate(self):
		pg.init()
		display = pg.display
		display.set_caption("Marching Squares")
		canvas = display.set_mode([self.x, self.y])
		save_screen = self.make_video(canvas)

		quit = False
		video = False
		while not quit:
			for event in pg.event.get():
				if (event.type == pg.QUIT):
					quit = True
				elif (event.type == pg.KEYDOWN):
					if (event.key == pg.K_ESCAPE):
						quit = True
					if (event.key == pg.K_s):
						self.screenshot(canvas)
					if (event.key == pg.K_v):
						video = not video

			self.update_grid()
			self.render_grid(canvas)
			display.update()

			if (video):
				next(save_screen)

		pg.quit()


if __name__ == "__main__":
	algo = MarchingSquares()
	algo.simulate()