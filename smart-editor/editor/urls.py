"""
    Created by Sanjul Sharma on April 22, 2021
    All rights reserved. Copyright © 2021.
"""
from django.conf.urls import url
from django.conf.urls.static import static

import settings
from editor.views import RichTextView, CheckKeyValidityView

__author__ = "Sanjul Sharma"

urlpatterns = [
    url(r'^$', RichTextView.as_view(), name="home"),
    url(r'^editor/$', RichTextView.as_view(), name="rich_text_edit"),
    url(r'^check-key-validation/$', CheckKeyValidityView.as_view(), name="check_key_validity"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
