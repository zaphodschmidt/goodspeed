from rest_framework import serializers
from .models import * 

class VertexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vertex
        fields = '__all__'

class ParkingSpotSerializer(serializers.ModelSerializer):
    vertices = VertexSerializer(many=True, read_only=True)

    class Meta:
        model = ParkingSpot
        fields = '__all__'

class CameraSerializer(serializers.ModelSerializer):
    parking_spots = ParkingSpotSerializer(many=True, read_only=True)

    class Meta:
        model = Camera
        fields = '__all__'

class BuildingSerializer(serializers.ModelSerializer):
    cameras = CameraSerializer(many=True, read_only=True)
    
    class Meta:
        model = Building
        fields = '__all__'
