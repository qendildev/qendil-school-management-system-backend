from rest_framework import serializers
from .models import Holiday

class HolidaySerializer(serializers.ModelSerializer):
    duration_days = serializers.ReadOnlyField()

    class Meta:
        model = Holiday
        fields = '__all__'
