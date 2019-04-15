#Application default verbose and logging level
DEFAULT_VERBOSE_LEVEL = 0
DEFAULT_MESSAGE_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# AccuWeather provider related configuration
ACCU_PROVIDER_NAME = 'accu'
ACCU_PROVIDER_TITLE = 'AccuWeather'

DEFAULT_ACCU_LOCATION_NAME = 'Lviv'
DEFAULT_ACCU_LOCATION_URL = \
    'https://www.accuweather.com/uk/ua/lviv/324561/weather-forecast/324561'
ACCU_BROWSE_LOCATIONS = "https://www.accuweather.com/uk/browse-locations"


# RP5 provider related configuration
RP5_PROVIDER_NAME = 'rp5'
RP5_PROVIDER_TITLE = 'rp5.ua'

DEFAULT_RP5_LOCATION_NAME = 'Lviv'
DEFAULT_RP5_LOCATION_URL = 'http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%' \
                            'B0_%D1%83_%D0%9B%D1%8C%D0%B2%D0%BE%D0%B2%D1%96,_' \
                            '%D0%9B%D1%8C%D0%B2%D1%96%D0%B2%D1%81%D1%8C%D0%BA' \
                            '%D0%B0_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C'
RP5_BROWSE_LOCATIONS = "http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D" \
                       "0%B2_%D1%81%D0%B2%D1%96%D1%82%D1%96"


# Gismeteo provider related configuration
GIS_PROVIDER_NAME = 'gis'
GIS_PROVIDER_TITLE = 'Gismeteo'

DEFAULT_GIS_LOCATION_NAME = 'Lviv'
DEFAULT_GIS_LOCATION_URL = 'https://www.gismeteo.ua/ua/weather-lviv-14412/'
GIS_BROWSE_LOCATIONS = "https://www.gismeteo.ua/ua/catalog/"


# Sinoptic provider related configuration
SIN_PROVIDER_NAME = 'sin'
SIN_PROVIDER_TITLE = 'Sinoptik'

DEFAULT_SIN_LOCATION_NAME = 'Lviv'
DEFAULT_SIN_LOCATION_URL = 'https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE' \
                           '%D0%B4%D0%B0-%D0%BB%D1%8C%D0%B2%D1%96%D0%B2'
SIN_BROWSE_LOCATIONS = "https://ua.sinoptik.ua/%D1%83%D0%BA%D1%80%D0%B0%D1%" \
                       "97%D0%BD%D0%B0"


#Configuration settings
CONFIG_FILE = 'wapp.ini'


#File to save settings
INFO_FILE = 'weather.txt'


#Cache settings
CACHE_DIR = '.wappcache'
CACHE_TIME = 300
