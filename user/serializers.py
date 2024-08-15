from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, FriendRequest



class UserSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ('name', 'email', 'password')

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format.")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")

        return value

    def create(self, validated_data):
        validated_data['username'] = validated_data['email'] 
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['name'],
            password=validated_data['password']
        )
        return user



class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid email or password.")
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'name': user.first_name,
                'email': user.email
            }
        }




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']



class PendingFriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user']

    def get_from_user(self, obj):
        user = obj.from_user
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }
