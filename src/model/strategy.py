from abc import ABC, abstractmethod
import requests
import json

class Strategy(ABC):
	
	@abstractmethod
	def find_path(self, G, elevation_data, source_node, destination_node, max_elevation_gain=False):
		"""
		Find a path in the graph that satisfies the parameters.
	
		Parameters:
		G (Multidigraph): The graph of the area
		src (latitude, longitude): The starting corrdinate
		dest (latitude, longitude): The destination corrdinate
		max_elevation_gain (boolean): Whether the path should minimize or maximize elevation gain
	
		Returns:
		int[]: A list of node ids
		"""
		pass
		