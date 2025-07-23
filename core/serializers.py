from djoser.serializers import UserSerializer as BaseUserSerializer,  UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
class UserCreateSerializer(BaseUserCreateSerializer):
    
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']

class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'email', 'username', 'first_name', 'last_name']

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        # Check old password
        if not self.context['request'].user.check_password(data.get('old_password')):
            raise serializers.ValidationError({'old_password': 'Wrong password.'})
        
        # Validate new password
        try:
            validate_password(data.get('new_password'), self.context['request'].user)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        
        return data