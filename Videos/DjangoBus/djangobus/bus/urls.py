from django.urls import path
from . import views

urlpatterns = [
    path('create_bus/', views.CreateBusView.as_view(), name='create'),
    path('view_buses/', views.GetBusView.as_view(), name='view-bus'),
    #create a bus url
    path('bus_list/', views.BustListView, name = "bus-list"), # view a bus list
    path('bus/<int:pk>/details', views.BusDetailView, name = "bus-details"), #bus details 
]