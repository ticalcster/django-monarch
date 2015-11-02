from monarch import mapping

import models


class NotMonarchMap(object):
    """Should not be in the monarch maps"""
    table_name = 'NotMonarchMap'


class ErrorMap(mapping.TableMap):
    # table_name = 'Error'
    pass


class LegacyGroupMap(mapping.TableMap):
    table_name = 'LegacyGroup'
    model_class = models.Group

    id = mapping.FieldMap('GroupID', pk=True)
    name = mapping.FieldMap('GroupName')
    website = mapping.FieldMap('Website')
