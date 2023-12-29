import unittest
from app import create_app

class EndpointsTest(unittest.TestCase):

    def setUp(self) -> None:
        app = create_app(config_name='testing')
        self.app = app.test_client()
        self.base_url = 'http://127.0.0.1:5000/'

    def tearDown(self) -> None:
        ...

    def test_can_get_entry_point_template(self):
        response = self.app.get(self.base_url)
 
        print(response.headers, response.status_code)

if __name__ == "__main__":
    unittest.main()