from django.urls import path

from . import views

app_name = 'tp3'
urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.generate_series, name='generate_series'),
]