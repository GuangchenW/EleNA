from abc import ABC, abstractmethod

class Strategy(ABC):
	
	# Returns a list of node ids representing the path
	@abstractmethod
	def find_path(self, G, src, dest, max_elevation_gain=False):
		pass