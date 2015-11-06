# -*- coding: utf-8 -*-
from copy import copy

from .exceptions import NoMapCreateMethodException, NoMapPKField
from .models import RecordLink

pathways = []


def pathway(have_model, need_model):
    def pathway_decorator(func):
        pathways.append({'have': have_model, 'need': need_model, 'pathway': func})

        return func

    return pathway_decorator


class FieldMap(object):
    name = None  #: Legacy field name
    pk = False  #: Is this field a pk?
    fk = False  #: Is this field a fk?
    foreign_map = None  #: TableMap to foreign record
    converter = None  #: Function to convert the old value to the new value
    model_class = None  #: Model class different from the tables model class
    model_field = None  #: Models field name
    default = None  # todo: not implemented yet

    def __init__(self, value=None):
        self.value = value

    def set_value(self, value):
        self.value = value

    def get_value(self):
        if self.converter and hasattr(self.converter, '__call__'):
            return self.converter(self.value)
        return self.value


def field_map(name, pk=False, fk=False, foreign_map=None, converter=None,
              model_class=None, model_field=None, default=None):
    attrs = {'name': name, 'pk': pk, 'fk': fk, 'foreign_map': foreign_map, 'converter': converter,
             'model_class': model_class, 'model_field': model_field, 'default': default}
    return type('%sFieldMap' % name, (FieldMap,), attrs)


class TableMap(object):
    """
    TableMap is the base for all table mappings from the legacy manager to Version 2.  It requires a table name
    and model class type.
    """
    table_name = None  #: Legacy systems table name
    model_class = None  #: Django's model class
    fields = ()  #: Tuple of fields to load

    def __new__(cls, *args, **kwargs):
        return super(TableMap, cls).__new__(cls, *args, **kwargs)

    def __init__(self, row, cmd=None):
        self.cmd = cmd

        # Error checking
        if not self.model_class:
            raise ValueError("No model_class defined.")
        if len(self.fields):
            raise ValueError("No fields defined.")
        if len(row) == 0:
            raise ValueError("Row has no fields.")

        # init the fields
        self.pk_fields = []  # Legacy pk column
        self.fk_fields = {}  # Foreign key fields
        self.local_fields = {}  # Local table fields
        self.foreign_fields = {}  # Non local fields
        for field in self.fields:
            # if not field.model_field:
            #     field.model_field = str(field.name)
            instance_field = copy(field)

            # add to pk list
            if field.pk:
                self.pk_fields.append(instance_field)
                # does the row contain the pk fields?
                if field.name not in row:
                    raise NoMapPKField

            # add to foreign key list
            if field.fk and field.foreign_map:
                if field.foreign_map.table_name not in self.fk_fields.keys():
                    self.fk_fields.update({field.foreign_map.table_name: []})
                self.fk_fields.get(field.foreign_map.table_name).append(field)

            # add to local list
            if (not field.fk) and field.model_field:
                dict_update = {instance_field.name: instance_field}
                if field.model_class:
                    self.local_fields.update(dict_update)
                else:
                    self.foreign_fields.update(dict_update)



        # for name, field in self.__class__.__dict__.iteritems():
        #     if isinstance(field, FieldMap):
        #         if not field.model_field:
        #             field.model_field = str(name)
        #         instance_field = copy(field)
        #         self.fields[field.name] = instance_field
        #
        #         if field.pk:
        #             self.pk_fields.append(instance_field)
        #             # does the row contain the pk fields?
        #             if field.name not in row:
        #                 raise NoMapPKField
        #         if field.name in row:
        #             instance_field.value = row[field.name]

        if (len(self.fk_fields) + len(self.local_fields) + len(self.foreign_fields)) == 0:
            raise ValueError("No stored fields defined.")
        if len(self.pk_fields) == 0:
            raise ValueError("No pk fields defined.")

        # sort the pks by name
        self.pk_fields.sort(key=lambda x: x.name)

        # create the legacy lookup pk field and value
        pk_field = []
        pk_key = []
        for field in self.pk_fields:
            pk_field.append(field.name)
            pk_key.append(str(row[field.name]))
        self._pk_field = "|".join(pk_field)
        self._pk_value = "|".join(pk_key)

        self.model = self.get_model()

    def migrate(self):
        for field in self.fields.itervalues():
            if not field.pk:
                if self.cmd:
                    self.cmd.stdout.write(".", ending=False)
                if hasattr(self.model, field.model_field) and field.value:
                    setattr(self.model, field.model_field, field.value)

        self.model.save()

        if self.cmd:
            self.cmd.stdout.write(self.cmd.style.MIGRATE_SUCCESS(" Saved"))

    def get_model_class(self):
        """
        Returns the model class.
        """
        return self.model_class

    def get_table_name(self):
        """
        Returns the legacy systems table name.
        """
        return self.table_name

    def get_model(self):
        """
        Will return from the database or creates a new one.

        :return: Returns a instance of `self.model_class`.
        """
        model = None
        # Get link record
        create_status = None
        try:
            model = RecordLink.objects.get(legacy_table=self.table_name,
                                           legacy_pk_field=self._pk_field,
                                           legacy_pk_value=self._pk_value).content_object
            create_status = self.cmd.style.MIGRATE_HEADING("Found")
        except RecordLink.DoesNotExist:
            model = self.create_model()
            model.save()  # in case model comes unsaved.
            # create RecordLink
            record_link = RecordLink(legacy_table=self.table_name,
                                     legacy_pk_field=self._pk_field,
                                     legacy_pk_value=self._pk_value)
            record_link.content_object = model
            record_link.save()

        if self.cmd:
            create_status = self.cmd.style.MIGRATE_HEADING("New")
            self.cmd.stdout.write(
                "  %(model)s (%(model_pk)s) : %(table)s (%(table_pk)s) " % {'model': model.__class__.__name__,
                                                                            'model_pk': model.pk,
                                                                            'table': self._pk_field,
                                                                            'table_pk': self._pk_value,
                                                                            },
                ending=False)
            if create_status:
                self.cmd.stdout.write(create_status, ending=False)

        return model

    def create_model(self):
        """
        Define how to recreate a new object from model_class.
        """
        return self.get_model_class()()
