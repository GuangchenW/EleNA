import osmnx as ox
import networkx as nx
import heapq
import math

from src.model.strategy import Strategy

class Dijkstra(Strategy):
	
	def __init__(self):
		self.max_elevation_gain = False
	
	# TODO: Implement dijkstra's from scratch
	def find_path(self, G, src, dest, max_elevation_gain=False):
		self.max_elevation_gain = max_elevation_gain
		source_node = ox.distance.nearest_nodes(G, src[1], src[0])
		destination_node = ox.distance.nearest_nodes(G, dest[1], dest[0])
		
		queue = [(0,(source_node,-1))]
		explored = {}
		
		curr_node = heapq.heappop(queue)
		while not curr_node[1][0] == destination_node:
			print('current node', curr_node[1][0])
			if curr_node[1][0] in explored.keys():
				if len(queue) <= 0:
					print('Path not found')
					return []
				curr_node = heapq.heappop(queue)
			else:
				explored[curr_node[1][0]] = curr_node[1][1]
				self.add_neighbors_to_queue(queue, explored, G, curr_node)
				curr_node = heapq.heappop(queue)
		explored[curr_node[1][0]]=curr_node[1][1]
		

		
		route = [curr_node[1][0]]
		while explored[route[-1]] >= 0:
			route.append(explored[route[-1]])
		route.reverse()
			
		#route = nx.shortest_path(G, source_node, destination_node)
		
		#fig, ax = ox.plot_graph_route(G, route, node_size=1, figsize=(40,40))
		#return list(map(lambda n: (G._node[n]['x'], G._node[n]['y']), route))
		return list(route)
		
	def add_neighbors_to_queue(self, queue, explored, G, curr_node):
		node_id = curr_node[1][0]
		#curr_elevation = self.get_elevation(G, node_id)
		for n in G.neighbors(node_id):
			if n in explored.keys():
				print('continued')
				continue
			distance = min(G.get_edge_data(node_id, n).values(), key=lambda x: x['length'])['length']
			#elevation_gain = self.get_elevation(G, n)-curr_elevation
			#elevation_gain = 0 if elevation_gain < 0 else elevation_gain
			elevation_gain = 0
			heapq.heappush(queue, (self.calculate_edge_weight(distance, elevation_gain)+curr_node[0], (n, node_id)))
	
	def calculate_edge_weight(self, distance, elevation_gain):
		if self.max_elevation_gain:
			return distance/elevation_gain
		else:
			return math.sqrt(distance**2 + elevation_gain**2)