import osmnx as ox
import networkx as nx

G = ox.graph_from_address('Whimbrel Place, Woronora Heights, NSW', dist=500, network_type='drive')
ox.plot_graph(G)