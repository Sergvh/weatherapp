"""Main application module"""

import html
from argparse import ArgumentParser
import sys
import logging

from providermanager import ProviderManager
from commandsmanager import CommandsManager
import config


class App:
    """Weather agregator aplication
     """

    loger = logging.getLogger(__name__)

    LOG_LEVEL_MAP = {0: logging.WARNING,
                     1: logging.INFO,
                     2: logging.DEBUG}

    def __init__(self):
        self.arg_parser = self._arg_parse()
        self.providermanager = ProviderManager()
        self.commandsmanager = CommandsManager()

    @staticmethod
    def _arg_parse():
        """Initialize argument parser
        """

        arg_parser = ArgumentParser(add_help=False)
        arg_parser.add_argument('-cc', '--clearcache', nargs='?',
                                help="use -cc [Service name] to clear cache "
                                "in file", default='')
        arg_parser.add_argument('-s', '--save', nargs='?',
                                help="use -s [Service name] for save data "
                                "in file", default='')
        arg_parser.add_argument('command', help='Service name', nargs='?')
        arg_parser.add_argument('-r', '--refresh', help='Update caches',
                                action='store_true')
        arg_parser.add_argument('-c', '--config', nargs='?',
                                help="use -c [Service name] for configure",
                                default='')

        arg_parser.add_argument(
            '-v', '--verbose',
            action='count',
            dest='verbose_level',
            default=config.DEFAULT_VERBOSE_LEVEL,
            help='Increase verbosity of logging output level')
        return arg_parser

    def configure_logging(self):
        """Ceate logging handlers for any log output
        """

        root_logger = logging.getLogger('')
        root_logger.setLevel(logging.DEBUG)

        console = logging.StreamHandler()
        console_level = self.LOG_LEVEL_MAP.get(self.options.verbose_level,
                                               logging.WARNING)
        console.setLevel(console_level)
        formatter = logging.Formatter(config.DEFAULT_MESSAGE_FORMAT)
        console.setFormatter(formatter)
        root_logger.addHandler(console)

    @staticmethod
    def produce_output(title, location, info):
        """Prints result
        """
        print(f'\n{title}')
        print(f'*' * 10)

        print(f'\n{location}')
        print(f'_' * 20)
        for key, value in info.items():
            print(f'{key}: {html.unescape(value)}')
        print('=' * 40, end='\n\n')

    def run(self, argv):
        """Run application

        :param argv: List of passed arguments
        """

        self.options, remaining_args = self.arg_parser.parse_known_args(argv)
        self.configure_logging()
        self.loger.debug('Got the following args %s', argv)
        command_name = self.options.command

        if not command_name:
            #run all weather providers by default
            for name, provider in self.providermanager._providers.items():
                provider_obj = provider(self)
                self.produce_output(provider_obj.title,
                                    provider_obj.location,
                                    provider_obj.run(remaining_args))
        elif command_name in self.providermanager:
            #run specific provider
            provider = self.providermanager[command_name]
            provider_obj = provider(self)
            self.produce_output(provider_obj.title,
                                provider_obj.location,
                                provider_obj.run(remaining_args))

        elif command_name in self.commandsmanager:
            #run specific command
            command = self.commandsmanager[command_name]
            command(self).run(remaining_args)


def main(argv=sys.argv[1:]):
    return App().run(argv)


if __name__ == '__main__':
    main(sys.argv[1:])
