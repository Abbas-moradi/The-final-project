from rest_framework import serializers
from .models import User, OtpCode, Address


"""
this UserSerializer is configured to work with the User model,
include all fields in the serialization, and mark the 'password' field
as write-only, ensuring that it's not exposed in API responses.
"""

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
    

    def validate_full_name(self, value):
        if 'admin' in value:
            raise serializers.ValidationError('Admin should not be in the full name')


class OtpCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpCode
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'