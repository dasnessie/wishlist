from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:wish_id>/buy/', views.buy, name='buy'),
    path('bought/<str:secret>', views.bought, name='bought'),
]
