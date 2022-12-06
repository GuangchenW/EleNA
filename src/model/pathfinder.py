import osmnx as ox
from .dijkstra import Dijkstra
from geojson import Feature, FeatureCollection, LineString

class Pathfinder:
	def __init__(self):
		self.strategy = Dijkstra()
		self.source = ""
		self.destination = ""
	
	# Returns: json string containing list of coordinates (long, lat)
	def find_path(self, src, dest, path_type='drive', max_elevation_gain=False):
		# TODO: use geopandas to to geoencoding
		G = ox.graph_from_address(src, dist=500, network_type=path_type, return_coords=True, simplify=True)
		H = ox.geocoder.geocode(dest)
		#print(H)
		path = self.strategy.find_path(G[0], G[1], H, max_elevation_gain)
		path_coords = self.construct_path(G[0], path)
		
		self.source = path_coords[0]
		self.destination = path_coords[-1]
		
		features = []
		features.append(Feature(geometry = LineString(path_coords)))
		return ('%s' % FeatureCollection(features))
	
	# Construct a smooth path based on a list of node ids
	def construct_path(self, G, route):
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
				if (lines[-1] != (x1, y1)):
					lines.append((x1, y1))
				lines.append((x2, y2))
		return lines
	
	# Returns: tuple containing coordinate (long, lat)
	def get_source(self):
		return self.source
		
	# Returns: tuple containing coordinate (long, lat)
	def get_destination(self):
		return self.destination
		
	def set_strategy(self, strategy):
		self.strategy = strategy
		
p = Pathfinder()
p.find_path('Whimbrel Place, Woronora Heights, NSW','Pelican Place, Woronora Heights, NSW')
#print(p.get_source())
#for n in p.find_path('Whimbrel Place, Woronora Heights, NSW','Pelican Place, Woronora Heights, NSW'):
#	print(n)