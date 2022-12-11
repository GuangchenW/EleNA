import webbrowser
import folium

class MapView:
    def __init__(self):
        self.start = ()
        self.end = ()
        self.m = None
    
    def render_path(self, start, end, path):
        self.start = (start[1], start[0])
        self.end = end
        folium.GeoJson(path).add_to(self.m)
        self.m = folium.Map(location = self.start, zoom_start=17)
        self.insert_start_image()
        self.insert_end_image()
        self.m.save("map.html")
        webbrowser.open("map.html")

    def insert_start_image(self):
        icon = folium.Icon(color="red", icon="glyphicon-home")
        marker = folium.Marker(location=self.start, icon=icon).add_to(self.m)
    
    def insert_end_image(self):
        icon = folium.Icon(color="red", icon="glyphicon-home")
        marker = folium.Marker(location=self.start, icon=icon).add_to(self.m)