
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta():
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'other_name', 'password']


        def create(self, validated_data):
            user = User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                other_name=validated_data['other_name']
            )

            return user

