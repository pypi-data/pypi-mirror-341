import unittest
from cvc import *
class Test(unittest.TestCase):
    def test_getCourseIDsBySearch(self):
        #valid search with C_ID
        getCourseIDsBySearch("santa monica", "comp132", "", "")
        #valid search with course symbol
        getCourseContentByID(getCourseIDsBySearch("Santa Monica College", "", "CS20B", "")[0])
        #valid search with course name
        getCourseContentByID(getCourseIDsBySearch("Santa Monica College", "", "", "Data Structures with Java")[0])
        #valid search with all info
        getCourseContentByID(getCourseIDsBySearch("Santa Monica College", "COMP132", "CS20B", "Data Structures with Java")[0])
        try:
            ids = getCourseIDsBySearch("fake school","","","")
            if len(ids) > 0:
                raise ValueError("Invalid info retrieved")
        except ValueError:
            self.fail()
if __name__ == '__main__':
    unittest.main()
