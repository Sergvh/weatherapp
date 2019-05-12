import unittest

from weatherapp.core.providermanager import ProviderManager


class DummyProvider:
    pass


class ProviderManagerTestCase(unittest.TestCase):
    """Unit test for provider manager
    """
    def setUp(self):
        self.provider_manager = ProviderManager()

    def test_add(self):
        """Tests add method of provider manager
        """

        self.provider_manager.add('dummy', DummyProvider)

        self.assertTrue('dummy' in self.provider_manager._providers,
                        msg="Provider 'dummy' is missing in provider manager")
        self.assertEqual(self.provider_manager.get('dummy'), DummyProvider)

    def test_get(self):
        """Tests get method of provider manager
        """

        self.provider_manager.add('dummy', DummyProvider)

        self.assertEqual(self.provider_manager.get('dummy'), DummyProvider)
        self.assertIsNone(self.provider_manager.get('1'))

    def test_contains(self):
        """Tests if '__contains__' method is working properly
        """

        self.provider_manager.add('dummy', DummyProvider)

        self.assertTrue(self.provider_manager.__contains__('dummy'),
                        DummyProvider)
        self.assertFalse('bar' in self.provider_manager)


if __name__ == '__main__':
    unittest.main()
