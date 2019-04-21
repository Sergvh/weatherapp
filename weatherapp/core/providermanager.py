from weatherapp.core.providers import AccuWeatherProvider, Rp5WeatherProvider, \
                      GisWeatherProvider, SinWeatherProvider


class ProviderManager:
    """Discovers registered providers and loads them
    """

    def __init__(self):
        self._providers = {}
        self._load_providres()

    def _load_providres(self):
        """Loads all existing providers
        """

        for provider in [AccuWeatherProvider, Rp5WeatherProvider,
                         GisWeatherProvider, SinWeatherProvider]:
            self.add(provider.name, provider)

    def add(self, name, provider):
        """ Add new provider by name

        :param name: providers name.
        :param provider:
        :return:
        """

        self._providers[name] = provider

    def get(self, name):
        """Gets provider by name"""

        return self._providers.get(name, None)

    def __len__(self):
        """ Returns count of all existing providers
        """

        return len(self._providers)

    def __contains__(self, name):
        """Returns True ir False if providers exists in container

        :param name: name of provider
        :return:
        """
        return name in self._providers

    def __getitem__(self, name):
        """ Gets one provider from container
        """

        return self._providers[name]
