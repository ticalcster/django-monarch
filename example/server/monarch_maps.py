from monarch.mapping import field_map, TableMap, pathway

from models import Group, Address, District


@pathway(Group, Address)
def group_to_address(group):
    return group.address


@pathway(District, Address)
def group_to_address(group):
    return group.address


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
        field_map('WebSite', model_field='website'),
        field_map('Address', model_field='address.address1'),
        field_map('City', model_field='address.city'),
        field_map('State', model_field='address.state'),
        field_map('Zip', model_class=Address, model_field='zip'),
    )

    def create_model(self):
        address = Address(city='MI')
        address.save()

        obj = self.model_class()
        obj.address = address
        obj.save()
        return obj


class LegacyDistrictMap(TableMap):
    table_name = 'LegacyDistrict'
    model_class = District

    fields = (
        field_map('DistrictID', pk=True),
        field_map('GroupID', fk=True, foreign_map=LegacyGroupMap, model_field='group'),
        field_map('DistrictName', model_field='name'),
        field_map('MaxDistricts', model_field='max_districts'),
        field_map('Address', model_field='address.address1'),
        field_map('City', model_class=Address, model_field='city'),
        field_map('State', model_field='address.state'),
        field_map('Zip', model_class=Address, model_field='zip'),
    )

    def create_model(self):
        address = Address(city='MI')
        address.save()

        obj = self.model_class(max_districts=0)
        obj.address = address
        obj.save()
        return obj

