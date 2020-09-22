"""
defines the urls to serve
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:wish_id>/buy/', views.buy, name='buy'),
    path('<int:wish_id>/nick_entry/', views.nick_entry, name='nick_entry'),
    path('bought/<str:secret>', views.bought, name='bought'),
    path('unbuy/<str:secret>', views.unbuy, name='unbuy'),
    path('nospoiler', views.index, {'nospoiler': True}, name='nospoiler'),
    path('buyerror', views.buyerror, name='buyerror'),
    path('stats', views.stats, name='stats'),
]
