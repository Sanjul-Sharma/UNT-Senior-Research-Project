"""
    Created by Sanjul Sharma on April 22, 2021
    All rights reserved. Copyright © 2021.
"""
from enum import Enum

from django.db import models

__author__ = "Sanjul Sharma"


class EditorStatus(Enum):
    empty = 0
    encrypted = 1
    decrypted = 2


class RichText(models.Model):
    editor_text = models.TextField(null=True, blank=True, default="")
    key = models.TextField(null=True, blank=True, default=None)
    editor_status = models.SmallIntegerField(default=0)  # EditorStatus
    key_inserted_on = models.BigIntegerField(default=0)
    key_expired = models.BooleanField(default=False)
    key_file_name = models.CharField(max_length=512, default=None, null=True)

    class Meta:
        app_label = "editor"
