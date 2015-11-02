from django.test import TestCase

from monarch import connectors
from monarch.runners import MigrationRunner


class MonarchConnectorTests(TestCase):
    def setUp(self):
        self.runner = MigrationRunner()

    def test_base_connector(self):
        connector = connectors.BaseConnector(self.runner.settings['default'])
        self.assertRaises(NotImplementedError, lambda: connector.fetcher())
        self.assertRaises(NotImplementedError, lambda: connector.fetch())

    # def test_base_connector(self):
    #     connector = connectors.JsonConnectorMixin()
    #     connector.fetcher = lambda: StringIO().write('{ "error" : false }')
    #     self.assertRaises(NotImplementedError, lambda: connector.fetch())
