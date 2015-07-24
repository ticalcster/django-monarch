# -*- coding: utf-8 -*-
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string, import_module

from .mapping import TableMap
from .exceptions import NoMapPKField

class MigrationRunner(object):
    def __init__(self, settings=None, tables=None, cmd=None):
        self.settings = self._get_settings(settings)
        self.cmd = cmd
        self.maps = []

        # Runner Setup
        if self.cmd:
            self.cmd.stdout.write(self.cmd.style.MIGRATE_HEADING("Monarch setup:"))

        self.monarch_maps = self.load_monarch_maps()

        if not self.maps:
            self.maps = self.get_migration_model_list(self.monarch_maps)

        if self.cmd:
            self.cmd.stdout.write(self.cmd.style.MIGRATE_LABEL("  Run migrations for: "), ending=False)
            self.cmd.stdout.write(", ".join(self.tables))

    def run(self, connection=None):
        pass
        # if self.cmd:
        #     self.cmd.stdout.write(self.cmd.style.MIGRATE_HEADING("Running migrations: "))
        #
        # connection_class = None
        # if connection:
        #     connection_class = connection
        # else:
        #     connection_class = get_connection_class()
        #
        # self.connection = connection_class(self.settings, cmd=self.cmd) # JSONConnection(self.settings, cmd=self.cmd)  # Not sure how to configure this
        #
        # for table_name in self.tables:
        #     # Check if it's a valid table
        #     if not self.monarch_tables.has_key(table_name):
        #         self.cmd.stdout.write(self.cmd.style.MIGRATE_FAILURE("  No migration model for table %s." % table_name))
        #         continue
        #
        #     table_hash = self.connection.fetch(table=table_name)
        #
        #     if table_hash.get('error'):
        #         if self.cmd:
        #             self.cmd.stdout.write(self.cmd.style.MIGRATE_FAILURE("  Error: %s." % table_hash['error']))
        #         continue
        #
        #     if not table_hash.get('rows'):
        #         if self.cmd:
        #             self.cmd.stdout.write(self.cmd.style.MIGRATE_FAILURE("  No rows for: %s." % table_name))
        #         continue
        #
        #     for row in table_hash['rows']:
        #         try:
        #             model_map = self.monarch_tables[table_name](row, cmd=self.cmd)
        #             model_map.migrate()
        #         except NoMapPKField, e:
        #             if self.cmd:
        #                 self.cmd.stdout.write("%s: %s" % (table_name, self.cmd.style.MIGRATE_FAILURE(e.message)))
        #
        # if self.cmd:
        #     self.cmd.stdout.write(self.cmd.style.MIGRATE_HEADING("Should have done something awesome!"))

    def get_apps_with_maps(self):
        from django.apps import apps
        apps_with_maps = []
        for app_config in apps.get_app_configs():
            try:
                mod = import_module("%s.monarch_maps" % app_config.module.__name__)
                apps_with_maps.append(app_config.label)
            except:
                pass
        return apps_with_maps

    def load_monarch_maps(self):
        apps_with_maps = self.get_apps_with_maps()

        if self.cmd:
            self.cmd.stdout.write(self.cmd.style.MIGRATE_LABEL("  Monarch tables loaded from: "), ending=False)
            self.cmd.stdout.write(", ".join(apps_with_maps))

        monarch_tables = {}
        for class_ in TableMap.__subclasses__():
            monarch_tables[class_.table_name] = class_
        return monarch_tables

    def get_migration_model_list(self, monarch_tables):
        migration_list = []
        for name in monarch_tables:
            migration_list.append(name)
        return migration_list

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


