import re
from urllib.parse import quote

from bs4 import BeautifulSoup

import config
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

    @staticmethod
    def get_name():
        return config.ACCU_PROVIDER_NAME

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
