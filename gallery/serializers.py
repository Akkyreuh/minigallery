from rest_framework import serializers
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()
    source = serializers.SerializerMethodField()
    
    class Meta:
        model = Image
        fields = ['id', 'title', 'url', 'image_file', 'image_url', 'source', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_source(self, obj):
        if obj.url:
            return 'ImgBB'
        elif obj.image_file:
            return 'Local'
        return 'Unknown'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        if instance.image_file and not instance.url:
            request = self.context.get('request')
            if request:
                data['image_url'] = request.build_absolute_uri(instance.image_file.url)
        
        return data

