from weatherapp.core.abstract import Command


class Providers(Command):

    """ Print all providers.
    """

    name = 'pvd'

    def run(self, argv):
        """ Run command.
        """

        for provider in self.app.providermanager._providers:
            print(provider)
