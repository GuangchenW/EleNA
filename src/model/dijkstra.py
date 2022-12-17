import osmnx as ox
import networkx as nx
import heapq
import math

from src.model.strategy import Strategy

class Dijkstra(Strategy):
	
	def __init__(self, G, elevation_data):
		"""
		Parameters:
		G (MultiDiGraph): Map of the area
		elevation_data (dict): Elevation data of each node on the map
		"""
		self.max_elevation_gain = False
		self.G = G
		self.elevation_data = elevation_data
	
	def find_path(self, source_node, destination_node, max_elevation_gain=False):
		self.max_elevation_gain = max_elevation_gain
		queue = [(0,(source_node,-1))]
		explored = {}
		
		curr_node = heapq.heappop(queue)
		while not curr_node[1][0] == destination_node:
			if curr_node[1][0] in explored.keys():
				if len(queue) <= 0:
					print('Path not found')
					return None
				curr_node = heapq.heappop(queue)
			else:
				explored[curr_node[1][0]] = curr_node[1][1]
				self.add_neighbors_to_queue(queue, explored, self.G, self.elevation_data, curr_node)
				curr_node = heapq.heappop(queue)
		explored[curr_node[1][0]]=curr_node[1][1]
		
		print("Number of nodes explored:", len(explored))
		route = [curr_node[1][0]]
		while explored[route[-1]] >= 0:
			route.append(explored[route[-1]])
		route.reverse()
			
		#route = nx.shortest_path(self.G, source_node, destination_node)
		
		
		#fig, ax = ox.plot_graph_route(G, route, node_size=1, figsize=(40,40))
		return list(route)
		
	def add_neighbors_to_queue(self, queue, explored, G, elevation_data, curr_node):
		node_id = curr_node[1][0]
		curr_elevation = self.get_elevation(node_id)
		for n in G.neighbors(node_id):
			if n in explored.keys():
				continue
			distance = min(G.get_edge_data(node_id, n).values(), key=lambda x: x['length'])['length']
			elevation_gain = self.get_elevation(n)-curr_elevation
			elevation_gain = 0.1 if elevation_gain <= 0 else elevation_gain
			heapq.heappush(queue, (self.calculate_edge_weight(distance, elevation_gain)+curr_node[0], (n, node_id)))
	
	def calculate_edge_weight(self, distance, elevation_gain):
		"""
		Calculate the edge weight based on distance and elevation gain between two nodes.
		
		Parameters:
		distance (float): Distance between two nodes
		elevation_gain (float): Elevation gain between two nodes
		
		Returns:
		(edge_weight)
		"""
		if self.max_elevation_gain:
			return math.sqrt(distance)/(elevation_gain**2)
		else:
			return distance
	
	def get_elevation(self, node_id):
		"""
		Get the elevation of a node on the map.
		
		Parameter:
		node_id (int): ID of the node
		
		Returns:
		(int): Elevation
		"""
		return self.elevation_data[str(node_id)]