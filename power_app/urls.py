from django.urls import path
from . import views

urlpatterns = [
    path('', views.solar_energy_prediction, name='solar_energy_prediction'),
    path('model/', views.model_page, name='model_page'),
    path('idea/', views.idea_page, name='idea_page'),
    path('input/', views.input_page, name='input_page'),
    path('about_us/', views.about_us_page, name='about_us_page'),

    
]
