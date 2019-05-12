import unittest

from weatherapp.core.providers.gis import GisWeatherProvider
from weatherapp.core import config
from weatherapp.core.app import App


class GISWeatherProviderTestCase(unittest.TestCase):
    """Test Gismeteo weather provider class methods
    """
    def setUp(self):

        self.provider = GisWeatherProvider(app=App)

    def test_GisWeatherProvider_default_values(self):
        """Tests Gismeteo weather provider default values
        """

        self.assertEqual(self.provider.name, 'gis')
        self.assertEqual(self.provider.default_location, 'Lviv')
        self.assertEqual(self.provider.title, 'Gismeteo')
        self.assertEqual(self.provider.default_url, 'https://www.gismeteo.ua/ua'
                                                    '/weather-lviv-14412/')

        self.assertEqual(self.provider.name, config.GIS_PROVIDER_NAME)
        self.assertEqual(self.provider.default_location, config.
                         DEFAULT_GIS_LOCATION_NAME)
        self.assertEqual(self.provider.title, config.GIS_PROVIDER_TITLE)
        self.assertEqual(self.provider.default_url, config.
                         DEFAULT_GIS_LOCATION_URL)

        self.assertEqual(self.provider.get_default_location(), config.
                         DEFAULT_GIS_LOCATION_NAME)
        self.assertEqual(self.provider.get_default_url(), config.
                         DEFAULT_GIS_LOCATION_URL)
        self.assertEqual(self.provider.get_name(), config.
                         GIS_PROVIDER_NAME)


if __name__ == '__main__':
    unittest.main()
