from copy import copy
from django.test import TestCase

from monarch.models import RecordLink

from server.monarch_maps import LegacyGroupMap, LegacyDistrictMap
from server.models import Group, Address, District


class MonarchTableMapTests(TestCase):
    def setUp(self):
        self.good_row = {'GroupID': 12, 'GroupName': 'The Best', 'WebSite': 'http://example.com/',
                         'Address': '123 Best Street', 'City': 'Grand Rapids', 'State': 'MI', 'Zip': '49508'}
        self.good_row_again = {'GroupID': 12, 'GroupName': 'The Better', 'WebSite': 'http://example.com/',
                               'Address': '123 Best Street', 'City': 'Grand Rapids', 'State': 'MI', 'Zip': '49508'}

        self.district_row = {'DistrictID': 100, 'GroupID': 12, 'DistrictName': 'District of 9', 'MaxDistricts': 5,
                             'Address': '123 Best Street', 'City': 'Grand Rapids', 'State': 'MI', 'Zip': '49508'}

    def test_get_table_map(self):
        table_map = LegacyGroupMap(self.good_row)
        self.assertEqual(table_map.get_table_name(), 'LegacyGroup')
        self.assertEqual(len(table_map.pk_fields), 1)
        table_map.migrate()

        migrated_model = Group.objects.get(name='The Best')
        self.assertEqual(migrated_model.website, 'http://example.com/')
        self.assertEqual(migrated_model.website, table_map.model.website)

        table_map_again = LegacyGroupMap(self.good_row_again)
        table_map_again.migrate()
        self.assertEqual(table_map_again.model.pk, table_map.model.pk)
        self.assertEqual(table_map_again.model.pk, 1)

        self.assertEqual(table_map.model.address.pk, 1)
        self.assertEqual(table_map.model.address.address1, '123 Best Street')
        self.assertEqual(table_map.model.address.zip, '49508')

        district_map = LegacyDistrictMap(self.district_row)
        district_map.migrate()

        migrated_district = District.objects.get(name='District of 9')
        self.assertEqual(migrated_district.pk, 1)
        self.assertEqual(migrated_district.group.pk, migrated_model.pk)
