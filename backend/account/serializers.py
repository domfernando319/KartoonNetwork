from .models import User, FriendRequest
from rest_framework import serializers

# these serializers are used to convert Django models (ie User and FriendRequest)
# into a format suitable for rendering as JSON responses

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'friends_count',)

class FriendRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = FriendRequest
        fields = ('id', 'created_by',)