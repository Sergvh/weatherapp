import configparser
from pathlib import Path
import hashlib
import time
from urllib.request import urlopen, Request
import re

from urllib.parse import quote

from bs4 import BeautifulSoup

import config


class WeatherProvider:
    """Base weather provider
    """

    def __init__(self, app):
        self.app = app

        location, url = self.get_configuration(self.name)
        self.location = location
        self.url = url

    def get_configuration(self, provider):
        """Returns configured location name and url

        :returns: name and url
        :rtype: tuple
        """

        parser = configparser.ConfigParser()
        parser.read(self.get_configuration_file())

        if provider in parser. sections():
            location_config = parser[provider]
            name, url = location_config['name'], location_config['url']

        return name, url

    def get_configuration_file(self):
        """Path to configuration file

        :returns Path to configuration file in your home directory.
        """
        return Path.home() / config.CONFIG_FILE

    def save_configuration(self, provider, name, url):
        """Save selected location to configuration file

        :param name: city name
        :param type: str

        :param url: Prefered location url
        :param type: str
        """
        parser = configparser.ConfigParser()
        url = url.replace('%', '%%')
        parser.read(self.get_configuration_file())
        parser[provider] = {'name': name, 'url': url}
        with open(self.get_configuration_file(), 'w') as configfile:
            parser.write(configfile)

    def get_request_headers(self):
        """Returns custom headers for url requests.
        """

        return {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64)'}

    def get_url_hash(self, url):
        """Returns generated hash for given url.
        """

        return hashlib.md5(url.encode('utf-8')).hexdigest()

    def save_cache(self, url, page_source):
        """ Save page source data to file
        """
        url_hash = self.get_url_hash(url)
        cache_dir = self.get_cache_directory()
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True)

        with (cache_dir / url_hash).open('wb') as cache_file:
            cache_file.write(page_source)

    def is_valid(self, path):
        """Check if current cache is valid.
        """

        return (time.time() - path.stat().st_mtime) < config.CACHE_TIME

    def get_cache(self, url):
        """Get cache data if any.
        """

        cache = b''
        url_hash = self.get_url_hash(url)
        cache_dir = self.get_cache_directory()
        if cache_dir.exists():
            cache_path = cache_dir / url_hash
            if cache_path.exists() and self.is_valid(cache_path):
                with cache_path.open('rb') as cache_file:
                    cache = cache_file.read()

        return cache

    def get_cache_directory(self):
        """Path to cache directory
        :returns Path to cache directory in your home directory.
        """
        return Path.home() / config.CACHE_DIR

    def get_page_source(self, url, refresh=False):
        """
        :param url: site url in str
        :return: decoded source code of html page received from url.
        """

        cache = self.get_cache(url)
        if cache and not self.app.options.refresh:
            page_source = cache
        else:
            request = Request(url, headers=self.get_request_headers())
            page_source = urlopen(request).read()
            self.save_cache(url, page_source)

        return page_source.decode('utf-8')

    def run(self, refresh=False):
        """Run provider
        """

        content = self.get_page_source(self.url, refresh=refresh)

        return self.get_weather_info(content, refresh=refresh)


class Rp5WeatherProvider(WeatherProvider):
    """Weather provider for rp5 site.
    """

    name = config.RP5_PROVIDER_NAME
    title = config.RP5_PROVIDER_TITLE

    default_location = config.DEFAULT_RP5_LOCATION_NAME
    default_url = config.DEFAULT_RP5_LOCATION_URL

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

    def get_weather_info(self, page_content, refresh=False):
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

    def get_weather_info(self, page_content, refresh=False):
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


class AccuWeatherProvider(WeatherProvider):
    """Weather provider for accuweather site.
    """

    name = config.ACCU_PROVIDER_NAME
    title = config.ACCU_PROVIDER_TITLE

    default_location = config.DEFAULT_ACCU_LOCATION_NAME
    default_url = config.DEFAULT_ACCU_LOCATION_URL

    def get_accu_locations(self, locations_url):
        locations_page = self.get_page_source(locations_url)
        soup = BeautifulSoup(locations_page, 'html.parser')

        locations = []
        for location in soup.find_all('li', class_='drilldown cl'):
            url = location.find('a').attrs['href']
            location = location.find('em').text
            locations.append((location, url))
        return locations

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


class SinWeatherProvider(WeatherProvider):
    """Weather provider for accuweather site.
    """

    name = config.SIN_PROVIDER_NAME
    title = config.SIN_PROVIDER_TITLE

    default_location = config.DEFAULT_SIN_LOCATION_NAME
    default_url = config.DEFAULT_SIN_LOCATION_URL

    def get_sin_locations(self, locations_url):
        locations_page = self.get_page_source(locations_url)
        soup = BeautifulSoup(locations_page, 'html.parser')

        locations = []
        for location in soup.find_all('li', class_='drilldown cl'):
            url = location.find('a').attrs['href']
            location = location.find('em').text
            locations.append((location, url))
        return locations

    def get_weather_info(self, page_content, refresh=False):
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
