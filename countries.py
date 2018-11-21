#!usr/bin/python3.6
import re
from urllib.request import urlopen, Request

ACCU_URL = "http://example.webscraping.com/"

headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64)'}

request = Request(ACCU_URL, headers=headers)
page = urlopen(request).read()
page = page.decode('utf-8')

COUNTRIES_TAG = '.png'
i = 0
country = ''
for match in re.finditer(COUNTRIES_TAG, page):
    if i != 0 and i <= 10:
        country = ''
        for char in page[match.end():]:
            if char != '<':
                country += char
            else:
                break
        print(f'Found country: {country[5:]}')
        i += 1
    else:
        i += 1
        continue
