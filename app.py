"""Main application module"""

import html
from argparse import ArgumentParser
import sys

from providermanager import ProviderManager


class App:
    """Weather agregator aplication
     """
    def __init__(self):
        self.arg_parser = self._arg_parse()
        self.providermanager = ProviderManager()

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
        return arg_parser

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


def main(argv=sys.argv[1:]):
    return App().run(argv)


if __name__ == '__main__':
    main(sys.argv[1:])
