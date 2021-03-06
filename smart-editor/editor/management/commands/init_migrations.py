"""
    Created by Sanjul Sharma on April 22, 2021
    All rights reserved. Copyright © 2021.
"""

__author__ = "Sanjul Sharma"


import inspect
import os

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.requires_model_validation = False

    def pred(self, c):
        return inspect.isclass(c) and c.__module__ == self.pred.__module__

    def handle(self, *args, **options):
        INSTALLED_APPS = settings.PROJECT_APPS

        for x in INSTALLED_APPS:
            if os.path.exists(x.replace('.', os.sep)):
                v = os.path.join(x.replace('.', os.sep), 'migrations')
                if not os.path.isdir(v) and not os.path.exists(v):
                    self.stdout.write('Creating migration folder for ....' + v)
                    os.makedirs(v)
                open(os.path.join(v, '__init__.py'), 'w').close()
        self.stdout.write('Migrations folders added.')
