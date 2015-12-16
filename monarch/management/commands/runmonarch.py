# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError

from monarch.runners import MigrationRunner
from monarch.connectors import HttpJsonConnector

class Command(BaseCommand):
    help = 'Import data from Manager.'

    def add_arguments(self, parser):
        parser.add_argument('tables', nargs='*')
        parser.add_argument('--runner', nargs='?', help="Monarch runner Class.")

    def handle(self, *args, **options):
        if not settings.MONARCH_SETTINGS:
            raise ImproperlyConfigured('No Monarch settings found.')
        monarch_settings = settings.MONARCH_SETTINGS['default']['SETTINGS']

        runner = MigrationRunner(cmd=self)
        runner.run(connection=HttpJsonConnector)

