"""Class for rp5.ua provider
"""

from urllib.parse import quote
import sys

from bs4 import BeautifulSoup

from weatherapp.core import config
from weatherapp.core.abstract import WeatherProvider
from weatherapp.core.formatters import TableFormatter


class Rp5WeatherProvider(WeatherProvider):
    """Weather provider for rp5 site.
    """

    name = config.RP5_PROVIDER_NAME
    title = config.RP5_PROVIDER_TITLE

    default_location = config.DEFAULT_RP5_LOCATION_NAME
    default_url = config.DEFAULT_RP5_LOCATION_URL

    @staticmethod
    def get_default_location():
        return config.DEFAULT_RP5_LOCATION_NAME

    @staticmethod
    def get_default_url():
        return config.DEFAULT_RP5_LOCATION_URL

    @staticmethod
    def get_name():
        return config.RP5_PROVIDER_NAME

    def get_rp5_locations(self, locations_url):
        locations_page = self.get_page_source(locations_url)
        soup = BeautifulSoup(locations_page, 'html.parser')

        locations = []
        soup = soup.find('div', class_='countryMap')
        if soup is not None:
            if soup.find_all('b'):
                for location in soup.find_all('b'):
                    url = "http://rp5.ua/" +\
                          quote(location.find('a').attrs['href'])
                    location = location.find('a').text
                    locations.append((location, url))
            elif soup.find_all('h3'):
                for location in soup.find_all('h3'):
                    url = "http://rp5.ua/" + \
                          quote(location.find('a').attrs['href'])
                    location = location.find('a').text
                    locations.append((location, url))
            else:
                for location in soup.find_all('div', class_='city_link'):
                    url = "http://rp5.ua/" + \
                          quote(location.find('a').attrs['href'])
                    location = location.find('a').text
                    locations.append((location, url))

        return locations

    def configurate(self):
        """Performs provider configuration
        """

        locations = self.get_rp5_locations(config.RP5_BROWSE_LOCATIONS)

        provider = self.name
        while locations:
            for index, location in enumerate(locations):
                sys.stdout.write(f'{index + 1}. {location[0]} \n')

            try:
                selected_index = int(input('Please select location: '))
                self.configure_logging()
                self.loger.debug('Got the following number %s', selected_index)
            except ValueError:
                sys.stdout.write('\nYou must enter an integer number!\n')
                raise SystemExit()

            try:
                location = locations[selected_index - 1]
                self.configure_logging()
                self.loger.debug('Got the following location %s', location)
            except IndexError:
                sys.stdout.write('\nThe number you entered is too large!\n')
                raise SystemExit()

            locations = self.get_rp5_locations(location[1])
        WeatherProvider.save_configuration(self, provider, *location)

    @staticmethod
    def get_weather_info(page_content, refresh=False):
        """
        :param page_content:  decoded page source
        :return: dictionary of
        """
        city_page = BeautifulSoup(page_content, 'html.parser')

        weather_info = {}

        temp = city_page.find('span', class_='t_0')
        if temp:
            weather_info['Temp'] = temp.text

        feel_temp = city_page.find('div', class_='ArchiveTempFeeling')
        if feel_temp:
            weather_info['Feel_temp'] = feel_temp.text

        wind_info = city_page.find('div', class_='wv_0')
        if wind_info:
            weather_info['Wind'] = wind_info.text + ' м/с'

        return weather_info
