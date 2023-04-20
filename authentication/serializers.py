from rest_framework import serializers
from django.contrib.auth.models import User

from authentication.models import MyUser


# from .models import User


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email', 'firstname', 'lastname', 'gender')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'firstname', 'lastname', 'gender', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = MyUser.objects.create_user(validated_data['username'], validated_data['email'],
                                          validated_data['password'], firstname = validated_data['firstname'],
                                          validated_data['lastname'], validated_data['gender']))

        return user
#
# from rest_framework import serializers
# from django.contrib.auth.models import User
#
#
# # User Serializer
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email')
#
#
# # Register Serializer
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'password')
#         extra_kwargs = {'password': {'write_only': True}, 'firstname': {'write_only': True}}
#
#     def create(self, validated_data):
#         user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'],
#                                         validated_data['password'])
#
#         return user
