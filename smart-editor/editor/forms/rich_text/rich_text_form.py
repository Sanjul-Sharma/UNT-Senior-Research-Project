"""
    Created by Sanjul Sharma on April 22, 2021
    All rights reserved. Copyright © 2021.
"""
from datetime import datetime

from django import forms
from django.db import transaction
from django.forms import Textarea

from editor.models.rich_text.rich_text import EditorStatus
from editor.models import RichText

__author__ = "Sanjul Sharma"


class RichTextForm(forms.Form):
    def __init__(self, instance=None, *args, **kwargs):
        super(RichTextForm, self).__init__(*args, **kwargs)
        self.fields["editor_text"] = forms.CharField(
            label="", required=True,
            initial=instance.editor_text if instance else "",
            widget=Textarea(
                attrs={
                    'class': 'form-control rich-text-area',
                    'placeholder': "",
                }
            ), help_text=""
        )

    @staticmethod
    def save(instance=None, **kwargs):
        with transaction.atomic():
            data_ = {"editor_text": kwargs.get("editor_text", "")[0], "key": kwargs.get("key", None)[0],
                     "key_inserted_on": int(datetime.now().timestamp() * 1000), "key_expired": False,
                     "editor_status": EditorStatus.encrypted.value,
                     "key_file_name": kwargs.get("key_file_name", None)[0]}
            if instance is None:
                instance = RichText(**data_)
            else:
                for f_, v_ in data_.items():
                    setattr(instance, f_, v_)
            instance.save()
            return instance

    class Meta:
        model = RichText
        fields = "editor_text",
