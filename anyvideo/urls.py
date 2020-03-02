from django.urls import path
from anyvideo import views
# from django.urls import re_path


urlpatterns = [
    path('', views.home, name='anyhome'),
    path('download/', views.anydownload, name='anydownload')

]
