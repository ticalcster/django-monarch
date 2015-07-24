from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.six import StringIO

from monarch.runners import MigrationRunner


class MonarchRunnerTestCase(TestCase):
    def setUp(self):
        pass

    def test_monarch_runner_with_custom_settings(self):
        self.assertEqual(
            MigrationRunner(settings={'default': {'CONNECTOR': 'MockRunner'}}).settings['default']['CONNECTOR'],
            'MockRunner')
        self.assertRaises(ImproperlyConfigured, lambda: MigrationRunner(settings={'nodefault': 'hehe'}))
        self.assertRaises(ImproperlyConfigured, lambda: MigrationRunner(settings={'default': 'hehe'}))

    def test_finding_apps_with_maps(self):
        runner = MigrationRunner()
        apps_with_maps = runner.get_apps_with_maps()
        self.assertIn('server', apps_with_maps)
        self.assertNotIn('monarch', apps_with_maps)

    def test_finding_monarch_maps(self):
        pass



class MonarchCommendTestCase(TestCase):
    def setUp(self):
        pass

    def test_command_output(self):
        out = StringIO()
        call_command('runmonarch', stdout=out)
        self.assertIn('Setup monarch:', out.getvalue())
