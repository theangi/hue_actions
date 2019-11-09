import unittest
import configparser
from .hue import Hue, NoLightsFound


class TestHue(unittest.TestCase):
    def setUp(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.assertIsNotNone(self.config)

    def test_config(self):
        with self.assertRaises(KeyError):
            _ = self.config['bridge_ip_address']
            _ = self.config['hue_user']

        self.assertTrue('ALL' in self.config)
        self.assertIsNotNone(self.config['ALL']['bridge_ip_address'])
        self.assertIsNotNone(self.config['ALL']['hue_user'])

    def test_get_all_lights(self):
        hue = Hue(None, None)

        hue.base_url = f'http://{ip}/api/{user}'

        with self.assertRaises(NoLightsFound):
            hue._get_all_lights()

        with self.assertRaises(NoLightsFound):
            hue._get_all_lights()
