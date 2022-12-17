# EleNA
Collaboration Project for CS 520

#### Use pipenv
1. Navigate to project root directory
2. Enter "pipenv shell" in command line to start new virtual shell session
3. Use command "pipenv install" to install dependencies (DO NOT modify PipFile.lock directly!)
4. Enter "exit" to exit pipenv

#### Documentation
1. Use the command "pydoc -w [module]" to generate documentations

#### Testing
1. Use the command "python -m unittest [testclass]" to test the software

#### How to run
1. Navigate to the root directory of the project
2. While in the virtual environment, enter "python3 src/main.py" in the terminal
3. The application should open in a browser
4. To quit the application, simply close the window

***FEATURES***
1. Provides user with an interface to enter start and end addresses and to either maximize or minimize total  elevation gain. User also has access to a confirm button and reset button.
2. calculates the best path based on user preference of elevation gain.
3. renders path onto folium map and displays map on a separate tab.

***Assumptions and limitations***
1. User must enter exact addresses in full (no abreviations), and must include city and state.
2. Addresses must be within the configured map (Amherst by default) area.

***Advanced configurations***
Run mapManager.py with the -download flag to configure the application to a different geographic area.
(WARNING: existing map and elevation data will be overridden)