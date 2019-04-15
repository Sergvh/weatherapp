"""Abstract class for managers
"""

import abc


class Manager(abc.ABC):
    """Abstract class for managers
    """

    @abc.abstractmethod
    def add(self, name, command):
        """ Add new command to manager

        :param name: command name.
        :type name: str
        :param command: command class
        :typw command: subtype of weatherapp.abstract.Command
        """

    @abs.abstractmethod
    def get(self, name):
        """Gets command from manager by name
        :param name: command name.
        :type name: str
        """

    @abs.abstractmethod
    def __len__(self):
        """ Returns count of all existing commands
        """

    @abs.abstractmethod
    def __contains__(self, name):
        """Returns True or False if command exists in manager

        Implementation of this "dunder" method allows us to use "in" operator
        with manager to check if command exists in manager.

        :param name: name of command
        :type name: str
        """

    @abs.abstractmethod
    def __getitem__(self, name):
        """ Gets command by name

        Implementation of this "dunder" method allows us to access commands
        by name in the same way that it works in dictionaries.

        :param name: name of command
        :type name: str
        """
