from abc import ABC, abstractmethod

class Strategy(ABC):
	
	@abstractmethod
	def find_path(self, G, src, dest, max_elevation_gain=False):
		"""
		Find a path in the graph that satisfies the parameters.
	
		Parameters:
		G (Multigraph): The graph of the area
		src (latitude, longitude): The starting corrdinate
		dest (latitude, longitude): The destination corrdinate
		max_elevation_gain (boolean): Whether the path should minimize or maximize elevation gain
	
		Returns:
		int[]: A list of node ids
		"""
		pass