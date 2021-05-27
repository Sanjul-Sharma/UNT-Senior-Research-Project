"""
    Created by Sanjul Sharma on April 22, 2021
    All rights reserved. Copyright © 2021.
"""

__author__ = "Sanjul Sharma"

from .apps import INSTALLED_APPS
from .database import DATABASES
from .celery_config import *

__all__ = ["INSTALLED_APPS",
           "DATABASES",
           "BROKER_URL",
           "CELERY_IMPORTS",
           "CELERY_RESULT_BACKEND",
           "CELERY_ACCEPT_CONTENT",
           "CELERY_TASK_SERIALIZER",
           "CELERY_RESULT_SERIALIZER",
           "CELERY_TIMEZONE",
           "CELERYBEAT_SCHEDULE",
           "CELERYD_TASK_SOFT_TIME_LIMIT",
           "CELERYD_TASK_TIME_LIMIT"
           ]
