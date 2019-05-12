import unittest

from weatherapp.core.providers.rp5 import Rp5WeatherProvider
from weatherapp.core import config
from weatherapp.core.app import App


class Rp5WeatherProviderTestCase(unittest.TestCase):
    """Test Rp5 weather provider class methods
    """
    def setUp(self):

        self.provider = Rp5WeatherProvider(app=App)

    def test_AccuWeatherProvider_default_values(self):
        """Tests Rp5 weather provider default values
        """

        self.assertEqual(self.provider.name, 'rp5')
        self.assertEqual(self.provider.default_location, 'Lviv')
        self.assertEqual(self.provider.title, 'rp5.ua')
        self.assertEqual(self.provider.default_url, 'http://rp5.ua/%D0%9F%D0%BE'
                         '%D0%B3%D0%BE%D0%B4%D0%B0_%D1%83_%D0%9B%D1%8C%D0%B2%D0'
                         '%BE%D0%B2%D1%96,_%D0%9B%D1%8C%D0%B2%D1%96%D0%B2%D1%81'
                         '%D1%8C%D0%BA%D0%B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1'
                                                    '%82%D1%8C')

        self.assertEqual(self.provider.name, config.RP5_PROVIDER_NAME)
        self.assertEqual(self.provider.default_location, config.
                         DEFAULT_RP5_LOCATION_NAME)
        self.assertEqual(self.provider.title, config.RP5_PROVIDER_TITLE)
        self.assertEqual(self.provider.default_url, config.
                         DEFAULT_RP5_LOCATION_URL)

        self.assertEqual(self.provider.get_default_location(), config.
                         DEFAULT_RP5_LOCATION_NAME)
        self.assertEqual(self.provider.get_default_url(), config.
                         DEFAULT_RP5_LOCATION_URL)
        self.assertEqual(self.provider.get_name(), config.
                         RP5_PROVIDER_NAME)


if __name__ == '__main__':
    unittest.main()
