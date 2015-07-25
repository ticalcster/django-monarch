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
    def __init__(self, name, pk=False, converter=None, model_class=None, model_field=None):
        self.name = name
        self.pk = pk
        self.converter = converter
        self.model_class = model_class
        self.model_field = None
        self.value = None


class TableMap(object):
    """
    TableMap is the base for all table mappings from the legacy manager to Version 2.  It requires a table name
    and model class type.
    """
    table_name = None
    model_class = None

    def __init__(self, row, cmd=None):
        # Error checking
        if not self.table_name:
            raise ValueError("No table_name defined.")
        if not self.model_class:
            raise ValueError("No model_class defined.")
        if len(row) == 0:
            raise ValueError("Row has no fields.")

        self.cmd = cmd

        # init the fields
        self.fields = {}
        self.pk_fields = []
        for name, field in self.__class__.__dict__.iteritems():
            if isinstance(field, FieldMap):
                if not field.model_field:
                    field.model_field = str(name)
                instance_field =  copy(field)
                self.fields[field.name] = instance_field

                if field.pk:
                    self.pk_fields.append(instance_field)
                    # does the row contain the pk fields?
                    if field.name not in row:
                        raise NoMapPKField
                if field.name in row:
                    instance_field.value = row[field.name]

        if len(self.fields) == 0:
            raise ValueError("No fields defined.")
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

    def get_model(self):
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
            create_status = self.cmd.style.MIGRATE_HEADING("New")

        if self.cmd:
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
        raise NotImplementedError
