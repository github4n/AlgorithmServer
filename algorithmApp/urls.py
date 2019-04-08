


from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('participle', views.participle, name='index'),
    path('similar', views.similar, name='similar'),
    path('getCompany',views.getCompany,name='getCompany'),
    path('download',views.download,name='download'),
    path('correctArea',views.correctArea,name='correctArea'),
    path('polarityEn',views.polarityEn,name='polarityEn'),
    path('autoSelect',views.autoSelect,name='autoSelect'),
    path('findLongest',views.findLongest,name='findLongest')
]