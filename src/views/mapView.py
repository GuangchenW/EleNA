import folium
from folium import IFrame
import os
import base64
from model.pathfinder import Pathfinder

class mapView:
    def __init__(self):
        path = Pathfinder()
        self.solution = path.find_path('Whimbrel Place, Woronora Heights, NSW','Pelican Place, Woronora Heights, NSW')
        self.m = folium.Map(location = path.get_source(), zoom_start=17)
    
    def render_path(self):
        folium.GeoJson(self.solution).add_to(self.m)
        self.m.save("index.html")