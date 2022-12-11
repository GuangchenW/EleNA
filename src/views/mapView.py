import webbrowser
import folium

class MapView:
    def __init__(self):
        self.start = ()
        self.end = ()
        self.m = None
    
    """
		Render a smooth path based on a computed path.
		
		Parameters:
		start ((longitude, latitude)): start of the route (where the start image will be)
		end ((longitude, latitude)): end of the route (where the end image will be)
        path (JSON string): readily computed path	
	"""
    def render_path(self, start, end, path):
        self.start = (start[1], start[0])
        self.end = end
        folium.GeoJson(path).add_to(self.m)
        self.m = folium.Map(location = self.start, zoom_start=17)
        self.insert_start_image()
        self.insert_end_image()
        self.m.save("map.html")
        webbrowser.open("map.html")

    """
		Inserts a home icon on the start of the path
	"""
    def insert_start_image(self):
        icon = folium.Icon(color="red", icon="glyphicon-home")
        marker = folium.Marker(location=self.start, icon=icon).add_to(self.m)
    
    """
		Inserts a destination icon on the end of the path
	"""
    def insert_end_image(self):
        icon = folium.Icon(color="red", icon="glyphicon-home")
        marker = folium.Marker(location=self.start, icon=icon).add_to(self.m)