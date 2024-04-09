#!.env/bin/python

import pygame
import numpy as np

import sys

class SquareEnv:
	def __init__(self,
				 WIDTH = 100,
				 HEIGHT = 100,
				 WINDOW_WIDTH=800,
				 WINDOW_HEIGHT=800,
				 raws=20,
				 cols=20,
				 agent_color=(0, 255, 0),
				 destination_color=(255, 0, 0),
				 mode="computer"):
		self.WIDTH = WIDTH
		self.HEIGHT = HEIGHT
		self.WINDOW_WIDTH = WINDOW_WIDTH
		self.WINDOW_HEIGHT = WINDOW_HEIGHT
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
		self.canvas = None

		self.mode = mode


	def init(self):
		if self.mode == "human":
			pygame.init()
			self.screen = pygame.display.set_mode((self.WINDOW_HEIGHT, self.WINDOW_WIDTH))

		self.canvas = (np.ones((self.HEIGHT, self.WIDTH, 3)) * 255.0).astype("uint8")
		self.__setAgentAndDestination()
		return self.canvas

	def reset(self):
		return self.init()

	def get_action_space(self):
		return (0, 1, 2, 3)

	def step(self, action):
		assert 0 <= action <= 3
		if action == 0:
			self.agent_current_col -= 1
			self.agent_current_col %= self.cols
		elif action == 1:
			self.agent_current_col += 1
			self.agent_current_col %= self.cols
		elif action == 2:
			self.agent_current_raw -= 1
			self.agent_current_raw %= self.raws
		elif action == 3:
			self.agent_current_raw += 1
			self.agent_current_raw %= self.raws

		reward = self.__computeReward()

		self.canvas = (np.ones((self.HEIGHT, self.WIDTH, 3)) * 255.0).astype("uint8")
		self.__drawGrid()
		self.__drawSquare(self.agent_current_raw, self.agent_current_col, self.agent_color)
		self.__drawSquare(self.destination_current_raw, self.destination_current_col, self.destination_color)

		same_raw = self.agent_current_raw and self.destination_current_raw
		same_col = self.agent_current_col and self.destination_current_col

		terminal = same_raw and same_col
		if self.mode == "human":
			new_surf = pygame.pixelcopy.make_surface(np.swapaxes(self.canvas, 0, 1))
			new_surf = pygame.transform.scale(new_surf, (self.WINDOW_HEIGHT, self.WINDOW_WIDTH))
			self.screen.blit(new_surf, (0, 0))

			pygame.display.update()

		return self.canvas, reward, terminal



	def __computeReward(self):
		return -self.__computeManhattanDistance() / self.max_distance


	def __computeManhattanDistance(self):
		abs_delta_raw = abs(self.agent_current_raw - self.destination_current_raw)
		abs_delta_col = abs(self.agent_current_col - self.destination_current_col)
		return abs_delta_raw + abs_delta_col
	

	def __setAgentAndDestination(self):
		self.agent_current_raw = np.random.randint(0, self.raws)
		self.agent_current_col = np.random.randint(0, self.cols)

		self.destination_current_raw = np.random.randint(0, self.raws)
		self.destination_current_col = np.random.randint(0, self.cols)

		same_raw = self.agent_current_raw and self.destination_current_raw
		same_col = self.agent_current_col and self.destination_current_col
		if same_raw and same_col:
			self.__setAgentAndDestination()


	def __drawGrid(self):
		for row in range(0, self.HEIGHT, self.square_height):
			self.canvas[row, :] = self.agent_color
	
		for col in range(0, self.WIDTH,  self.square_width):
			self.canvas[:, col] = self.agent_color

		self.canvas[:, -1] = self.agent_color
		self.canvas[-1, :] = self.agent_color
	
	def __drawSquare(self, raw, col, color):
		begin_raw = raw*self.square_width+1
		end_raw= raw*self.square_width + self.square_width
	
		begin_col = col*self.square_width+1
		end_col = col*self.square_width + self.square_width
	
		for u in range(begin_raw, end_raw):
			for v in range(begin_col, end_col):
				self.canvas[u, v] = color

	def __moveSquare(self, direction):
		#direction == "LEFT":
		if direction == 0:
			self.agent_current_col -= 1
			self.agent_current_col %= self.cols
		#direction == "RIGHT":
		elif direction == 1:
			self.agent_current_col += 1
			self.agent_current_col %= self.cols
		#direction == "UP":
		elif direction == 2:
			self.agent_current_raw -= 1
			self.agent_current_raw %= self.raws
		#direction == "DOWN":
		elif direction == 3:
			self.agent_current_raw += 1
			self.agent_current_raw %= self.raws

	def executeForHuman(self):
		pygame.init()
		self.screen = pygame.display.set_mode((self.WINDOW_HEIGHT, self.WINDOW_WIDTH))

		self.__setAgentAndDestination()

		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						self.__moveSquare(0)
					elif event.key == pygame.K_RIGHT:
						self.__moveSquare(1)
					elif event.key == pygame.K_UP:
						self.__moveSquare(2)
					elif event.key == pygame.K_DOWN:
						self.__moveSquare(3)
					elif event.key == pygame.K_ESCAPE:
						self.running = False


			#self.canvas = (np.random.random((self.HEIGHT, self.WIDTH, 3)) * 255.0).astype("uint8")
			self.canvas = (np.ones((self.HEIGHT, self.WIDTH, 3)) * 255.0).astype("uint8")
			self.__drawGrid()
			self.__drawSquare(self.agent_current_raw, self.agent_current_col, self.agent_color)
			self.__drawSquare(self.destination_current_raw, self.destination_current_col, self.destination_color)

			print(self.__computeReward())

			new_surf = pygame.pixelcopy.make_surface(np.swapaxes(self.canvas, 0, 1))
			new_surf = pygame.transform.scale(new_surf, (self.WINDOW_HEIGHT, self.WINDOW_WIDTH))
			self.screen.blit(new_surf, (0, 0))

			pygame.display.update()

		pygame.quit()


def main():
	env = SquareEnv()
	env.executeForHuman()

	
if __name__ == "__main__":
	main()
