"""Abstract classes for ptoject
"""

import abc
import argparse
import configparser
from pathlib import Path
import hashlib
import time
from urllib.request import urlopen, Request

import config


class Command(abc.ABC):
    """Base class for commands

    :param app: Main application instance.
    :type app: app.App
    """

    def __init__(self, app):
        self.app = app

    @staticmethod
    def get_parser():
        """Initialize argument parser for command
        """

        parser = argparse.ArgumentParser()
        return parser

    @abc.abstractmethod
    def run(self, argv):
        """Invoked by application when the command is run
        Should be overriden in subclass
        """


class WeatherProvider(Command):
    """Weather provider abstract class

    Defines behavior for all weather providers.
    """

    def __init__(self, app):
        super().__init__(app)

        location, url = self.get_configuration()
        self.location = location
        self.url = url

    @abc.abstractmethod
    def configurate(self):
        """Performs provider configuration
        """


    @abc.abstractmethod
    def get_name(self):
        """Provider name
        """


    @abc.abstractmethod
    def get_weather_info(self, content):
        """Collects weather information

        Gets weather information from source and produce it in the following
        format:

        weather_info = {
            'temp':        ''  #temperature
            'cond':        ''  #weather condition
            'feels_like':  ''  #feels like temperature
            'wind':        ''  #wind information
        """

    @abc.abstractmethod
    def get_default_location(self):
        """Default location name.
        """

    @abc.abstractmethod
    def get_default_url(self):
        """Default location url
        """

    def get_configuration(self):
        """Returns configured location name and url

        :returns: name and url
        :rtype: tuple
        """

        name = self.get_default_location()
        url = self.get_default_url()
        configuration = configparser.ConfigParser()

        try:
            configuration.read(self.get_configuration_file())
        except configparser.Error:
            print(f'Bad configuration file.'
                  f' Please reconfigurate your provider {self.name}')

        if self.get_name() in configuration. sections():
            location_config = configuration[self.get_name()]
            name, url = location_config['name'], location_config['url']

        return name, url

    @staticmethod
    def get_configuration_file():
        """Path to configuration file

        :returns Path to configuration file in your home directory.
        """
        return Path.home() / config.CONFIG_FILE

    def save_configuration(self, provider, name, url):
        """Save selected location to configuration file

        :param provider: provider name
        :param type: str

        :param name: city name
        :param type: str

        :param url: Prefered location url
        :param type: str
        """
        print(provider+'   '+name+'   '+url)
        parser = configparser.ConfigParser()

        config_file = self.get_configuration_file()

        if config_file.exists():
            parser.read(config_file)

        url = url.replace('%', '%%')
        parser[provider] = {'name': name, 'url': url}
        with open(config_file, 'w') as configfile:
            parser.write(configfile)

    @staticmethod
    def get_request_headers():
        """Returns custom headers for url requests.
        """

        return {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64)'}

    @staticmethod
    def get_url_hash(url):
        """Returns generated hash for given url.
        """

        return hashlib.md5(url.encode('utf-8')).hexdigest()

    def save_cache(self, url, page_source):
        """ Save page source data to file
        """
        url_hash = self.get_url_hash(url)
        cache_dir = self.get_cache_directory()
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True)

        with (cache_dir / url_hash).open('wb') as cache_file:
            cache_file.write(page_source)

    @staticmethod
    def is_valid(path):
        """Check if current cache is valid.
        """

        return (time.time() - path.stat().st_mtime) < config.CACHE_TIME

    def get_cache(self, url):
        """Get cache data if any.
        """

        cache = b''
        url_hash = self.get_url_hash(url)
        cache_dir = self.get_cache_directory()
        if cache_dir.exists():
            cache_path = cache_dir / url_hash
            if cache_path.exists() and self.is_valid(cache_path):
                with cache_path.open('rb') as cache_file:
                    cache = cache_file.read()

        return cache

    @staticmethod
    def get_cache_directory():
        """Path to cache directory
        :returns Path to cache directory in your home directory.
        """
        return Path.home() / config.CACHE_DIR

    def get_page_source(self, url, refresh=False):
        """
        :param url: site url in str
        :return: decoded source code of html page received from url.
        """

        cache = self.get_cache(url)
        if cache and not self.app.options.refresh:
            page_source = cache
        else:
            request = Request(url, headers=self.get_request_headers())
            page_source = urlopen(request).read()
            self.save_cache(url, page_source)

        return page_source.decode('utf-8')

    def run(self, argv, refresh=False):
        """Run provider
        """

        content = self.get_page_source(self.url, refresh=refresh)

        return self.get_weather_info(content, refresh=refresh)

