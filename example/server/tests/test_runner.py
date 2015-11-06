# from django.core.exceptions import ImproperlyConfigured
# from django.test import TestCase
#
# from monarch.runners import MigrationRunner
#
#
# class MonarchRunnerTests(TestCase):
#     def setUp(self):
#         pass
#
#     def test_monarch_runner_with_custom_settings(self):
#         self.assertEqual(
#             MigrationRunner(settings={'default': {'CONNECTOR': 'monarch.connectors.FakeConnector'}}).settings[
#                 'default']['CONNECTOR'],
#             'monarch.connectors.FakeConnector')
#         self.assertRaises(ImportError, lambda: MigrationRunner(settings={'default': {'CONNECTOR': 'monarch.connectors.NotAConnector'}}))
#         self.assertRaises(ImproperlyConfigured, lambda: MigrationRunner(settings={'nodefault': 'hehe'}))
#         self.assertRaises(ImproperlyConfigured, lambda: MigrationRunner(settings={'default': 'hehe'}))
#
#     def test_finding_apps_with_maps(self):
#         runner = MigrationRunner()
#         self.assertIn('server', runner.apps_with_maps)
#         self.assertNotIn('monarch', runner.apps_with_maps)
#
#     def test_finding_monarch_maps(self):
#         runner = MigrationRunner()
#         self.assertIn('LegacyGroup', runner.monarch_maps)
#         self.assertNotIn('NotMonarchTable', runner.monarch_maps)
#
#     def test_connectors(self):
#         runner = MigrationRunner()
#         self.assertEqual('TEST', runner.settings['default']['connector'])
