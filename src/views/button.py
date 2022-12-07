from flexx import flx

class user_input(flx.Widget):
    #max choice value 0 when reset, value 1 when maximizing latitude, value 2 when maximizing longitude
    maxChoice = flx.StringProp('', settable = True)
    
    def init(self):
        super().init()
        with flx.VBox():
            with flx.HBox():
                self.start_location = flx.LineEdit(placeholder_text = 'departure..')
                self.end_location = flx.LineEdit(placeholder_text = 'arrival..')
                self.locationLabel = flx.Label(text = '...')
            with flx.VBox():
                self.choice1 = flx.RadioButton(text = 'max latitude')
                self.choice2 = flx.RadioButton(text = 'max longitude')
                self.choiceLabel = flx.Label(text = '...')
            with flx.HBox():
                
                self.resetting = flx.Button(text = 'Reset')
                self.confirming = flx.Button(text = 'confirm')
    
    @flx.reaction('start_location.text','end_location.text')
    def get_location(self, *events):
        #self.set_departLoc(self.start_location.text);
        #self.set_endLoc(self.end_location.text);
        self.label.set_text('Depart from ' + self.start_location.text + ', ' + 'and arrive at ' + self.end_location.text +', ')
    
    @flx.reaction('choice1.checked')
    def choice1_clicked(self, *events):
        self.set_maxChoice(2)
        #self.choice2.set_disabled(True)
        self.label.set_text('Depart from ' + self.start_location.text + ', ' + 'and arrive at ' + self.end_location.text +', ' + 'maximizing lat')

    @flx.reaction('choice2.checked')
    def choice1_clicked(self, *events):
        self.set_maxChoice(2)
        #self.choice1.set_disabled(True)
        self.label.set_text('Depart from ' + self.start_location.text + ', ' + 'and arrive at ' + self.end_location.text +', ' + 'maximizing longitude')
    
    @flx.reaction('resetting.pointer_click')
    def reset_click(self, *events):
        self.set_maxChoice(0)
        self.start_location.set_text('')
        self.end_location.set_text('')
        self.choice1.set_checked(False)
        self.choice2.set_checked(False)
        self.label.set_text('')


    #@flx.reaction('confirming.pointer_click')
   # def confirming_click(self, *events):
     #   return 

if __name__ == '__main__':
    m = flx.launch(user_input)
    flx.run()