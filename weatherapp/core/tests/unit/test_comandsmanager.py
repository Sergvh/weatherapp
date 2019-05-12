import unittest

from weatherapp.core.commandsmanager import CommandsManager


class DummyCommand:
    pass


class CommandsmanagerTestCase(unittest.TestCase):
    """Unit test for commands manager
    """
    def setUp(self):
        self.command_manager = CommandsManager()

    def test_add(self):
        """Tests add method of commands manager
        """

        self.command_manager.add('dummy', DummyCommand)

        self.assertTrue('dummy' in self.command_manager.commands, msg="Command"
                        "'dummy' is missing in command manager")
        self.assertEqual(self.command_manager.get('dummy'), DummyCommand)

    def test_get(self):
        """Tests get method of commands manager
        """

        self.command_manager.add('dummy', DummyCommand)

        self.assertEqual(self.command_manager.get('dummy'), DummyCommand)
        self.assertIsNone(self.command_manager.get('1'))

    def test_contains(self):
        """Tests if '__contains__' method is working properly
        """

        self.command_manager.add('dummy', DummyCommand)

        self.assertTrue(self.command_manager.__contains__('dummy'),
                        DummyCommand)
        self.assertFalse('bar' in self.command_manager)


if __name__ == '__main__':
    unittest.main()
