import unittest
import json
from urllib.request import urlopen

BASE_URL = "http://127.0.0.1:8000"

class TestPathSnapAPI(unittest.TestCase):

    def test_home(self):
        data = json.loads(urlopen(BASE_URL).read())
        self.assertEqual(data["message"], "PathSnap API is running")

    def test_health(self):
        data = json.loads(urlopen(BASE_URL + "/health").read())
        self.assertEqual(data["status"], "healthy")

    def test_route(self):
        data = json.loads(urlopen(BASE_URL + "/route").read())
        self.assertGreater(data["total_points"], 0)

if __name__ == "__main__":
    unittest.main()
