from flexx import flx
import os
import sys

from views.mainGUI import user_input

if __name__ == '__main__':
	app = flx.App(user_input)
	app.launch('browser')
	#m = flx.launch(user_input)
	flx.run()