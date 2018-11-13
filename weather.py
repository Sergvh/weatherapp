#!usr/bin/python3.6

from urllib.request import urlopen, Request

ACCU_URL = "https://www.accuweather.com/uk/ua/lviv/324561/weather-forecast/324561"

headers = {'User-Agent' : 'Mozilla/5.0 (X11; Fedora; Linux x86_64)'}

accu_request = Request(ACCU_URL, headers=headers)
accu_page = urlopen(accu_request).read()

print(accu_page)
