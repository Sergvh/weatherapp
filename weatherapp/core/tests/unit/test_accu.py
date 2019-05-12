import unittest

from weatherapp.core.providers.accu import AccuWeatherProvider
from weatherapp.core import config
from weatherapp.core.app import App


class AccuWeatherProviderTestCase(unittest.TestCase):
    """Test AccuWeatherProvider class methods
    """
    def setUp(self):

        self.provider = AccuWeatherProvider(app=App)

    def test_AccuWeatherProvider_default_values(self):
        """Tests AccuWeatherprovider default values
        """

        self.assertEqual(self.provider.name, 'accu')
        self.assertEqual(self.provider.default_location, 'Lviv')
        self.assertEqual(self.provider.title, 'AccuWeather')
        self.assertEqual(self.provider.default_url, 'https://www.accuweather.c'
                                                    'om/uk/ua/lviv/324561/'
                                                    'weather-forecast/324561')

        self.assertEqual(self.provider.name, config.ACCU_PROVIDER_NAME)
        self.assertEqual(self.provider.default_location, config.
                         DEFAULT_ACCU_LOCATION_NAME)
        self.assertEqual(self.provider.title, config.ACCU_PROVIDER_TITLE)
        self.assertEqual(self.provider.default_url, config.
                         DEFAULT_ACCU_LOCATION_URL)

        self.assertEqual(self.provider.get_default_location(), config.
                         DEFAULT_ACCU_LOCATION_NAME)
        self.assertEqual(self.provider.get_default_url(), config.
                         DEFAULT_ACCU_LOCATION_URL)
        self.assertEqual(self.provider.get_name(), config.
                         ACCU_PROVIDER_NAME)


if __name__ == '__main__':
    unittest.main()
