from monarch.mapping import FieldMap, TableMap


class NotMonarchMap(object):
    """Should not be in the monarch maps"""
    table_name = 'NotMonarchMap'


class ErrorMap(TableMap):
    #table_name = 'Error'
    pass


class LegacyPost(TableMap):
    table_name = 'Entry'
