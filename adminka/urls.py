from django.urls import path
from adminka import views

urlpatterns = [
    path('', views.adminka_home, name='adminka_home'),

]