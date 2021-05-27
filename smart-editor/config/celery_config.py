from __future__ import absolute_import
"""
    Created by Sanjul Sharma on April 22, 2021
    All rights reserved. Copyright © 2021.
"""

__author__ = "Sanjul Sharma"


BROKER_URL = 'redis://localhost:6379'
CELERY_IMPORTS = ('editor.tasks', )
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERYBEAT_SCHEDULE = {}
CELERYD_TASK_SOFT_TIME_LIMIT = 120 * 60
CELERYD_TASK_TIME_LIMIT = 150 * 60
