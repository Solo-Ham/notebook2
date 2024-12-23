from .models import CustomUser, Note
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.response import Response

from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


class RegisterSerializer(ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = get_user_model()
        fields = ['id','email', 'name', 'password1', 'password2']
        read_only_fields = ['id']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise ValidationError("The two passwords must match")
        
        return data
    
    def create(self, valiadted_data):
        valiadted_data.pop('password2')


        user = CustomUser.objects.create_user(
            email = valiadted_data['email'],
            name = valiadted_data['name'],
            password = valiadted_data['password1']
        )

        return user

class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = ["title", 'body']


class NoteDisplaySerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'body', 'date']
        read_only_fields = ['id', 'date']

class CustomTokenObtainSerializer(TokenObtainSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
    
        user = self.user
        data['email'] = user.email
        data['name'] = user.name

        print(data)

        return data

class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'name']


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_data(self, value):
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            return Response({"message": "User with this email does not exist"})
        return value
    
    def save(self):
        user = CustomUser.objects.get(email=self.validated_data['email'])
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        email = self.validated_data['email']
        reset_link = f"https://solo-ham.github.io/solonote.github.io/reset_password.html?uid={uid}&token={token}"
        send_mail(
            "Password Reset",
            f"Please click the link below to reset your password\n{reset_link}",
            "solomonobonyo74@gmail.com",
            [email]
        )
    

