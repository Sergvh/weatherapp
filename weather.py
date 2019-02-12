#!usr/bin/env python

import html
import configparser
import sys
import time
import argparse
import hashlib
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.parse import quote

ACCU_URL = ("https://www.accuweather.com/uk/ua/lviv/324561/weather-forecast/"
            "324561")
RP5_URL = ("http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D1%83_"
           "%D0%9B%D1%8C%D0%B2%D0%BE%D0%B2%D1%96,_%D0%9B%D1%8C%D0%B2%D1%96%D0%"
           "B2%D1%81%D1%8C%D0%BA%D0%B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%"
           "D1%82%D1%8C")

ACCU_BROWSE_LOCETION = "https://www.accuweather.com/uk/browse-locations"
RP5_BROWSE_LOCETION = "http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D" \
                      "0%B2_%D1%81%D0%B2%D1%96%D1%82%D1%96"
GIS_BROWSE_LOCETION = "https://www.gismeteo.ua/ua/catalog/"

CONFIG_LOCATION = 'Location'
CONFIG_FILE = 'weatherapp.ini'

INFO_FILE = 'weather.txt'

CACHE_DIR = '.wappcache'
CACHE_TIME = 300

DEFAULT_NAME = 'Kyiv'
DEFAULT_URL = "https://www.accuweather.com/uk/ua/kyiv/324505/weather-forecast" \
              "/324505 "

PROVIDER = { 'accu': ACCU_BROWSE_LOCETION,
             'rp5': RP5_BROWSE_LOCETION,
             'gis': GIS_BROWSE_LOCETION}

headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64)'}


def get_request_headers():
    return{'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64)'}


def get_accu_locations(locations_url):
    locations_page = get_page_source(locations_url)
    soup = BeautifulSoup(locations_page, 'html.parser')

    locations = []
    for location in soup.find_all('li', class_='drilldown cl'):
        url = location.find('a').attrs['href']
        location = location.find('em').text
        locations.append((location, url))
    return locations


def get_rp5_locations(locations_url):
    locations_page = get_page_source(locations_url)
    soup = BeautifulSoup(locations_page, 'html.parser')

    locations = []
    soup = soup.find('div', class_='countryMap')
    if soup is not None:
        if soup.find_all('b'):
            for location in soup.find_all('b'):
                url = "http://rp5.ua/" + quote(location.find('a').attrs['href'])
                location = location.find('a').text
                locations.append((location, url))
        elif soup.find_all('h3'):
            for location in soup.find_all('h3'):
                url = "http://rp5.ua/" + quote(location.find('a').attrs['href'])
                location = location.find('a').text
                locations.append((location, url))
        else:
            for location in soup.find_all('div', class_='city_link'):
                url = "http://rp5.ua/" + quote(location.find('a').attrs['href'])
                location = location.find('a').text
                locations.append((location, url))

    return locations


def get_gis_locations(locations_url):
    locations_page = get_page_source(locations_url)
    soup = BeautifulSoup(locations_page, 'html.parser')

    locations = []

    divka = soup.find('div', class_='countries wrap')
    if divka:
        print(divka)
        for location in divka.find_all('li'):
            url = "https://www.gismeteo.ua" + location.find('a').attrs['href']
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


LOCATIONS_PROVIDERS = {'accu': get_accu_locations,
                       'rp5': get_rp5_locations,
                       'gis': get_gis_locations}


def get_cache_directory():
    """Path to cache directory
    :returns Path to cache directory in your home directory.
    """
    return Path.home() / CACHE_DIR


def get_configuration_file():
    """Path to configuration file
    :returns Path to configuration file in your home directory.
    """
    return Path.home() / CONFIG_FILE


def get_info_file():
    return Path.home() / INFO_FILE


def get_configuration(provider):

    name = DEFAULT_NAME
    url = DEFAULT_URL
    parser = configparser.ConfigParser()
    parser.read(get_configuration_file())

    if provider in parser.sections():
        config = parser[provider]
        name, url = config['name'], config['url']

    return name, url


def save_configuration(provider, name, url):
    parser = configparser.ConfigParser()
    url = url.replace('%', '%%')
    parser.read(get_configuration_file())
    parser[provider] = {'name': name, 'url': url}
    with open(get_configuration_file(), 'w') as configfile:
        parser.write(configfile)


def configurate(provider):
    locations = LOCATIONS_PROVIDERS[provider](PROVIDER[provider])

    while locations:
        for index, location in enumerate(locations):
            print(f'{index + 1}. {location[0]}')
        selected_index = int(input('Please select location: '))
        location = locations[selected_index - 1]
        locations = LOCATIONS_PROVIDERS[provider](location[1])
    save_configuration(provider, *location)


def get_url_hash(url):
    """Returns generated hash for given url.
    """

    return hashlib.md5(url.encode('utf-8')).hexdigest()


