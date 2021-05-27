"""
    Created by Sanjul Sharma on April 22, 2021
    All rights reserved. Copyright © 2021.
"""
from json import JSONEncoder

from django.http import HttpResponse

__author__ = "Sanjul Sharma"


class JsonMixin(object):
    def render_json_response(self, context):
        return self.get_json_response(self.convert_context_to_json(context=context))

    def get_json_response(self, content, **kwargs):
        return HttpResponse(content=content, content_type='application/json', **kwargs)

    def convert_context_to_json(self, context):
        encoder = JSONEncoder()
        return encoder.encode(context)
