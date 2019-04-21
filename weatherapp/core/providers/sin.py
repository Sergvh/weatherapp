"""Class for sinoptik.ua provider
"""

from bs4 import BeautifulSoup

from weatherapp.core import config
from weatherapp.core.abstract import WeatherProvider


class SinWeatherProvider(WeatherProvider):
    """Weather provider for accuweather site.
    """

    name = config.SIN_PROVIDER_NAME
    title = config.SIN_PROVIDER_TITLE

    default_location = config.DEFAULT_SIN_LOCATION_NAME
    default_url = config.DEFAULT_SIN_LOCATION_URL

    @staticmethod
    def get_default_location():
        return config.DEFAULT_SIN_LOCATION_NAME

    @staticmethod
    def get_default_url():
        return config.DEFAULT_SIN_LOCATION_URL

    @staticmethod
    def get_name():
        return config.SIN_PROVIDER_NAME

    def get_sin_locations(self, locations_url):
        locations_page = self.get_page_source(locations_url)
        soup = BeautifulSoup(locations_page, 'html.parser')

        locations = []
        for location in soup.find_all('li', class_='drilldown cl'):
            url = location.find('a').attrs['href']
            location = location.find('em').text
            locations.append((location, url))
        return locations

    def configurate(self):
        """Performs provider configuration
        """
        locations = self.get_sin_locations(config.SIN_BROWSE_LOCATIONS)

        provider = self.name
        while locations:
            for index, location in enumerate(locations):
                print(f'{index + 1}. {location[0]}')

            try:
                selected_index = int(input('Please select location: '))
                self.configure_logging()
                self.loger.debug('Got the following number %s', selected_index)
            except ValueError:
                print('\nYou must enter an integer number!\n')
                raise SystemExit()

            try:
                location = locations[selected_index - 1]
                self.configure_logging()
                self.loger.debug('Got the following location %s', location)
            except IndexError:
                print('\nThe number you entered is too large!\n')
                raise SystemExit()

            locations = self.get_sin_locations(location[1])
        WeatherProvider.save_configuration(self, provider, *location)

    @staticmethod
    def get_weather_info(page_content, refresh=False):
        """
        :param page_content:  html page source
        :return:
        """
        city_page = BeautifulSoup(page_content, 'html.parser')
        city_page = city_page.find('div', class_='wMain clearfix')

        weather_info = {}

        temp = city_page.find('p', class_='today-temp')
        if temp:
            weather_info['Temp'] = temp.text

        feal_temp = city_page.find('tr', class_='temperatureSens')
        if feal_temp:
            feal_temp = feal_temp.find('td', class_='p5')
            if feal_temp:
                weather_info['Feal_Temp'] = feal_temp.text

        condition = city_page.find('tr', class_='img weatherIcoS')
        if condition:
            weather_info['Condition'] = condition.find('div').attrs['title']

        wind_info = city_page.find('div', class_='Tooltip wind wind-W')
        if wind_info:
            weather_info['Wind'] = wind_info.text + ' м/с'
        return weather_info
