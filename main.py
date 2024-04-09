#!.env/bin/python

import torch
import torch.nn as nn
from environments.SquareEnv import SquareEnv
import time
import sys

class Q_NET(nn.Module):
	def __init__(self):
		super(Q_NET, self).__init__()
		self.net = nn.Sequential(
			 nn.Conv2d(3, 8, 3, 2, 1),
			 nn.ReLU(),
			 nn.Conv2d(8, 16, 3, 2, 1),
			 nn.ReLU(),
			 nn.Conv2d(16, 16, 3, 4, 1),
			 nn.ReLU(),
			 nn.Conv2d(16, 1, 3, 4, 1),
			 )
	def forward(self, state):
		return torch.flatten(self.net(state))



device = torch.device("cuda")
env = SquareEnv()
state = torch.tensor(env.init() / 255, dtype=torch.float32, device=device)
state = torch.swapaxes(state, 0, 2)
q_net = Q_NET().to(device)
result = q_net(state)
print(result.size())
