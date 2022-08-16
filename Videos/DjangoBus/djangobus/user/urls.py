
from django.urls import path
from . import views

urlpatterns = [
    
    path('about/', views.about, name='about'),
    path('', views.WelcomeView.as_view(), name='Welcome'),
]