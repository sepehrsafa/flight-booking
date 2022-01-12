from rest_framework import serializers
from app1.models import irantrainstations
class irantrainstationsserializer(serializers.ModelSerializer):
    class Meta:
        model = irantrainstations
        fields = ['StationCode', 'StationNameFarsi', 'StationNameFarsi2', 'StationNameEnglish']