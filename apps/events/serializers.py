from rest_framework import serializers
from .models import Event, EventRSVP
from apps.authentication.serializers import UserSerializer

class EventSerializer(serializers.ModelSerializer):
    organizer_details = UserSerializer(source='organizer', read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('organizer', 'is_published')

class EventRSVPSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = EventRSVP
        fields = '__all__'
        read_only_fields = ('user',)

class RSVPActionSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=EventRSVP.STATUS_CHOICES)
