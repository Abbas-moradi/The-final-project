from rest_framework import serializers
from .models import User, OtpCode, Address


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
                        'email': {'read_only': True},
                        'phone_number':{'read_only':True}
                        }


class OtpCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtpCode
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'