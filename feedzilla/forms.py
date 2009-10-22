# -*- coding: utf-8 -*-
from django import forms
from django.core.mail import mail_admins

from feedzilla.models import Request
from feedzilla import settings as app_settings

class AddBlogForm(forms.Form):
    url = forms.URLField()

    def clean_url(self):
        value = self.cleaned_data['url']
        try:
            Request.objects.get(url=value)
        except Request.DoesNotExist:
            return value
        else:
            raise forms.ValidationError(u'Заявка для этого адреса уже была отправлена')

    def save(self):
        url = self.cleaned_data['url']
        obj = Request.objects.create(url=url)
        body = u'Новая заявка для планеты: %s' % url
        mail_admins(u'%s: новая заявка' % app_settings.SITE_TITLE, body)
        return obj
