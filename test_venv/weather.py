#!usr/bin/python3.7
import html
import sys
import argparse
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

ACCU_URL = "https://www.accuweather.com/uk/ua/lviv/324561/weather-forecast/324561"
RP5_URL = ("http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D1%83_"
           "%D0%9B%D1%8C%D0%B2%D0%BE%D0%B2%D1%96,_%D0%9B%D1%8C%D0%B2%D1%96%D0%"
           "B2%D1%81%D1%8C%D0%BA%D0%B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C")

headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64)'}


def get_request_headers():
    return{'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64)'}


def get_page_source(url):
    """
    :param url: site url in str
    :return: decoded source code of html page received from url.
    """
    request = Request(url, headers=get_request_headers())
    page_source = urlopen(request).read()
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
        'li', class_='night current first cl')

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


def produce_output(info):
    for key, value in info.items():
        print(f'{key}: {html.unescape(value)}')
    print('\n')


def main(argv):
    """ Main entry point
        :argv - must be:
                        'accu' for AccuWeather:
                        'rp5' for RP5
                        'all' for both
    """

    KNOWN_COMMANDS = {'accu': 'AccuWeather', 'rp5': 'RP5', 'all': 'all'}

    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Service name', nargs=1)
    params = parser.parse_args(argv)
    weather_sites = {
        'AccuWeather': ACCU_URL, 'RP5': RP5_URL
    }

    if params.command:
        command = params.command[0]
        if command in KNOWN_COMMANDS:
            if command == 'all':
                print('One moment please\n')
            else:
                weather_sites = {
                    KNOWN_COMMANDS[command]: weather_sites[KNOWN_COMMANDS[command]]
                }
        else:
            print('Unknown command provided!')
            sys.exit(1)

    for name in weather_sites:
        content = get_page_source(weather_sites[name])
        if name == 'AccuWeather':
            produce_output(get_accu_weather_info(content))
        else:
            produce_output(get_rp5_weather_info(content))


if __name__ == '__main__':
    main(sys.argv[1:])
