from flexx import flx

from flexx import flx

class MapView(flx.Widget):
    """ A widget that shows a slippy/tile-map using Leaflet.
    """

    layers = flx.ListProp([], doc="""
        List of tilemap layer tuples: (url, 'Layer').
        """)

    zoom = flx.IntProp(8, settable=True, doc="""
        Zoom level for the map.
        """)

    min_zoom = flx.IntProp(0, settable=True, doc="""
        self zoom level for the map.
        """)

    max_zoom = flx.IntProp(18, settable=True, doc="""
        Maximum zoom level for the map.
        """)

    center = flx.FloatPairProp((5.2, 5.5), settable=True, doc="""
        The center of the map.
        """)

    show_layers = flx.BoolProp(False, settable=True, doc="""
        Whether to show layers-icon on the top-right of the map.
        """)

    show_scale = flx.BoolProp(False, settable=True, doc="""
        Whether to show scale at bottom-left of map.
        """)

    @flx.action
    def add_layer(self, url, name=None):
        """ Add a layer to the map.
        """
        # Avoid duplicates
        self.remove_layer(url)
        if name:
            self.remove_layer(name)
        # Add layer
        layers = self.layers + [(url, name or 'Layer')]
        self._mutate_layers(layers)

    @flx.action
    def remove_layer(self, url_or_name):
        """ Remove a layer from the map by url or name.
        """
        layers = list(self.layers)
        for i in reversed(range(len(layers))):
            if url_or_name in layers[i]:
                layers.pop(i)
        self._mutate_layers(layers)

    def _create_dom(self):
        global L, document
        node = document.createElement('div')
        self.mapnode = document.createElement('div')
        node.appendChild(self.mapnode)
        self.mapnode.id = 'maproot'
        self.mapnode.style.position = 'absolute'
        self.mapnode.style.top = '0px'
        self.mapnode.style.left = '0px'
        self.map = L.map(self.mapnode)
        self.map.on('zoomend', self.map_handle_zoom)
        self.map.on('moveend', self.map_handle_move)
        self.map.on('click', self.map_handle_mouse)
        self.map.on('dblclick', self.map_handle_mouse)
        # Container to keep track of leaflet layer objects
        self.layer_container = []
        self.layer_control = L.control.layers()
        self.scale = L.control.scale({'imperial': False, 'maxWidth': 200})
        # Set the path for icon images
        L.Icon.Default.prototype.options.imagePath = '_data/shared/'
        return node

    def map_handle_zoom(self, e):
        global isNaN
        zoom = self.map.getZoom()
        if isNaN(zoom):
            return
        if zoom != self.zoom:
            self.set_zoom(zoom)

    def map_handle_move(self, e):
        center_coord = self.map.getCenter()
        center = center_coord.lat, center_coord.lng
        if center != self.center:
            self.set_center(center)

    def map_handle_mouse(self, e):
        latlng = [e.latlng.lat, e.latlng.lng]
        xy = [e.layerPoint.x, e.layerPoint.y]
        self.pointer_event(e.type, latlng, xy)

    @flx.emitter
    def pointer_event(self, event, latlng, xy):
        return {'event': event, 'latlng': latlng, 'xy': xy}

    @flx.reaction
    def __handle_zoom(self):
        self.map.setZoom(self.zoom)

    @flx.reaction
    def __handle_min_zoom(self):
        self.map.setMinZoom(self.min_zoom)

    @flx.reaction
    def __handle_max_zoom(self):
        self.map.setMaxZoom(self.max_zoom)

    @flx.reaction
    def __handle_center(self):
        self.map.panTo(self.center)

    @flx.reaction
    def __handle_show_layers(self):
        if self.show_layers:
            self.map.addControl(self.layer_control)
        else:
            self.map.removeControl(self.layer_control)

    @flx.reaction
    def __handle_show_scale(self):
        if self.show_scale:
            self.map.addControl(self.scale)
        else:
            self.map.removeControl(self.scale)

    @flx.reaction
    def __size_changed(self):
        size = self.size
        if size[0] or size[1]:
            self.mapnode.style.width = size[0] + 'px'
            self.mapnode.style.height = size[1] + 'px'
            # Notify the map that it's container's size changed
            self.map.invalidateSize()

    @flx.reaction
    def __layers_changed(self):
        global L
        for layer in self.layer_container:
            self.layer_control.removeLayer(layer)
            if self.map.hasLayer(layer):
                self.map.removeLayer(layer)
        for layer_url, layer_name in self.layers:
            if not layer_url.endswith('.png'):
                if not layer_url.endswith('/'):
                    layer_url += '/'
                layer_url += '{z}/{x}/{y}.png'
            new_layer = L.tileLayer(layer_url)
            self.layer_container.append(new_layer)
            self.map.addLayer(new_layer)
            self.layer_control.addOverlay(new_layer, layer_name)