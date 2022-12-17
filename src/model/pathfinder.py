import osmnx as ox

import src.model.mapManager as mapManager
from src.model.dijkstra import Dijkstra
from src.model.Astar import Astar
from geojson import Feature, FeatureCollection, LineString

class Pathfinder:
	def __init__(self):
		self.map = mapManager.get_map()
		self.elevation_data = mapManager.get_elevation_data()
		self.strategy = Dijkstra(self.map, self.elevation_data)
		self.source = ""
		self.destination = ""
	
	def find_path(self, src, dest, path_type='drive', max_elevation_gain=False):
		"""
		Find a path given the start and end point and the appropriate parameters.
		
		Parameters:
		src (str): The starting address
		dest (str): The destination address
		path_type (str): The type of transportation
		max_elevation_gain (boolean): Whether the path should minimize or maximize elevation gain
		
		Returns:
		string: json string containing list of coordinates (long, lat) as feature collection.
		"""
		
		G = self.map
		try:
			src = ox.geocoder.geocode(src)
			dest = ox.geocoder.geocode(dest)
		except ValueError as ve:
			print("Cannot geocode addresses")
			return None
		
		source_node, source_error = ox.distance.nearest_nodes(G, src[1], src[0], return_dist=True)
		destination_node, destination_error = ox.distance.nearest_nodes(G, dest[1], dest[0], return_dist=True)
		
		if source_error > 400:
			print("Cannot find a point on map close to the starting address")
			return None
		if destination_error > 400:
			print("Cannot find a point on map close to the starting address")
			return None

		path = self.strategy.find_path(source_node, destination_node, max_elevation_gain)
		if path is None or len(path) < 1:
			print('Cannot find path')
			return None
		print('Path length', len(path))
		path_coords = self.construct_path(G, path)
		
		self.source = path_coords[0]
		self.destination = path_coords[-1]
		
		features = []
		features.append(Feature(geometry = LineString(path_coords)))
		return ('%s' % FeatureCollection(features))
	
	# Reference: https://towardsdatascience.com/find-and-plot-your-optimal-path-using-plotly-and-networkx-in-python-17e75387b873
	def construct_path(self, G, route):
		"""
		Construct a smooth path based on a list of node ids.
		
		Parameters:
		G (Multigraph): The graph of the area
		route (int[]): The list of node ids representing the route
		
		Returns:
		(logitude, latitude)[]: A list of coordinates representing the path.
		"""
		
		if len(route) == 1:
			return [(G._node[route[0]]['y'],G._node[route[0]]['x'])]
		
		edge_nodes = list(zip(route[:-1], route[1:]))
		lines = []
		for u, v in edge_nodes:
			# if there are parallel edges, select the shortest in length
			data = min(G.get_edge_data(u, v).values(), key=lambda x: x['length'])
			# if it has a geometry attribute
			if 'geometry' in data:
				# add them to the list of lines to plot
				xs, ys = data['geometry'].xy
				for coord in zip(xs, ys):
					lines.append(coord)
			else:
				# if it doesn't have a geometry attribute,
				# then the edge is a straight line from node to node
				x1 = G.nodes[u]['x']
				y1 = G.nodes[u]['y']
				x2 = G.nodes[v]['x']
				y2 = G.nodes[v]['y']
				if len(lines) <= 0 or lines[-1] != (x1, y1):
					lines.append((x1, y1))
				lines.append((x2, y2))
		return lines
	
	def get_source(self):
		"""
		Returns:
		(long, lat): The coordinate tof the starting point of the last path found.
		"""
		return self.source
		
	def get_destination(self):
		"""
		Returns:
		(long, lat): The coordinate tof the destination point of the last path found.
		"""
		return self.destination
		
	def set_strategy(self, strategy):
		"""
		Set the pathfinding strategy for this pathfinder.
		
		Parameters:
		strategy (str): The pathfinding strategy to be used.
		"""
		if (strategy == 'astar'):
			self.strategy = Astar(self.map, self.elevation_data)
		else:
			self.strategy = Dijkstra(self.map, self.elevation_data)
			

if __name__=='__main__':
	p = Pathfinder()
	p.find_path('277 Triangle Street, Amherst, MA 01002','112 Eastman Lane, Amherst, MA 01003', max_elevation_gain=False)
	#print(ox.geocoder.geocode('50'))
	#print(p.get_source())
	pass