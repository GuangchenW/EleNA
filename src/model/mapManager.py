import osmnx as ox
import networkx as nx
import sys
import os
import requests
import json

DOWNLOAD_FLAG = 'download'
PREVIEW_FLAG = 'preview'
CURRENT_DIRECTORY = os.path.dirname(__file__)

def main():
	"""
	Usage: python mapManager.py -download [place] [-preview]
	"""
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
	"""
	Download map data using OSMnx and save to disk.
	
	Parameters:
	place (str): Name of the area, e.g. Amherst,MA,USA
	preview (boolean): Whether to show preview of map once download completes
	"""
	G = ox.graph_from_place(place, simplify=False, network_type='drive')
	ox.io.save_graphml(G)
	if preview:
		ox.plot.plot_graph(G)
		
def download_evelation(G):
	"""
	Download elevation data using open-evelation and save to disk.
	
	Paramter:
	G (MultiDiGraph): The map of the area
	"""
	nodeId = []
	for node in G.nodes():
		nodeId.append(node)
	
	elevation_map = {}

	pointer = 0
	print(len(nodeId))
	while True:
		points = {}
		points['locations'] = []
		prevPointer = pointer
		for i in range(200):
			if pointer > len(nodeId)-1:
				break
			points['locations'].append({
				'latitude': G._node[nodeId[pointer]]['y'],
				'longitude': G._node[nodeId[pointer]]['x']
			})
			pointer+=1
			print(pointer)
		
		data = json.dumps(points)
		databytes = data.encode('utf-8')
		headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
		response = requests.post('https://api.open-elevation.com/api/v1/lookup', data=databytes, headers=headers)
		if (response.status_code >= 400):
			print('Error: Failed to download elevation data. Status code', response.status_code)
			return
			
		elevation_data = list(map(lambda result : result['elevation'], response.json()['results']))
		for i in range(pointer-prevPointer):
			elevation_map[nodeId[prevPointer+i]] = elevation_data[i]
		if pointer > len(nodeId)-1:
			break
		
	with open(os.path.join(CURRENT_DIRECTORY, './data/elevation.json'), "w") as outfile:
		json.dump(elevation_map, outfile)
		
def get_graph():
	"""
	Load the saved map from disk.
	
	Returns:
	MultiDiGraph, or None if no saved graph exists.
	"""
	if not os.path.exists(os.path.join(CURRENT_DIRECTORY, './data/graph.graphml')):
		raise Exception("Cannot find saved map. Have you downloaded any yet?")
		return None
	
	G = ox.load_graphml(filepath=os.path.join(CURRENT_DIRECTORY, './data/graph.graphml'))
	return G
	
def get_elevation_data():
	"""
	Load the saved elevation data from disk.
	
	Returns:
	dict, or None if no saved data exists.
	"""
	if not os.path.exists(os.path.join(CURRENT_DIRECTORY, './data/elevation.json')):
		raise Exception("Cannot find saved elevation data. Have you downloaded any yet?")
		return None
	
	with open(os.path.join(CURRENT_DIRECTORY, './data/elevation.json'), 'r') as f:
		elevation_data = json.load(f)
	return elevation_data
	
if __name__=='__main__':
	main()