"""App commands
"""

from abstract import Command


class Configurate(Command):
    """Help to configure weather provider
    """

    name = 'config'

    def get_parser(self):
        parser = super(Configurate, self).get_parser()#super.get_parser()
        parser.add_argument('provider', help='Provider name')
        return parser

    def run(self, argv):
        """Run command
        """

        parsed_args = self.get_parser().parse_args(argv)
        if parsed_args.provider:
            provider_name = parsed_args.provider
            if provider_name in self.app.providermanager:
                provider_factory = self.app.providermanager.get(provider_name)
                provider_factory(self.app).configurate()


class Help(Command):
    """Showing help information
    """

    name = 'help'

    def run(self, argv):
        pass
