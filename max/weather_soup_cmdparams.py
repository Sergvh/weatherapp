#!usr/bin/python3.6
import html
import sys
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request

ACCU_URL = "https://www.accuweather.com/uk/ua/lviv/324561/weather-forecast/324561"
RP5_URL = ("http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D1%83_"
           "%D0%9B%D1%8C%D0%B2%D0%BE%D0%B2%D1%96,_%D0%9B%D1%8C%D0%B2%D1%96%D0%"
           "B2%D1%81%D1%8C%D0%BA%D0%B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C")

headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64)'}

ACCU_TAGS = ('large-temp', 'cond')
RP5_TAGS = ('t_0', 'ArchiveTempFeeling')


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


def get_weather_info(soup, tags):
    """
    :param soup:  decoded page source
    :param tags: string what to find in page content
    :return:
    """
    return tuple([get_tag_content(soup, tag) for tag in tags])


def produce_output(provider_name, temp, condition):
    print(f'\n {provider_name}\n')
    print(f'Temperature: {html.unescape(temp)}\n')
    print(f'Condition: {html.unescape(condition)}\n')


def main(n):
    """ Main entry point
        :n - must be:
                        1 for AccuWeather:
                        2 for RP5
                        0 for both
    """
    if n == '1':
        weather_sites = {'AccuWeather': (ACCU_URL, ACCU_TAGS)}
    elif n == '2':
        weather_sites = {'RP5': (RP5_URL, RP5_TAGS)}
    else:
        weather_sites = {'AccuWeather': (ACCU_URL, ACCU_TAGS),
                     'RP5': (RP5_URL, RP5_TAGS)}

    for name in weather_sites:
        url, tags = weather_sites[name]
        content = get_page_source(url)
        soup = bs(content, 'html.parser')
        temp, condition = get_weather_info(soup, tags)
        produce_output(name, temp, condition)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Argument must be 1 for Accuweather 2 for RP5 or something else for both")
        quit()
