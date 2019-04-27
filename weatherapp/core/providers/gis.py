"""Class for gismeteo.ua provider
"""

from bs4 import BeautifulSoup
import sys

from weatherapp.core import config
from weatherapp.core.abstract import WeatherProvider


class GisWeatherProvider(WeatherProvider):
    """Weather provider for gismeteo site.
    """

    name = config.GIS_PROVIDER_NAME
    title = config.GIS_PROVIDER_TITLE

    default_location = config.DEFAULT_GIS_LOCATION_NAME
    default_url = config.DEFAULT_GIS_LOCATION_URL

    @staticmethod
    def get_default_location():
        return config.DEFAULT_GIS_LOCATION_NAME

    @staticmethod
    def get_default_url():
        return config.DEFAULT_GIS_LOCATION_URL

    @staticmethod
    def get_name():
        return config.GIS_PROVIDER_NAME

    def get_gis_locations(self, locations_url):
        locations_page = self.get_page_source(locations_url)
        soup = BeautifulSoup(locations_page, 'html.parser')

        locations = []

        divka = soup.find('div', class_='countries wrap')
        if divka:
            for location in divka.find_all('li'):
                url = "https://www.gismeteo.ua" + location.find('a').attrs[
                    'href']
                location = location.find('a').text
                locations.append((location, url))
        else:
            divka = soup.find('div', class_='districts subregions wrap')
            if divka:
                for location in divka.find_all('li'):
                    url = "https://www.gismeteo.ua" + \
                          location.find('a').attrs['href']
                    location = location.find('a').text
                    locations.append((location, url))
            else:
                divka = soup.find('div', class_='subregions wrap')
                if divka:
                    for location in divka.find_all('li'):
                        url = "https://www.gismeteo.ua" + \
                              location.find('a').attrs['href']
                        location = location.find('a').text
                        locations.append((location, url))

        return locations

    def configurate(self):
        """Performs provider configuration
        """
        locations = self.get_gis_locations(config.GIS_BROWSE_LOCATIONS)

        provider = self.name
        while locations:
            for index, location in enumerate(locations):
                sys.stdout.write(f'{index + 1}. {location[0]}\n')

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

            locations = self.get_gis_locations(location[1])
        WeatherProvider.save_configuration(self, provider, *location)

    @staticmethod
    def get_weather_info(page_content, refresh=False):
        """
        :param page_content:  decoded page source
        :return: dictionary of
        """
        city_page = BeautifulSoup(page_content, 'html.parser')
        city_page = city_page.find('div', class_='section higher')

        weather_info = {}

        temp = city_page.find('dd', class_='value m_temp c')
        if temp:
            weather_info['Temp'] = temp.text + '°C'

        pressure = city_page.find('dd', class_='value m_press torr')
        if pressure:
            weather_info['Pressure'] = pressure.text + 'мм рт. ст.'

        wind_info = city_page.find('dd', class_='value m_wind ms')
        if wind_info:
            weather_info['Wind'] = wind_info.text + ' м/с'

        return weather_info
