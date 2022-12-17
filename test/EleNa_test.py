import unittest
import osmnx as ox
import networkx as nx
from src.model.pathfinder import Pathfinder
import src.model.mapManager as mapManager
from src.model.dijkstra import Dijkstra
from src.model.Astar import Astar


class TestingModel(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestingModel, self).__init__(*args, **kwargs)
		self.pathfinder = Pathfinder()
		self.G = mapManager.get_map()
		self.elevation_data = mapManager.get_elevation_data()
		self.dijkstra = Dijkstra(self.G, self.elevation_data)
		self.astar = Astar(self.G, self.elevation_data)
		self.addr1 = '277 Triangle Street, Amherst, MA'
		self.addr2 = '112 Eastman Lane, Amherst, MA 01003'
		self.addr3 = '740 N Pleasant St, Amherst, MA 01003'
		self.addr4 = '551 N Pleasant St, Amherst, MA 01003'
		self.addr_out_map = 'whimbrel place, woronora heights, nsw'
		self.addr_weird = 'blah'
		
		addr1_coord = ox.geocoder.geocode(self.addr1)
		addr2_coord = ox.geocoder.geocode(self.addr2)
		addr3_coord = ox.geocoder.geocode(self.addr3)
		addr4_coord = ox.geocoder.geocode(self.addr4)
		
		self.source_node = ox.distance.nearest_nodes(self.G, addr1_coord[1], addr1_coord[0])
		self.source_node2 = ox.distance.nearest_nodes(self.G, addr4_coord[1], addr4_coord[0])
		self.destination_node = ox.distance.nearest_nodes(self.G, addr2_coord[1], addr2_coord[0])
		self.destination_node2 = ox.distance.nearest_nodes(self.G, addr3_coord[1], addr3_coord[0])
	
	def test_pathfinder_source_out_of_map(self):
		self.assertTrue(self.pathfinder.find_path(self.addr_out_map, self.addr1) is None)
	
	def test_pathfinder_destination_out_of_map(self):
		self.assertTrue(self.pathfinder.find_path(self.addr1, self.addr_out_map) is None)
	
	def test_pathfinder_weird_address(self):
		self.assertTrue(self.pathfinder.find_path(self.addr_weird, self.addr_out_map) is None)
	
	def test_pathfinder_faulty_address(self):
		self.assertTrue(self.pathfinder.find_path('112 Eastman Lane, Amherst, CA 01003', self.addr1) is None)
		
	def test_pathfinder_get_source(self):
		self.pathfinder.source = ""
		self.pathfinder.find_path(self.addr1, self.addr2)
		self.assertNotEqual("", self.pathfinder.source)
		
	def test_pathfinder_get_source(self):
		self.pathfinder.destination = ""
		self.pathfinder.find_path(self.addr1, self.addr2)
		self.assertNotEqual("", self.pathfinder.destination)
	
	def test_dijkstra_point_path(self):
		self.pathfinder.set_strategy("dijkstra")
		self.assertTrue(self.pathfinder.find_path(self.addr1,self.addr1) is not None)
		
	def test_dijkstra_normal(self):
		"""
		This is a straight road and the number of nodes on path is obtained from visualization of the graph
		"""
		route = self.dijkstra.find_path(self.source_node2, self.destination_node2)
		self.assertEqual(len(route), 50)
		
	def test_dijkstra_max_elev(self):
		route1 = self.dijkstra.find_path(self.source_node, self.destination_node)
		route2 = self.dijkstra.find_path(self.source_node, self.destination_node, max_elevation_gain=True)
		self.assertNotEqual(route1, route2)
		
	def test_astar_normal(self):
		"""
		This is a straight road and the number of nodes on path is obtained from visualization of the graph
		"""
		route = self.astar.find_path(self.source_node2, self.destination_node2)
		self.assertEqual(len(route), 50)
	
	def test_astar_max_elev(self):
		route1 = self.astar.find_path(self.source_node, self.destination_node)
		route2 = self.astar.find_path(self.source_node, self.destination_node, max_elevation_gain=True)
		self.assertNotEqual(route1, route2)
		
	def test_normal_astar_equal_dijkstar(self):
		route1 = self.dijkstra.find_path(self.source_node2, self.destination_node2)
		route2 = self.astar.find_path(self.source_node2, self.destination_node2)
		self.assertEqual(route1, route2)
		
	if __name__ == '__main__':
		unittest.main()