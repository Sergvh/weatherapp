from weatherapp.core.commands import Configurate, Help, Providers


class CommandsManager:
    """Discovers registered commands and loads them
    """

    def __init__(self):
        self.commands = {}
        self._load_commands()

    def _load_commands(self):
        """Loads all existing commands
        """

        for command in [Configurate, Providers, Help]:
            self.add(command.name, command)

    def add(self, name, command):
        """ Add new provider by name

        :param name: command name.
        :param command: command class
        :return:
        """

        self.commands[name] = command

    def get(self, name):
        """Gets command by name"""

        return self.commands.get(name, None)

    def __len__(self):
        """ Returns count of all existing commands
        """

        return len(self.commands)

    def __contains__(self, name):
        """Returns True or False if commands exists in container

        :param name: name of command
        :return:
        """
        return name in self.commands

    def __getitem__(self, name):
        """ Gets one command from container
        """

        return self.commands[name]
