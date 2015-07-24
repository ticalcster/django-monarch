# -*- coding: utf-8 -*-
class NoMapPKField(Exception):
    message = 'A Primary Key is missing form the import row.'


class NoMapCreateMethodException(Exception):
    pass

