from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', CoinListView.as_view(),{'haveOnly':1},name='collection'),
    url(r'^whish/$', CoinListView.as_view(),{'haveOnly':0},name='whishlist'),
    url(r'^add/$', CoinCreateView.as_view(),name='register'),
    url(r'^(?P<slug>[\w-]+)/$',CoinDetailView.as_view(),name='view'),
    url(r'^(?P<slug>[\w-]+)/update/$',CoinUpdateView.as_view(),name='update'),
]