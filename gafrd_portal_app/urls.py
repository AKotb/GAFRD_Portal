from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('contactus/', views.contactus, name='contactus'),
    path('services/', views.services, name='services'),
    path('elibrary/', views.elibrary, name='elibrary'),
    path('model_call/', views.model_call, name='model_call'),
    path('run_clip_polygon/', views.run_clip_polygon, name='run_clip_polygon'),
    path('download_shapefile/', views.download_shapefile, name='download_shapefile'),
    path('contactus_response/', views.contactus_response, name='contactus_response')
]
