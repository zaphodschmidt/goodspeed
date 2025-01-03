from rest_framework import serializers
from .models import * 


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'image_url', 'uploaded_at']
    
    def get_image_url(self,obj):
        return self.context['request'].build_absolute_uri(obj.image.url)
    

class VertexSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vertex
        fields = '__all__'
        extra_kwargs = {
            'spot': {'required': False}
        }


class ParkingSpotSerializer(serializers.ModelSerializer):
    vertices = VertexSerializer(many=True, required=False)

    class Meta:
        model = ParkingSpot
        fields = '__all__'

    def create(self, validated_data):
        # Extract vertices data if provided
        vertices_data = validated_data.pop('vertices', None)

        # Create parking spot instance
        new_parking_spot_obj = super().create(validated_data)

        # Define defaults for vertex positions
        DEFAULT_LEFT = 30
        DEFAULT_RIGHT = 70
        DEFAULT_TOP = 30
        DEFAULT_BOTTOM = 70

        # Create default vertices if no vertices data is provided
        if not vertices_data:
            Vertex.objects.create(spot=new_parking_spot_obj, x=DEFAULT_LEFT, y=DEFAULT_TOP)
            Vertex.objects.create(spot=new_parking_spot_obj, x=DEFAULT_RIGHT, y=DEFAULT_TOP)
            Vertex.objects.create(spot=new_parking_spot_obj, x=DEFAULT_LEFT, y=DEFAULT_BOTTOM)
            Vertex.objects.create(spot=new_parking_spot_obj, x=DEFAULT_RIGHT, y=DEFAULT_BOTTOM)
        else:
            # Create vertices based on provided data
            for vertex_data in vertices_data:
                Vertex.objects.create(spot=new_parking_spot_obj, **vertex_data)

        return new_parking_spot_obj
        

    def update(self, instance, validated_data):
        #Extract vertices data
        vertices_data = validated_data.pop('vertices', [])

        #Update this parking spot
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        #Update each vertice individually
        # for vertex_data in vertices_data:
        #     vertex_id = vertex_data.get('id')
        #     existing_vertex_object= Vertex.objects.get(id=vertex_id) 
        #     vertex_serializer_instance = VertexSerializer(existing_vertex_object, data=vertex_data)
        #     vertex_serializer_instance.is_valid(raise_exception=True)
        #     vertex_serializer_instance.save()

        instance.save()

        return instance
        

class CameraSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    parking_spots = ParkingSpotSerializer(many=True, read_only=True)

    class Meta:
        model = Camera
        fields = '__all__'

class BuildingSerializer(serializers.ModelSerializer):
    cameras = CameraSerializer(many=True, read_only=True)
    
    class Meta:
        model = Building
        fields = '__all__'
