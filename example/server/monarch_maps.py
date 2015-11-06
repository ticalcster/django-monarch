from monarch.mapping import field_map, TableMap

from models import Group, Address


class NotMonarchMap(object):
    """Should not be in the monarch maps"""
    table_name = 'NotMonarchMap'


class ErrorMap(TableMap):
    # table_name = 'Error'
    pass


class LegacyGroupMap(TableMap):
    table_name = 'LegacyGroup'
    model_class = Group

    fields = (
        field_map('GroupID', pk=True, ),
        field_map('GroupName', model_field='name'),
        field_map('Website', model_field='website'),
    )

    def create_model(self):
        address = Address(city='MI')
        address.save()

        obj = self.model_class()
        obj.address = address
        obj.save()
        return obj
