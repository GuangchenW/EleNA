import osmnx as ox
import networkx as nx
import heapq
import math

from src.model.strategy import Strategy

class Astar(Strategy):
	
	def __init__(self, G, elevation_data):
		self.max_elevation_gain = False
		self.G = G
		self.elevation_data = elevation_data
	
	def find_path(self, source_node, destination_node, max_elevation_gain=False):
		self.max_elevation_gain = max_elevation_gain
		queue = [(self.calculate_heuristic(self.G, source_node, destination_node),(source_node,-1))]
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
				self.add_neighbors_to_queue(queue, explored, self.G, self.elevation_data, curr_node, destination_node)
				curr_node = heapq.heappop(queue)
		explored[curr_node[1][0]]=curr_node[1][1]
		
		print("Number of nodes explored:", len(explored))
		route = [curr_node[1][0]]
		while explored[route[-1]] >= 0:
			route.append(explored[route[-1]])
		route.reverse()
			
		#route = nx.shortest_path(G, source_node, destination_node)
		
		#fig, ax = ox.plot_graph_route(G, route, node_size=1, figsize=(40,40))
		#return list(map(lambda n: (G._node[n]['x'], G._node[n]['y']), route))
		return list(route)
		
	def add_neighbors_to_queue(self, queue, explored, G, elevation_data, curr_node, dest_node_id):
		node_id = curr_node[1][0]
		curr_elevation = self.get_elevation(node_id)
		for n in G.neighbors(node_id):
			if n in explored.keys():
				#print('continued')
				continue
			distance = min(G.get_edge_data(node_id, n).values(), key=lambda x: x['length'])['length']
			elevation_gain = self.get_elevation(n)-curr_elevation
			elevation_gain = 0.1 if elevation_gain <= 0 else elevation_gain
			#elevation_gain = 0
			totalWeight = curr_node[0] - self.calculate_heuristic(G, node_id, dest_node_id) + self.calculate_edge_weight(distance, elevation_gain) + self.calculate_heuristic(G, n, dest_node_id)
			heapq.heappush(queue, (totalWeight, (n, node_id)))
	
	def calculate_edge_weight(self, distance, elevation_gain):
		if self.max_elevation_gain:
			return math.sqrt(distance)/(elevation_gain**2)
		else:
			return distance
			#return math.sqrt(distance**2 + elevation_gain**2)
	
	def calculate_heuristic(self, G, node_id, dest_node_id):
		lat1, lng1 = G._node[node_id]['y'], G._node[node_id]['x']
		lat2, lng2 = G._node[dest_node_id]['y'], G._node[dest_node_id]['x']
		euclidean_dist = ox.distance.great_circle_vec(lat1, lng1, lat2, lng2)
		if self.max_elevation_gain:
			elevation_diff = self.get_elevation(dest_node_id) - self.get_elevation(node_id)
			elevation_diff = 0.1 if elevation_diff <= 0 else elevation_diff
			return math.sqrt(euclidean_dist)/(elevation_diff**2)
		else:
			return euclidean_dist
	
	def get_elevation(self, node_id):
		return self.elevation_data[str(node_id)]