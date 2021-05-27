"""
    Created by Sanjul Sharma on April 22, 2021
    All rights reserved. Copyright © 2021.
"""
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from editor.mixin.json_mixin import JsonMixin
from editor.models import RichText

__author__ = "Sanjul Sharma"


class CheckKeyValidityView(View, JsonMixin):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(CheckKeyValidityView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        pk_ = kwargs.get("pk", request.POST.get("pk"))
        key_ = kwargs.get("key", request.POST.get("key"))
        rich_text = RichText.objects.filter(pk=pk_).values("key", "key_expired").first()
        if rich_text:
            if rich_text.get("key") is None:
                return self.render_json_response(context={"result": "Success", "data": True})
            elif rich_text.get("key") == key_ and rich_text.get("key_expired"):
                return self.render_json_response(context={"result": "Success", "data": True})
        return self.render_json_response(context={"result": "Success", "data": False})
