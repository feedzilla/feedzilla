# -*- coding: utf-8 -*-
from django import forms
from django.core.mail import mail_admins
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from feedzilla.models import Request

class AddBlogForm(forms.Form):
    url = forms.URLField(label=_('Site URL'))

    def clean_url(self):
        value = self.cleaned_data['url']
        try:
            Request.objects.get(url=value)
        except Request.DoesNotExist:
            return value
        else:
            raise forms.ValidationError(_('This address has been already submitted.'))

    def save(self):
        url = self.cleaned_data['url']
        obj = Request.objects.create(url=url)
        body = _('New submission for the planet: %s') % url
        mail_admins(_('%s: new submission') % settings.FEEDZILLA_SITE_TITLE, body)
        return obj
