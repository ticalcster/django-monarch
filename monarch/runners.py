# -*- coding: utf-8 -*-
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string, import_module

# django <= 1.6 import_by_path
# django >= 1.7

from .mapping import TableMap
from .exceptions import NoMapPKField


class MigrationRunner(object):
    def __init__(self, settings=None, maps=None, cmd=None):
        self.settings = self._get_settings(settings)
        self.apps_with_maps = self._get_apps_with_maps()
        self.monarch_maps = self._get_monarch_maps()
        self.cmd = cmd
        self.maps = maps
        if not self.maps:
            # Load all know maps if non are given
            self.maps = self._get_monarch_map_keys()
        self.connection = None
        self._init_connectors(self.settings)

        # Runner Setup
        if self.cmd:
            self.cmd.stdout.write(self.cmd.style.MIGRATE_HEADING("Monarch setup:"))
            self.cmd.stdout.write(self.cmd.style.MIGRATE_LABEL("  Monarch tables loaded from: "), ending=False)
            self.cmd.stdout.write(", ".join(self.apps_with_maps))
            self.cmd.stdout.write(self.cmd.style.MIGRATE_LABEL("  Run migrations for: "), ending=False)
            self.cmd.stdout.write(", ".join(self.maps))

    def run(self, connection=None):
        if self.cmd:
            self.cmd.stdout.write(self.cmd.style.MIGRATE_HEADING("Running migrations: "))

        connection_class = None
        if connection:
            connection_class = connection
        else:
            raise ImproperlyConfigured('No connection class given.')

        self.connection = connection_class(self.settings['default']['SETTINGS'],
                                           cmd=self.cmd)  # JSONConnection(self.settings, cmd=self.cmd)  # Not sure how to configure this

        for table_name in self.maps:
            # Check if it's a valid table
            if not self.monarch_maps.has_key(table_name):
                self.cmd.stdout.write(self.cmd.style.MIGRATE_FAILURE("  No migration model for table %s." % table_name))
                continue

            table_hash = self.connection.fetch(table=table_name)

            if table_hash.get('error'):
                if self.cmd:
                    self.cmd.stdout.write(self.cmd.style.MIGRATE_FAILURE("  Error: %s." % table_hash['error']))
                continue

            if not table_hash.get('rows'):
                if self.cmd:
                    self.cmd.stdout.write(self.cmd.style.MIGRATE_FAILURE("  No rows for: %s." % table_name))
                continue

            for row in table_hash['rows']:
                try:
                    model_map = self.monarch_maps[table_name](row, cmd=self.cmd)
                    model_map.migrate()
                except NoMapPKField, e:
                    if self.cmd:
                        self.cmd.stdout.write("%s: %s" % (table_name, self.cmd.style.MIGRATE_FAILURE(e.message)))

        if self.cmd:
            self.cmd.stdout.write(self.cmd.style.MIGRATE_HEADING("Should have done something awesome!"))
            print

    # def _get_monarch_class(self, name):
    #     monarch_tables = {}
    #     for class_ in TableMap.__subclasses__():
    #         if class_.__name__:
    #             return class_
    #     raise NotImplementedError("{0} was not found.".format(name))

    def _get_apps_with_maps(self):
        from django.apps import apps
        apps_with_maps = []
        for app_config in apps.get_app_configs():
            try:
                mod = import_module("%s.monarch_maps" % app_config.module.__name__)
                apps_with_maps.append(app_config.label)
            except:
                pass
        return apps_with_maps

    def _get_monarch_maps(self):
        monarch_tables = {}
        for class_ in TableMap.__subclasses__():
            if class_.table_name:
                monarch_tables[class_.table_name] = class_
        return monarch_tables

    def _get_monarch_map_keys(self):
        # TODO: is there a python builtin to do this?
        key_list = []
        for name in self.monarch_maps:
            key_list.append(name)
        return key_list

    def _get_settings(self, monarch_settings):
        _settings = {}
        if monarch_settings:
            _settings = monarch_settings
        else:
            # load from django settings
            from django.conf import settings
            if not settings.MONARCH_SETTINGS:
                raise ImproperlyConfigured('No monarch settings.')
            _settings = settings.MONARCH_SETTINGS

        if 'default' in _settings:
            if 'CONNECTOR' in _settings['default']:
                return _settings
            raise ImproperlyConfigured('No CONNECTOR in default settings.')
        raise ImproperlyConfigured('No default monarch settings.')

    def _init_connectors(self, settings):
        connectors = {}
        for connector in settings.itervalues():
            class_ = import_string(connector['CONNECTOR'])
            connector['connector'] = 'TEST'
