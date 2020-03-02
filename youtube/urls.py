from django.urls import path
from youtube import views
# from django.urls import re_path


urlpatterns = [
    path('', views.home, name='home'),
    path('download/', views.download, name='download'),
    path('about-us/', views.about, name='about'),
    path('privacy-policy/', views.policy, name='policy'),
    path('terms-conditions/', views.terms, name='terms'),
]
