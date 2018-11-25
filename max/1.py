#!usr/bin/python3.6
import html
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request

ACCU_URL = "https://www.accuweather.com/uk/ua/lviv/324561/weather-forecast/324561"
RP5_URL = ("http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D1%83_"
          "%D0%9B%D1%8C%D0%B2%D0%BE%D0%B2%D1%96,_%D0%9B%D1%8C%D0%B2%D1%96%D0%"
          "B2%D1%81%D1%8C%D0%BA%D0%B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C")

headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64)'}

ACCU_TAGS = ('class="large-temp"', 'class="cond')#('<span class="large-temp">', '<span class="cond">')
RP5_TAGS = ('class="t_0"', 'class="ArchiveTempFeeling"')#('<span class="t_0" style="display: block;">',
            #'<div class="ArchiveTempFeeling">')
            #'<div class="TempStr"><span class="t_0" style="display: block;">')

def get_request_headers():
    return{'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64)'}

request = Request(RP5_URL, headers=get_request_headers())

page_source = urlopen(request).read()

page_source = page_source.decode('utf-8')
soup = bs(page_source, 'html.parser')
k = 'ArchiveTempFeeling'
a = soup.find(attrs={'class': k})
print(a.text)