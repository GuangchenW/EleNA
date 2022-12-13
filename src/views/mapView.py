import webbrowser
import folium

class MapView:
    def __init__(self):
        self.start = ()
        self.end = ()
        self.m = None
    
    def render_path(self, start, end, path):
        """
        Render a smooth path based on a computed path.
        
        Parameters:
        start ((longitude, latitude)): start of the route (where the start image will be)
        end ((longitude, latitude)): end of the route (where the end image will be)
        path (JSON string): readily computed path   
        """
        self.start = (start[1], start[0])
        self.end = end
        self.m = folium.Map(location = self.start, zoom_start=17)
        folium.GeoJson(path).add_to(self.m)
        self.insert_start_image()
        self.insert_end_image()
        self.m.save("map.html")
        webbrowser.open("map.html", new=2)

    def insert_start_image(self):
        """
        Inserts a home icon on the start of the path
        """
        icon = folium.Icon(color="red", icon="glyphicon-home")
        marker = folium.Marker(location=self.start, icon=icon).add_to(self.m)
    
    def insert_end_image(self):
        """
        Inserts a destination icon on the end of the path
        """
        icon = folium.Icon(color="red", icon="glyphicon-home")
        marker = folium.Marker(location=self.start, icon=icon).add_to(self.m)