import osmnx as ox
import networkx as nx

from src.model.strategy import Strategy

class Dijkstra(Strategy):
	# TODO: Implement dijkstra's from scratch
	def find_path(self, G, src, dest, max_elevation_gain=False):
		source_node = ox.distance.nearest_nodes(G, src[1], src[0])
		destination_node = ox.distance.nearest_nodes(G, dest[1], dest[0])
		print(self.get_elevation(G, src[0], src[1]))
		route = nx.shortest_path(G, source_node, destination_node)
		
		#fig, ax = ox.plot_graph_route(G, route, node_size=1, figsize=(40,40))
		#return list(map(lambda n: (G._node[n]['x'], G._node[n]['y']), route))
		return route
		
	