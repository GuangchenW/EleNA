from abc import ABC, abstractmethod

class Strategy(ABC):
	@abstractmethod
	def find_path(self, G, src, dest, max_elevation_gain=False):
		pass