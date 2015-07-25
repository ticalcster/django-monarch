from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.six import StringIO
import cStringIO


from monarch import connectors
from monarch.runners import MigrationRunner


class MonarchRunnerTests(TestCase):
    def setUp(self):
        pass

    def test_monarch_runner_with_custom_settings(self):
        self.assertEqual(
            MigrationRunner(settings={'default': {'CONNECTOR': 'monarch.connectors.FakeConnector'}}).settings[
                'default']['CONNECTOR'],
            'monarch.connectors.FakeConnector')
        self.assertRaises(ImportError, lambda: MigrationRunner(settings={'default': {'CONNECTOR': 'monarch.connectors.NotAConnector'}}))
        self.assertRaises(ImproperlyConfigured, lambda: MigrationRunner(settings={'nodefault': 'hehe'}))
        self.assertRaises(ImproperlyConfigured, lambda: MigrationRunner(settings={'default': 'hehe'}))

    def test_finding_apps_with_maps(self):
        runner = MigrationRunner()
        self.assertIn('server', runner.apps_with_maps)
        self.assertNotIn('monarch', runner.apps_with_maps)

    def test_finding_monarch_maps(self):
        runner = MigrationRunner()
        self.assertIn('LegacyGroup', runner.monarch_maps)
        self.assertNotIn('NotMonarchTable', runner.monarch_maps)

    def test_connectors(self):
        runner = MigrationRunner()
        self.assertEqual('TEST', runner.settings['default']['connector'])


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

class MonarchCommendTests(TestCase):
    def setUp(self):
        pass

    def test_command_output(self):
        out = StringIO()
        call_command('runmonarch', stdout=out)
        self.assertIn('Monarch setup:', out.getvalue())
