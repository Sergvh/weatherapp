#!usr/bin/python3.6
import html
import time
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request

URL = "http://example.webscraping.com/"


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


def get_country_info(soup):
    """
    :return: selects and prints all countries names.
    """
    a = soup.select('td a')
    for country in a:
        print(country.text)

def get_href_next(soup):
    """    
    :return:  text off link on next page
    """
    next1 = ''
    pagination = soup.find('div', {"id": 'pagination'})
    a = pagination.find_all('a')
    for link in a:
        if link.text == 'Next >':
            next1 = link['href']
    return next1


def main():
    """ Main entry point
    """
    next1 = '0'
    while next1 != '':
        content = get_page_source(URL+next1)
        soup = bs(content, 'html.parser')
        get_country_info(soup)
        time.sleep(1)
        next1 = get_href_next(soup)


if __name__ == '__main__':
    main()
