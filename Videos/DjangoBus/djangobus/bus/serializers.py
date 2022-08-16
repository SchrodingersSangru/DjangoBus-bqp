from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Bus


class CreateBusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bus
        fields = '__all__'
        
        
    def create_bus(self, validated_data):
        # creating a bus serializer 
        bus = Bus.objects.create()
        bus.save()
        
        return bus
        

class BusViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'