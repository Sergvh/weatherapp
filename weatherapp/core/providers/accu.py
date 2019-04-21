"""Class for accuweather.com provider
"""

import re

from bs4 import BeautifulSoup

from weatherapp.core import config
from weatherapp.core.abstract import WeatherProvider


class AccuWeatherProvider(WeatherProvider):
    """Weather provider for accuweather site.
    """

    name = config.ACCU_PROVIDER_NAME
    title = config.ACCU_PROVIDER_TITLE

    default_location = config.DEFAULT_ACCU_LOCATION_NAME
    default_url = config.DEFAULT_ACCU_LOCATION_URL

    @staticmethod
    def get_default_location():
        return config.DEFAULT_ACCU_LOCATION_NAME

    @staticmethod
    def get_default_url():
        return config.DEFAULT_ACCU_LOCATION_URL

    def get_name(self):
        return self.name

    def get_accu_locations(self, locations_url):
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
        locations = self.get_accu_locations(config.ACCU_BROWSE_LOCATIONS)

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

            locations = self.get_accu_locations(location[1])

        WeatherProvider.save_configuration(self, provider, *location)

    def get_weather_info(self, page_content, refresh=False):
        """
        :param page_content:  html page source
        :return:
        """
        city_page = BeautifulSoup(page_content, 'html.parser')
        current_day_section = city_page.find(
            'li', class_=re.compile('(day|night) current first cl'))

        weather_info = {}
        if current_day_section:
            current_day_url = current_day_section.find('a').attrs['href']
            if current_day_url:
                current_day_page = self.get_page_source(current_day_url)
                if current_day_page:
                    current_day = \
                        BeautifulSoup(current_day_page, 'html.parser')
                    weather_details = \
                        current_day.find('div', attrs={'id': 'detail-now'})
                    condition = weather_details.find('span', class_='cond')
                    if condition:
                        weather_info['condition'] = condition.text
                    temp = weather_details.find('span', class_='large-temp')
                    if temp:
                        weather_info['temp'] = temp.text
                    feal_temp = weather_details.find('span',
                                                     class_='small-temp')
                    if feal_temp:
                        weather_info['feal_temp'] = feal_temp.text
                    wind_info = weather_details.find_all('li', class_='wind')
                    if wind_info:
                        weather_info['wind'] = \
                            ''.join(map(lambda t: t.text.strip(), wind_info))
        return weather_info

