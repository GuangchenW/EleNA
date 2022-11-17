import osmnx as ox
import networkx as nx

G = ox.graph_from_address('398 N. Sicily Pl., Chandler, Arizona', dist=500, network_type='drive')
ox.plot_graph(G)