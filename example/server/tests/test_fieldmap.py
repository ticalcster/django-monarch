from django.test import TestCase

from monarch.mapping import FieldMap, field_map

from server.models import Group


def convert_to_upper(field_object, value):
    if hasattr(value, 'upper'):
        return value.upper()
    return value


class DummyField(FieldMap):
    name = 'GroupID'
    model_field = 'id'


class DummyFieldConvert(FieldMap):
    name = 'GroupID'
    model_field = 'id'
    converter = convert_to_upper


class MonarchFieldMapTests(TestCase):
    def setUp(self):
        pass

    def test_field_map_get_value(self):
        dummy_field = DummyField(value='asdf')
        self.assertEqual(dummy_field.get_value(), 'asdf')

        dummy_field = DummyFieldConvert(value='asdf')
        self.assertEqual(dummy_field.get_value(), 'ASDF')

    def test_field_map_factory(self):
        GroupFieldMap = field_map('GroupID', model_field='id')
        self.assertEqual(GroupFieldMap.model_field, 'id')

