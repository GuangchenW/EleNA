import unittest
from src.views.mainGUI import user_input

class TestEleNa(unittest.TestCase):
    
    def test_address_valid(self):
        controller = user_input()
        controller.startLoc = '140 Governors Drive, Amherst, MA 01002'
        controller.endLoc = '31 North Pleasant Street, Amherst, MA 01002'
        controller.confirm_click()
        self.assertEqual(controller.infoLabel, 'Calculating route from 140 Governors Drive, Amherst, MA 01002 to 31 North Pleasant Street, Amherst, MA 01002. (Complete!)')