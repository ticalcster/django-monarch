from django.test import TestCase

from server.monarch_maps import LegacyGroupMap


class MonarchTableMapTests(TestCase):
    def setUp(self):
        self.good_row = {'GroupID': 12, 'GroupName': 'The Best', 'WebSite': 'http://example.com/'}

    def test_get_table_map(self):
        table_map = LegacyGroupMap(self.good_row)
        self.assertEqual(table_map.get_table_name(), 'LegacyGroup')
