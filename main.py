#!.env/bin/python

import pygame
import numpy as np

import sys

class SquareEnv:
	def __init__(self, WIDTH, HEIGHT, raws, cols, agent_color, destination_color):
		self.WIDTH = WIDTH
		self.HEIGHT = HEIGHT
		self.raws = raws
		self.cols = cols
		self.agent_color = agent_color
		self.destination_color = destination_color
		self.square_width = WIDTH//cols	
		self.square_height = HEIGHT//raws	
	
		self.running = True

		self.agent_current_raw = None
		self.agent_current_col = None

		self.destination_current_raw = None
		self.destination_current_col = None

		self.max_distance = raws + cols

		self.screen = None


	def computeReward(self):
		return -self.computeManhattanDistance() / self.max_distance

	def computeManhattanDistance(self):
		abs_delta_raw = abs(self.agent_current_raw - self.destination_current_raw)
		abs_delta_col = abs(self.agent_current_col - self.destination_current_col)
		return abs_delta_raw + abs_delta_col
	

	def setAgentAndDestination(self):
		self.agent_current_raw = np.random.randint(0, self.raws)
		self.agent_current_col = np.random.randint(0, self.cols)

		self.destination_current_raw = np.random.randint(0, self.raws)
		self.destination_current_col = np.random.randint(0, self.cols)

		same_raw = self.agent_current_raw and self.destination_current_raw
		same_col = self.agent_current_col and self.destination_current_col
		if same_raw and same_col:
			self.setAgentAndDestination()


	def drawGrid(self):
		for row in range(self.square_height, self.HEIGHT, self.square_height):
			self.canvas[row, :] = self.agent_color
	
		for col in range(self.square_width, self.WIDTH,  self.square_width):
			self.canvas[:, col] = self.agent_color
	
	def drawSquare(self, raw, col, color):
		begin_raw = raw*self.square_width
		end_raw= raw*self.square_width + self.square_width
	
		begin_col = col*self.square_width
		end_col = col*self.square_width + self.square_width
	
		for u in range(begin_raw, end_raw):
			for v in range(begin_col, end_col):
				self.canvas[u, v] = color

	def moveSquare(self, direction):
		if direction == "LEFT":
			self.agent_current_col -= 1
			self.agent_current_col %= self.cols
		elif direction == "RIGHT":
			self.agent_current_col += 1
			self.agent_current_col %= self.cols
		elif direction == "UP":
			self.agent_current_raw -= 1
			self.agent_current_raw %= self.raws
		elif direction == "DOWN":
			self.agent_current_raw += 1
			self.agent_current_raw %= self.raws

	def execute(self):
		pygame.init()
		self.screen = pygame.display.set_mode((self.HEIGHT, self.WIDTH))

		self.setAgentAndDestination()

		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						self.moveSquare("LEFT")
					elif event.key == pygame.K_RIGHT:
						self.moveSquare("RIGHT")
					elif event.key == pygame.K_UP:
						self.moveSquare("UP")
					elif event.key == pygame.K_DOWN:
						self.moveSquare("DOWN")
					elif event.key == pygame.K_ESCAPE:
						self.running = False


			self.canvas = (np.random.random((self.HEIGHT, self.WIDTH, 3)) * 255.0).astype("uint8")
			self.drawGrid()
			self.drawSquare(self.agent_current_raw, self.agent_current_col, self.agent_color)
			self.drawSquare(self.destination_current_raw, self.destination_current_col, self.destination_color)

			print(self.computeReward())

			self.canvas = np.swapaxes(self.canvas, 0, 1)
			new_surf = pygame.pixelcopy.make_surface(self.canvas)
			self.screen.blit(new_surf, (0, 0))

			pygame.display.update()

		pygame.quit()


def main():

	WIDTH, HEIGHT = 800, 800
	rows, cols = 20, 20
	agent_color = (0, 255, 0)
	destination_color = (255, 0, 0)

	env = SquareEnv(WIDTH, HEIGHT, rows, cols, agent_color, destination_color)
	env.execute()

	
if __name__ == "__main__":
	main()
