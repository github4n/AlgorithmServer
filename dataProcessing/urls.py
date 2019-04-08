


from django.urls import path

from . import views

urlpatterns = [
    path('getFenciWord', views.getFenciWord, name='getFenciWord'),
]