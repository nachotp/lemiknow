"""
Unittests
To run the tests: `python -m unittest discover -v lemiknow.tests`
"""
import unittest

from lemiknow.desktop_sender import desktop_sender

class TestSenders(unittest.TestCase):

    def test_desktop_sender(self):
        @desktop_sender(title="Test Desktop")
        def train():
            import time
            time.sleep(5)
            return {"loss": 1}
        self.assertEqual(train(), {"loss": 1})

if __name__ == "__main__":
    unittest.main()
