from rest_framework import serializers
from .models import Image
from rest_framework import serializers
from .models import ImageHistory

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'name')
        


class ImageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageHistory
        fields = ['image_number', 'is_accepted', 'timestamp']