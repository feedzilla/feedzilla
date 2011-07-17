# -*- coding: utf-8 -*-
# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD
from django import forms
from django.core.mail import mail_admins
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from feedzilla.models import Request

class AddBlogForm(forms.ModelForm):
    class Meta:
        model = Request

    def clean_url(self):
        url = self.cleaned_data['url']
        try:
            Request.objects.get(url=url)
        except Request.DoesNotExist:
            return url
        else:
            raise forms.ValidationError(_('This address has been already submitted.'))
