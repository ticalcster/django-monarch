from django.test import TestCase

from example.server.monarch_maps import LegacyGroupMap


class MonarchTableMapTests(TestCase):
    def setUp(self):
        pass

    def test_get_table_map(self):
        table_map = LegacyGroupMap()
        self.assertEqual(table_map.get_table_name(), 'LegacyGroup')
