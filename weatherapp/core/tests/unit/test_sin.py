import unittest

from weatherapp.core.providers.sin import SinWeatherProvider
from weatherapp.core import config
from weatherapp.core.app import App


class SINWeatherProviderTestCase(unittest.TestCase):
    """Test Sinoptik weather provider class methods
    """
    def setUp(self):

        self.provider = SinWeatherProvider(app=App)

    def test_SINWeatherProvider_default_values(self):
        """Tests Sinoptik weather provider default values
        """

        self.assertEqual(self.provider.name, 'sin')
        self.assertEqual(self.provider.default_location, 'Lviv')
        self.assertEqual(self.provider.title, 'Sinoptik')
        self.assertEqual(self.provider.default_url, 'https://ua.sinoptik.ua/%D0'
                                                    '%BF%D0%BE%D0%B3%D0%BE%D0'
                                                    '%B4%D0%B0-%D0%BB%D1%8C%D0'
                                                    '%B2%D1%96%D0%B2')

        self.assertEqual(self.provider.name, config.SIN_PROVIDER_NAME)
        self.assertEqual(self.provider.default_location, config.
                         DEFAULT_SIN_LOCATION_NAME)
        self.assertEqual(self.provider.title, config.SIN_PROVIDER_TITLE)
        self.assertEqual(self.provider.default_url, config.
                         DEFAULT_SIN_LOCATION_URL)

        self.assertEqual(self.provider.get_default_location(), config.
                         DEFAULT_SIN_LOCATION_NAME)
        self.assertEqual(self.provider.get_default_url(), config.
                         DEFAULT_SIN_LOCATION_URL)
        self.assertEqual(self.provider.get_name(), config.
                         SIN_PROVIDER_NAME)


if __name__ == '__main__':
    unittest.main()
