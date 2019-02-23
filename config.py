ACCU_PROVIDER_NAME = 'accu'
RP5_PROVIDER_NAME = 'rp5'
GIS_PROVIDER_NAME = 'gis'
#
# ACCU_URL = ("https://www.accuweather.com/uk/ua/lviv/324561/weather-forecast/"
#             "324561")
# RP5_URL = ("http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D1%83_"
#            "%D0%9B%D1%8C%D0%B2%D0%BE%D0%B2%D1%96,_%D0%9B%D1%8C%D0%B2%D1%96%D0%"
#            "B2%D1%81%D1%8C%D0%BA%D0%B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%"
#            "D1%82%D1%8C")

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

PROVIDER = {'accu': ACCU_BROWSE_LOCETION,
            'rp5': RP5_BROWSE_LOCETION,
            'gis': GIS_BROWSE_LOCETION}
