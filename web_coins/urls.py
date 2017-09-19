from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from coins.views import *
from .views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^learn/$', lrn_links,name='darkness'),
    url(r'^learn/simple/$', lrn_home_old),
    url(r'^learn/inheritance/$', lrn_inheritance),
    url(r'^learn/nosnips/$', lrn_home_learning),

    url(r'^coins/',include('coins.urls',namespace='coins')),

    url(r'^$', TemplateView.as_view(template_name="index.html"),name='home'),
    url(r'^about/$', TemplateView.as_view(template_name="about.html"),name='about'),
    #url(r'^coins/(?P<country>\w+)/$',CoinListView.as_view()),#search
    url(r'^login/$', LoginView.as_view(template_name="login.html"),name='login'),
]
if settings.DEBUG is True:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)