def save_cache(url, page_source):
    """ Save page source data to file
    """
    url_hash = get_url_hash(url)
    cache_dir = get_cache_directory()
    if not cache_dir.exists():
        cache_dir.mkdir(parents=True)

    with (cache_dir / url_hash).open('wb') as cache_file:
        cache_file.write(page_source)


def is_valid(path):
    """Check if current cache is valid.
    """

    return (time.time() - path.stat().st_mtime) < CACHE_TIME


def get_cache(url):
    """Get cache data if any.
    """

    cache = b''
    url_hash = get_url_hash(url)
    cache_dir = get_cache_directory()
    if cache_dir.exists():
        cache_path = cache_dir / url_hash
        if cache_path.exists() and is_valid(cache_path):
            with cache_path.open('rb') as cache_file:
                cache = cache_file.read()

    return cache


def get_page_source(url, refresh=False):
    """
    :param url: site url in str
    :return: decoded source code of html page received from url.
    """

    cache = get_cache(url)
    if cache and not refresh:
        page_source = cache
        print(f"cache for {url}")
    else:
        request = Request(url, headers=get_request_headers())
        page_source = urlopen(request).read()
        save_cache(url, page_source)

    return page_source.decode('utf-8')


def get_tag_content(soup, tag):
    """
    :param soup: decoded page source
    :param tag: string what to find in page content
    :return: generated string with information wich was found after tag
    """
    content = soup.find(attrs={'class': tag})
    return content.text


def get_accu_weather_info(page_content):
    """
    :param soup:  decoded page source
    :param tags: string what to find in page content
    :return:
    """
    city_page = BeautifulSoup(page_content, 'html.parser')
    current_day_section = city_page.find(
        'li', class_='day current first cl')

    weather_info = {'name': 'AccuWeather'}
    if current_day_section:
        current_day_url = current_day_section.find('a').attrs['href']
        if current_day_url:
            current_day_page = get_page_source(current_day_url)
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
                feal_temp = weather_details.find('span', class_='small-temp')
                if feal_temp:
                    weather_info['feal_temp'] = feal_temp.text
                wind_info = weather_details.find_all('li', class_='wind')
                if wind_info:
                    weather_info['wind'] = \
                        ''.join(map(lambda t: t.text.strip(), wind_info))
    return weather_info


def get_rp5_weather_info(page_content):
    """
    :param page_content:  decoded page source
    :return: dictionary of
    """
    city_page = BeautifulSoup(page_content, 'html.parser')

    weather_info = {'Name': 'RP5'}

    temp = city_page.find('span', class_='t_0')
    if temp:
        weather_info['Temp'] = temp.text

    feel_temp = city_page.find('div', class_='ArchiveTempFeeling')
    if feel_temp:
        weather_info['Feel_temp'] = feel_temp.text

    wind_info = city_page.find('div', class_='wv_0')
    if wind_info:
        weather_info['Wind'] = wind_info.text+' м/с'

    return weather_info


def get_gis_weather_info(page_content):
    print('Hello')


def produce_output(city_name, info, provider):
    #print(provider+'\n')
    print(f'{city_name}')
    print(f'_'*20)
    for key, value in info.items():
        print(f'{key}: {html.unescape(value)}')
    print('\n')


def save_data_to_file(provider, info):
    """
    :param info:
    :return:
    """

    with open(get_info_file(), 'w') as info_file:
        for key, value in info.items():
            info_file.write(f'{key}: {html.unescape(value)}\n')

GET_INFO_PROVIDERS = {'accu': get_accu_weather_info,
                      'rp5': get_rp5_weather_info,
                      'gis': get_gis_weather_info}

def get_weather_info(provider, refresh = False):
    city_name, city_url = get_configuration(provider)
    content = get_page_source(city_url, refresh)
    produce_output(city_name, GET_INFO_PROVIDERS[provider](content), provider)
    return GET_INFO_PROVIDERS[provider](content)



def get_all_providers_info():
    """
    :param params:
    :return:
    """
    get_accu_weather_info()
    get_rp5_weather_info()


KNOWN_COMMANDS = {'accu': get_weather_info,
                  'rp5': get_weather_info,
                  '-s': save_data_to_file,
                  '-c': configurate,
                  'all': get_all_providers_info}


def main(argv):
    """ Main entry point
        :argv - must be:
                        'accu' for AccuWeather:
                        'rp5' for RP5
                        'all' for both
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--save',  nargs='?',
                        help="use -s [Service name] for save data "
                        "in file", default='')
    parser.add_argument('-c', '--config', nargs='?',
                        help="use -c [Service name] for configure", default='')
    parser.add_argument('command', help='Service name', nargs='?')
    parser.add_argument('-r', '--refresh', help='Update caches',
                        action='store_true')

    params = parser.parse_args(argv)

    if params.command:
        KNOWN_COMMANDS[params.command](params.command, refresh=params.refresh)
    elif params.save:
        KNOWN_COMMANDS['-s'](params.save,
                             KNOWN_COMMANDS[params.save](params.save))
    elif params.config:
        KNOWN_COMMANDS['-c'](params.config)
    else:
          print('Unknown command provided!')
          sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])
