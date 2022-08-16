from django.shortcuts import render
from email.message import Message
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from django.shortcuts import render, redirect
from .models import Bus
# from knox.models import AuthToken
from django.contrib.auth.models import User
from .serializers import BusViewSerializer, CreateBusSerializer
from rest_framework import generics
from django.views import generic
from rest_framework.permissions import IsAuthenticated , AllowAny
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from rest_framework.permissions import IsAuthenticated , AllowAny
# Create your views here.


# add a bus to the list view.
class CreateBusView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CreateBusSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # if a user is manager then he can add a bus to the list.
        if self.requst.user.is_manager:
            response = {
                "success": True,
                "user": CreateBusSerializer(Bus, context=self.get_serializer_context()).data,
                "status code": status.HTTP_200_OK,
                "message": "Bus registered successfully",
            }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)
    


## Get the bus Information.

class GetBusView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BusViewSerializer
    # if a user is a user, then he can see the list of bus.
    
    def get(self, request):
        if self.request.user.is_user:
            serializer = self.serializer_class(request.user)
        return Response(serializer.data)
    
    

#### CRUD + L operations for Products #####



# Buses List view 
class BustListView(generic.ListView):
    template_name = "bus/buslist.html"
    context_object_name = "bus"
    def get(self, request, *args, **kwargs):
        
        if self.request.user.is_user:
            bus = Bus.objects.filter(soft_delete=True)
            return render(request, self.template_name, {'bus': bus})
       
       
       

class BusDetailView(generic.DetailView):
    template_name = "bus/bus_detail.html"
    context_object_name = 'bus'
    model = Bus
    success_url = reverse_lazy("bus:bus-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context