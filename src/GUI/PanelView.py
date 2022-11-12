from flexx import flx

class PanelView(flx.Widget):

    def init(self):
        with flx.HBox():
            self.leaflet = PanelView(
                flex=1,
                center=(52, 4.1),
                zoom=12,
                show_scale=lambda: self.cbs.checked,
                show_layers=lambda: self.cbl.checked,
            )
            with flx.VBox():
                self.btna = flx.Button(text='Add SeaMap')
                self.btnr = flx.Button(text='Remove SeaMap')
                self.cbs = flx.CheckBox(text='Show scale')
                self.cbl = flx.CheckBox(text='Show layers')
                self.list = flx.VBox()
                flx.Widget(flex=1)

        self.leaflet.add_layer('http://a.tile.openstreetmap.org/', 'OpenStreetMap')

    @flx.reaction('btna.pointer_click')
    def handle_seamap_add(self, *events):
        self.leaflet.add_layer('http://t1.openseamap.org/seamark/', 'OpenSeaMap')

    @flx.reaction('btnr.pointer_click')
    def handle_seamap_remove(self, *events):
        self.leaflet.remove_layer('http://t1.openseamap.org/seamark/', 'OpenSeaMap')

    # @flx.reaction('cbs.checked', 'cbl.checked')
    # def handle_checkboxes(self, *events):
    #     self.leaflet.set_show_scale(self.cbs.checked
    #     self.leaflet.show_layers = self.cbl.checked

    @flx.reaction('leaflet.pointer_event')
    def handle_leaflet_mouse(self, *events):
        global L
        ev = events[-1]
        latlng = tuple(ev['latlng'])
        flx.Label(text='%f, %f' % (int(100*latlng[0])/100, int(100*latlng[1])/100),
                       parent=self.list)
        latlng = tuple(ev['latlng'])
        if ev['event'] == 'click':
            m = L.marker(ev['latlng'])
            m.bindTooltip('%f, %f' % (latlng[0], latlng[1]))
            m.addTo(self.leaflet.map)