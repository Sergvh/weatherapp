#!usr/bin/env python

import html
import sys
import os
import argparse

from pathlib import Path

from providers import AccuWeatherProvider, Rp5WeatherProvider,\
                      GisWeatherProvider
import config


def get_info_file():
    return Path.home() / config.INFO_FILE


# def configurate(provider):
#     locations = config.LOCATIONS_PROVIDERS[provider](PROVIDER[provider])
#
#     while locations:
#         for index, location in enumerate(locations):
#             print(f'{index + 1}. {location[0]}')
#         selected_index = int(input('Please select location: '))
#         location = locations[selected_index - 1]
#         locations = config.LOCATIONS_PROVIDERS[provider](location[1])
#     save_configuration(provider, *location)


def get_tag_content(soup, tag):
    """
    :param soup: decoded page source
    :param tag: string what to find in page content
    :return: generated string with information wich was found after tag
    """
    content = soup.find(attrs={'class': tag})
    return content.text


def get_gis_weather_info(page_content):
    print('Hello')


def produce_output(city_name, info):
    print(f'\n{city_name}')
    print(f'_'*20)
    for key, value in info.items():
        print(f'{key}: {html.unescape(value)}')
    print('\n')


def save_data_to_file(info):
    """
    :param info:
    :return:
    """

    with open(get_info_file(), 'w') as info_file:
        for key, value in info.items():
            info_file.write(f'{key}: {html.unescape(value)}\n')


def get_accu_weather_info(refresh=False):
    accu = AccuWeatherProvider()
    produce_output(accu.location, accu.run(refresh=refresh))


def get_rp5_weather_info(refresh=False):
    rp5 = Rp5WeatherProvider()
    produce_output(rp5.location, rp5.run(refresh=refresh))


def get_gis_weather_info(refresh=False):
    gis = GisWeatherProvider()
    produce_output(gis.location, gis.run(refresh=refresh))


def get_all_providers_info(refresh=False):
    """
    :param params:
    :return:
    """
    get_accu_weather_info(refresh=refresh)
    get_rp5_weather_info(refresh=refresh)
    get_gis_weather_info(refresh=refresh)


# def clear_old_cache():
#     cache_dir = get_cache_directory()
#     if cache_dir.exists():
#         for name in os.listdir(cache_dir):
#             cache_path = cache_dir / name
#             if cache_path.exists() and not is_valid(cache_path):
#                 print(cache_path)
#                 os.remove(cache_path)
#

# def delete_all_cache():
#     cache_dir = get_cache_directory()
#     if cache_dir.exists():
#         os.removedirs(cache_dir)
#

KNOWN_COMMANDS = {'accu': get_accu_weather_info,
                  'rp5': get_rp5_weather_info,
                  'gis': get_gis_weather_info,
                  '-s': save_data_to_file,
                  # '-c': configurate,
                  'all': get_all_providers_info}


def main(argv):
    """ Main entry point
        :argv - must be:
                        'accu' for AccuWeather:
                        'rp5' for RP5
                        'all' for both
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-cc', '--clearcache', nargs='?',
                        help="use -cc [Service name] to clear cache "
                             "in file", default='')
    parser.add_argument('-s', '--save',  nargs='?',
                        help="use -s [Service name] for save data "
                        "in file", default='')
    parser.add_argument('-c', '--config', nargs='?',
                        help="use -c [Service name] for configure", default='')
    parser.add_argument('command', help='Service name', nargs='?')
    parser.add_argument('-r', '--refresh', help='Update caches',
                        action='store_true')

    #clear_old_cache()

    params = parser.parse_args(argv)

    if params.command:
        KNOWN_COMMANDS[params.command](refresh=params.refresh)
    elif params.save:
        KNOWN_COMMANDS['-s'](params.save,
                             KNOWN_COMMANDS[params.save](params.save))
    elif params.config:
        KNOWN_COMMANDS['-c'](params.config)
    # elif params.clearcache:
    #     delete_all_cache()

    else:
          print('Unknown command provided!')
          sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])
