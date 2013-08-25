from django.conf.urls import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', TemplateView.as_view(template_name='home.html'), name='home_page'),
    url(r'', include('feedzilla.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
