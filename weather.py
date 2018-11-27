#!usr/bin/python3.6
import html
from urllib.request import urlopen, Request

ACCU_URL = "https://www.accuweather.com/uk/ua/lviv/324561/weather-forecast/324561"
RP5_URL = ("http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D1%83_"
          "%D0%9B%D1%8C%D0%B2%D0%BE%D0%B2%D1%96,_%D0%9B%D1%8C%D0%B2%D1%96%D0%"
          "B2%D1%81%D1%8C%D0%BA%D0%B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C")

headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64)'}

ACCU_TAGS = ('<span class="large-temp">', '<span class="cond">')
RP5_TAGS = ('<span class="t_0" style="display: block;">',
            '<div class="ArchiveTempFeeling">')
            #'<div class="TempStr"><span class="t_0" style="display: block;">')


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


def get_tag_content(page_content, tag):
    """
    :param page_content: decoded page source
    :param tag: string what to find in page content
    :return: generated string with information wich was found after tag
    """
    tag_size = len(tag)
    tag_index = page_content.find(tag)
    value_start = tag_index + tag_size
    content = ''

    for char in page_content[value_start:]:
        if char != '<':
            content += char
        else:
            break
    return content

def get_weather_info(page_content, tags):
    """
    :param page_content:  decoded page source
    :param tags: string what to find in page content
    :return:
    """
    return tuple([get_tag_content(page_content, tag) for tag in tags])


def produce_output(provider_name, temp, condition):
    print(f'\n {provider_name}')
    print(f'Temperature: {html.unescape(temp)}\n')
    print(f'Condition: {html.unescape(condition)}\n')

def main():
    """ Main antry point
    """
    weather_sites = {'AccuWeather': (ACCU_URL, ACCU_TAGS),
                     'RP5': (RP5_URL, RP5_TAGS)}

    for name in weather_sites:
        url, tags = weather_sites[name]
        content = get_page_source(url)
        temp, condition = get_weather_info(content, tags)
        produce_output(name, temp, condition)


if __name__ == '__main__':
    main()
