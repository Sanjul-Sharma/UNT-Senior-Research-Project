"""
    Created by Sanjul Sharma on April 22, 2021
    All rights reserved. Copyright © 2021.
"""
from copy import deepcopy

from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from editor.forms import RichTextForm
from editor.mixin.json_mixin import JsonMixin
from editor.models import RichText

__author__ = "Sanjul Sharma"


class RichTextView(FormView, JsonMixin):
    form_class = RichTextForm

    def get_template_names(self):
        return ["base/base.html"]

    def get_success_url(self):
        return "/editor/"

    def get_context_data(self, **kwargs):
        context = super(RichTextView, self).get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['header'] = "Smart Editor"
        context["object"] = RichText.objects.first()
        return context

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(RichTextView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request=request, template_name=self.get_template_names(), context=self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        try:
            key_validation = request.GET.get("key_validation")
            if int(key_validation) == 1:
                pk_ = request.POST.get("pk", None)
                key_ = request.POST.get("key", None)
                if int(pk_) and key_:
                    rich_text_inst = RichText.objects.filter(pk=pk_, key=key_).first()
                    if rich_text_inst:
                        messages.success(request, "Decrypted successfully.")
                        return self.render_json_response(context={"result": "Success", "data": {
                            "msg": "Decrypted successfully."}})
            return self.render_to_response(context={"result": "Error", "message": "Key is invalid!!!"})
        except Exception as exp:
            pass
        pk_ = request.POST.get("pk", None)
        inst = RichText.objects.get(pk=pk_) if pk_ else None
        form = self.form_class(instance=inst)
        form.is_valid()
        instance_ = form.save(instance=inst, **request.POST)
        try:
            return self.render_json_response(context={"result": "Success", "data": {
                "msg": "Encrypted successfully.", "editor_text": instance_.editor_text, "pk": instance_.pk,
                "key_expired": instance_.key_expired}})
        except Exception as exp:
            return self.form_invalid(form)
