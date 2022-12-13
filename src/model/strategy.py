from abc import ABC, abstractmethod
import requests
import json

class Strategy(ABC):
	
	@abstractmethod
	def find_path(self, G, src, dest, max_elevation_gain=False):
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
	
	def get_elevation(self, G, node_id):
		"""
		Get the elevation given a node in graph.
		
		Parameters:
		G (Multidigraph): The graph of the area
		node_id (int): The id of the node
		
		Returns:
		float: Elevation
		"""
		longitude = G._node[node_id]['x']
		latitude = G._node[node_id]['y']
		data = requests.get('https://api.open-elevation.com/api/v1/lookup?locations='+str(latitude)+','+str(longitude))
		if data.status_code >= 400:
			print('Error getting elevation for '+str(latitude)+','+str(longitude))
			return None
		
		parsed_data = json.loads(data.text)
		elevation = parsed_data['results'][0]['elevation']
		return elevation