import osmnx as ox
from model.dijkstra import Dijkstra
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
		self.source = (G[1][1], G[1][0])
		self.destination = (H[1], H[0])
		path = self.strategy.find_path(G[0], G[1], H, max_elevation_gain)
		
		features = []
		features.append(Feature(geometry = LineString(path)))
		return ('%s' % FeatureCollection(features))
		
	# Returns: tuple containing coordinate (long, lat)
	def get_source(self):
		return self.source
		
	# Returns: tuple containing coordinate (long, lat)
	def get_destination(self):
		return self.destination
		
	def set_strategy(self, strategy):
		self.strategy = strategy
		
#p = Pathfinder()
#p.find_path('Whimbrel Place, Woronora Heights, NSW','Pelican Place, Woronora Heights, NSW')
#print(p.get_source())
#for n in p.find_path('Whimbrel Place, Woronora Heights, NSW','Pelican Place, Woronora Heights, NSW'):
#	print(n)