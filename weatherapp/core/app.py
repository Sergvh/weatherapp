#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

"""Main application module"""

from argparse import ArgumentParser
import sys
import logging

from weatherapp.core.providermanager import ProviderManager
from weatherapp.core.commandsmanager import CommandsManager
from weatherapp.core.formatters import TableFormatter
from weatherapp.core import config


class App:
    """Weather agregator aplication
     """

    loger = logging.getLogger(__name__)

    LOG_LEVEL_MAP = {0: logging.WARNING,
                     1: logging.INFO,
                     2: logging.DEBUG}

    def __init__(self, stdin=None, stdout=None, stderr=None):
        self.stdin = stdin or sys.stdin
        self.stdout = stdout or sys.stdout
        self.stderr = stderr or sys.stderr
        self.arg_parser = self._arg_parse()
        self.providermanager = ProviderManager()
        self.commandsmanager = CommandsManager()
        self.formatters = self.load_formaters()

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
        arg_parser.add_argument('-f', '--formatter',
                                action='store',
                                default='table',
                                help="Output default to table. There are 'list'"
                                     "and 'scv'")
        arg_parser.add_argument(
            '-v', '--verbose',
            action='count',
            dest='verbose_level',
            default=config.DEFAULT_VERBOSE_LEVEL,
            help='Increase verbosity of logging output level')

        arg_parser.add_argument(
            '-d', '--debug',
            action='store_true',
            default=False,
            help='Show errors.')

        return arg_parser

    @staticmethod
    def load_formaters():
        return {'table': TableFormatter}

    def configure_logging(self):
        """Ceate logging handlers for any log output
        """

        root_logger = logging.getLogger('')
        root_logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler()
        console = handler
        console_level = self.LOG_LEVEL_MAP.get(self.options.verbose_level,
                                               logging.WARNING)
        console.setLevel(console_level)
        formatter = logging.Formatter(config.DEFAULT_MESSAGE_FORMAT)
        console.setFormatter(formatter)
        root_logger.addHandler(console)

    def produce_output(self, title, location, data):
        """Prints result
        """

        formatter = self.formatters.get(self.options.formatter, 'table')()
        columns = [title, location]

        self.stdout.write(formatter.emit(columns, data))
        self.stdout.write('\n')

    def run_command(self, name, argv):
        """Run specified command
        """

        command = self.commandsmanager.get(name)
        try:
            command(self).run(argv)
        except Exception:
            msg = "Error during command: %s execution"
            if self.options.debug:
                self.loger.exception(msg, name)
            else:
                self.loger.error(msg, name)

    def run_provider(self, name, argv):
        """Execute specified  weather provider
        """

        provider = self.providermanager.get(name)
        provider = provider(self)
        self.produce_output(provider.title,
                            provider.location,
                            provider.run(argv))

    def run_providers(self, argv):
        """Execute all available weather providers
        """

        for provider in self.providermanager._providers.values():
            provider = provider(self)
            self.produce_output(provider.title,
                                provider.location,
                                provider.run(argv))

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
            return self.run_providers(remaining_args)

        elif command_name in self.providermanager:
            #run specific provider
            return self.run_provider(command_name, remaining_args)

        elif command_name in self.commandsmanager:
            #run specific command
            return self.run_command(command_name, remaining_args)



def main(argv=sys.argv[1:]):
    return App().run(argv)


if __name__ == '__main__':
    main(sys.argv[1:])
