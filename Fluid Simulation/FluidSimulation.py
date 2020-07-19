import pygame as pg
import random
import datetime
from math import ceil, floor
from opensimplex import OpenSimplex

class Fluid:
	def NxN(self):
		#
		return [0 for _ in range(self.N * self.N)]

	def IX(self, x, y):
		x = min(self.N - 1, max(0, x))
		y = min(self.N - 1, max(0, y))
		return x + y * self.N

	def __init__(self, dt, diffusion, viscosity):
		self.N = 128
		self.iter = 4
		self.scale = 5

		self.dt = dt
		self.diff = diffusion
		self.visc = viscosity

		self.s = self.NxN()
		self.density = self.NxN()

		self.Vx = self.NxN()
		self.Vy = self.NxN()
		self.Vx0 = self.NxN()
		self.Vy0 = self.NxN()

		self.noise = OpenSimplex()
		self.t = 0

	def add_density(self, x, y, amt):
		index = self.IX(x, y)
		self.density[index] += amt

	def add_velocity(self, x, y, amt_x, amt_y):
		index = self.IX(x, y)
		self.Vx[index] += amt_x
		self.Vy[index] += amt_y

	def diffuse(self, b, x, x0, diff):
		a = self.dt * diff * (self.N - 2) * (self.N - 2)
		self.lin_solve(b, x, x0, a, 1 + 6 * a)

	def set_bnd(self, b, x):
		n = self.N
		for i in range(1, n - 1):
			x[self.IX(i, 0    )] = -x[self.IX(i, 1    )] if b == 2 else x[self.IX(i, 1    )]
			x[self.IX(i, n - 1)] = -x[self.IX(i, n - 2)] if b == 2 else x[self.IX(i, n - 2)]

		for j in range(1, n - 1):
			x[self.IX(0    , j)] = -x[self.IX(1    , j)] if b == 1 else x[self.IX(1    , j)]
			x[self.IX(n - 1, j)] = -x[self.IX(n - 2, j)] if b == 1 else x[self.IX(n - 2, j)]

		x[self.IX(0    , 0    )] = 0.5 * (x[self.IX(1    , 0    )] + x[self.IX(0    , 1    )])
		x[self.IX(0    , n - 1)] = 0.5 * (x[self.IX(1    , n - 1)] + x[self.IX(0    , n - 2)])
		x[self.IX(n - 1, 0    )] = 0.5 * (x[self.IX(n - 2, 0    )] + x[self.IX(n - 1, 1    )])
		x[self.IX(n - 1, n - 1)] = 0.5 * (x[self.IX(n - 2, n - 1)] + x[self.IX(n - 1, n - 2)])

	def lin_solve(self, b, x, x0, a, c):
		for k in range(self.iter):
			for j in range(1, self.N - 1):
				for i in range(1, self.N - 1):
					n = x[self.IX(i + 1, j)]
					n += x[self.IX(i - 1, j)]
					n += x[self.IX(i, j + 1)]
					n += x[self.IX(i, j - 1)]
					x[self.IX(i, j)] = (x0[self.IX(i, j)] + a * n) / c
			self.set_bnd(b, x)

	def project(self, velocX, velocY, p, div):
		for j in range(1, self.N - 1):
			for i in range(1, self.N - 1):
				n = velocX[self.IX(i + 1, j)]
				n -= velocX[self.IX(i - 1, j)]
				n += velocY[self.IX(i, j + 1)]
				n -= velocY[self.IX(i, j - 1)]
				div[self.IX(i, j)] = -0.5 * n / self.N
				p[self.IX(i, j)] = 0
	
	
		self.set_bnd(0, div)
		self.set_bnd(0, p)
		self.lin_solve(0, p, div, 1, 6)
    	
		for j in range(1, self.N - 1):
			for i in range(1, self.N - 1):
				nx = p[self.IX(i + 1, j)] - p[self.IX(i - 1, j)]
				ny = p[self.IX(i, j + 1)] - p[self.IX(i, j - 1)]
				velocX[self.IX(i, j)] -= 0.5 * nx * self.N
				velocY[self.IX(i, j)] -= 0.5 * ny * self.N

		self.set_bnd(1, velocX)
		self.set_bnd(2, velocY)

	def advect(self, b, d, d0, velocX, velocY):
		dtx = self.dt * (self.N - 2)
		dty = self.dt * (self.N - 2)

		for j in range(1, self.N - 1):
			for i in range(1, self.N - 1):
				tmp1 = dtx * velocX[self.IX(i, j)]
				tmp2 = dty * velocY[self.IX(i, j)]
				x = i - tmp1
				y = j - tmp2

				if (x < 0.5):
					x = 0.5; 
				if (x > self.N + 0.5): 
					x = self.N + 0.5
				i0 = floor(x)
				i1 = i0 + 1.0
				if (y < 0.5):
					y = 0.5 
				if (y > self.N + 0.5):
					y = self.N + 0.5
				j0 = floor(y);
				j1 = j0 + 1.0

				s1 = x - i0; 
				s0 = 1.0 - s1; 
				t1 = y - j0; 
				t0 = 1.0 - t1;

				i0i = int(i0);
				i1i = int(i1);
				j0i = int(j0);
				j1i = int(j1);

				s_0 = s0 * (t0 * d0[self.IX(i0i, j0i)] + t1 * d0[self.IX(i0i, j1i)])
				s_1 = s1 * (t0 * d0[self.IX(i1i, j0i)] + t1 * d0[self.IX(i1i, j1i)])

				d[self.IX(i, j)] = s_0 + s_1

		self.set_bnd(b, d);

	def step(self):
		self.diffuse(1, self.Vx0, self.Vx, self.visc)
		self.diffuse(2, self.Vy0, self.Vy, self.visc)
	
		self.project(self.Vx0, self.Vy0, self.Vx, self.Vy)
    
		self.advect(1, self.Vx, self.Vx0, self.Vx0, self.Vy0)
		self.advect(2, self.Vy, self.Vy0, self.Vx0, self.Vy0)

		self.project(self.Vx, self.Vy, self.Vx0, self.Vy0)

		self.diffuse(0, self.s, self.density, self.diff);
		self.advect(0, self.density, self.s, self.Vx, self.Vy);

	def add_dye(self):
			centre = self.N // 2
			for i in range(-1, 2):
				for j in range(-1, 2):
					self.add_density(centre + i, centre + j, 100)

			mult = 7
			amt_x = self.noise.noise2d(123, self.t) * mult 
			amt_y = self.noise.noise2d(424, self.t + 1234) * mult 
			self.add_velocity(centre, centre, amt_x, amt_y)
			self.t += 0.1

	def fade_dye(self):
		for d in self.density:
			d = min(255, max(0, d - 0.5))

	def set_brightness(self, b):
		return int(255 * b / (100 + b))

	def render(self, canvas):
		canvas.fill([50, 50, 50])
		
		# density
		for j in range(self.N):
			for i in range(self.N):
				d = self.scale
				b = int(self.density[self.IX(i, j)])
				b = self.set_brightness(b)
				colour = [b, b, b]
				pg.draw.rect(canvas, colour, [i * d, j * d, d, d])

	def make_video(self, screen):
		_image_num = 0
		while True:
			_image_num += 1
			str_num = "000" + str(_image_num)
			file_name = "./images/image" + str_num[-4:] + ".jpg"
			pg.image.save(screen, file_name)
			yield

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
		display.set_caption("Fluid Simulation by Mike Ash")
		d = self.N * self.scale
		canvas = display.set_mode([d, d])
		save_screen = self.make_video(canvas)

		quit = False
		video = True
		vid_frames = 0
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

			self.add_dye()
			self.step()
			self.render(canvas)
			# self.fade_dye()

			display.update()

			if (video):
				vid_frames += 1
				next(save_screen)
				print(vid_frames)
				if (vid_frames == 240):
					video = not video
					quit = True

		pg.quit()


if __name__ == "__main__":
	simulation = Fluid(0.1, 0, 0.00001)
	simulation.simulate()