import osmnx as ox
import networkx as nx
import sys
import os
import requests
import json

DOWNLOAD_FLAG = 'download'
PREVIEW_FLAG = 'preview'

def main():
	if len(sys.argv) <= 1:
		print('Requires the name of a place (with no whitespace), e.g. Amherst,MA,USA')
		return
	args = sys.argv[1:]
	
	place = ''
	preview = False
	
	i = 0
	while i < len(args):
		if args[i].startswith('-'):
			flag = args[i][1:]
			i+=1
			if flag == DOWNLOAD_FLAG:
				if i >= len(args):
					print('Error: No place associated with download flag')
					return
				place = args[i]
				i+=1
			elif flag == PREVIEW_FLAG:
				preview = True
	download_graph(place, preview=preview)
	
def download_graph(place, preview=False):
	G = ox.graph_from_place(place, simplify=False, network_type='drive')
	ox.io.save_graphml(G)
	if preview:
		ox.plot.plot_graph(G)
		
def get_graph():
	G = ox.load_graphml(filepath='src/model/data/graph.graphml')
	return G
	
if __name__=='__main__':
	main()