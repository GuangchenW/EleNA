from importlib.resources import path
from pathlib import Path
from flexx import flx
from src.model.pathfinder import Pathfinder
from src.views.mapView import MapView


class user_input(flx.PyWidget):
    
    def init(self):
        super().init()

        #three field
        self.startLoc = ''
        self.endLoc = ''
        self.EGain = False
        self.solution = ''
        self.pathfinder = Pathfinder()
        self.map_view = MapView()

        #user interface box
        with flx.VBox():
            with flx.HBox():
                self.start_location = flx.LineEdit(placeholder_text = 'departure..')
                self.end_location = flx.LineEdit(placeholder_text = 'arrival..')
            with flx.VBox():
                self.choice1 = flx.RadioButton(text = 'min Elevation Gain')
                self.choice2 = flx.RadioButton(text = 'max Elevation Gain')
                #self.infoLabel = flx.Label(text = '...')
            with flx.HBox():
                self.resetting = flx.Button(text = 'Reset')
                self.confirming = flx.Button(text = 'confirm')
            with flx.VBox():
                self.infoLabel = flx.Label()
    
    @flx.reaction('resetting.pointer_click')
    def reset_click(self, *events):
        """
        After the user click reset button, all fields in the user interface will be empty. 
        All information will be disregarded and nothing will be saved.
        """
        self.start_location.set_text('')
        self.end_location.set_text('')
        self.choice1.set_checked(False)
        self.choice2.set_checked(False)
        self.infoLabel.set_text('')

    @flx.reaction('confirming.pointer_click')
    def confirm_click(self, *events):
        """
        confirm_click function reasponse to user's click on confirm button. 
        After the user click confirm, the start location, end location, and the elevation gain 
        are set and recorded.
        At the same time, user interface will print the information for start and end location, 
        so for the elevation gain.
        """
        self.confirming.set_disabled(True)
        self.startLoc = self.start_location.text
        self.endLoc = self.end_location.text
        if(self.choice1.checked):
            self.EGain = True
        elif(self.choice2.checked):
            self.EGain = False
        else:
            self.EGain = False
        self.infoLabel.set_text('Calculating route from ' + self.startLoc + ' to ' + self.endLoc + '. (Loading...)')
        self.solution = self.pathfinder.find_path(self.startLoc, self.endLoc)
        self.infoLabel.set_text('Calculating route from ' + self.startLoc + ' to ' + self.endLoc + '. (Complete!)')
        self.confirming.set_disabled(False)
        self.map_view.render_path(self.pathfinder.get_source(), self.pathfinder.get_destination(), self.solution)

    
    def get_start(self):
        """
        Return the start location.
        """
        return self.startLoc

    def get_end(self):
        """
        Return the end location.
        """
        return self.endLoc

    def get_EGain(self):
        """
        return the choice of elevation gain.
        """
        return self.EGain
