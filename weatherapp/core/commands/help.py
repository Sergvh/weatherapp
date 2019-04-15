from weatherapp.core.abstract import Command


class Help(Command):
    """Showing help information
    """

    name = 'help'

    def run(self, argv):
        pass
