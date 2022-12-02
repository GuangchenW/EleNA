import folium
from folium import IFrame
import os
import base64
from model.pathfinder import Pathfinder

class mapView:
    def __init__(self):
        path = Pathfinder()
        self.solution = path.find_path('Whimbrel Place, Woronora Heights, NSW','Pelican Place, Woronora Heights, NSW')
        self.start = (path.get_source()[1], path.get_source()[0])
        self.m = folium.Map(location = self.start, zoom_start=17)
    
    def render_path(self):
        folium.GeoJson(self.solution).add_to(self.m)
        self.m.save("index.html")

    def insert_start_image(self):
        icon1 = folium.Icon(color="red", icon="glyphicon-home")
        marker1 = folium.Marker(location=self.start, icon=icon1).add_to(self.m)