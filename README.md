# EleNA
Collaboration Project for CS 520

### Use pipenv
1. Navigate to project root directory
2. Enter "pipenv shell" in command line to start new virtual shell session
3. Use command "pipenv install" to install existing dependencies and dependencies you want to include (DO NOT modify PipFile.lock directly!)
3. Enter "exit" to exit pipenv
4. To run the program, while in your virtual environment, enter "python3 src/main.py"

***FEATURES***
1. Provides user with an interface to enter start and end addresses and to either maximize or minimize total  elevation gain. User also has access to a confirm button and reset button.
2. calculates the best path based on user preference of elevation gain.
3. renders path onto folium map and displays map on a separate tab.

***Assumptions and limitations***
1. User must enter exact addresses in full (no abreviations), and must include city and state.
2. Addresses must be within the Amherst area.